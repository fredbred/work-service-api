from fastapi import FastAPI, HTTPException
from uuid import UUID
from models import User, Gender, Shift, UpdateUser
import datetime

# To create the FastAPI
app = FastAPI()

# We create a small database to test our API
db: list[User] = [
    User(
        id="2ce60a7e-9292-47dc-868a-ac6f634ebbbd",
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        shifts=[[datetime.date(2022, 1, 30), Shift.evening], [datetime.date(2022, 1, 31), Shift.evening]]
        ),

    User(
        id="4374873f-4e87-42ba-9837-0f4cc796c04d",
        first_name="Will",
        last_name="Smith",
        gender=Gender.male,
        shifts=[[datetime.date(2022, 1, 25), Shift.night], [datetime.date(2022, 1, 26), Shift.day]]
        ),

    User(
        id="ccf004e5-4f3b-424c-a947-05f4d8205ac3",
        first_name="Mary",
        last_name="Poppins",
        gender=Gender.female,
        shifts=[[datetime.date(2022, 2, 3), Shift.day], [datetime.date(2022, 2, 4), Shift.evening], [datetime.date(2022, 2, 3), Shift.evening]]
        )
]


@app.get("/")   # To make sure the application started
async def root():
    return{"Hello": "API Test"}


@app.get("/api/v1/users")   # To fetch all the users in database
async def fetch_users():
    return db


@app.get("/api/v1/users/{user_id}")   # To fetch a user in database
async def fetch_user(user_id: UUID):
    for user in db:  # For each user in database
        if user.id == user_id:  # If the user is in the database
            return user
    # If the user is not found, return an exception
    raise HTTPException(
        status_code=404,
        detail=f"User ID: {user_id} doesn't exist."
    )

@app.get("/api/v1/users/planning/{user_id}")   # To fetch a user in database
async def fetch_user_planning(user_id: UUID):
    for user in db:  # For each user in database
        if user.id == user_id:  # If the user is in the database
            return user.shifts
    # If the user is not found, return an exception
    raise HTTPException(
        status_code=404,
        detail=f"User ID: {user_id} doesn't exist."
    )


@app.post("/api/v1/users")  # To add a user (see User base model in models.py)
async def new_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")  # To remove a user from the database
async def remove_user(user_id: UUID):
    for user in db:             # For each user in database
        if user.id == user_id:  # If the user is in the database
            db.remove(user)
            return
    # If the user is not found, return an exception
    raise HTTPException(
        status_code=404,
        detail=f"User ID: {user_id} doesn't exist."
    )


@app.put("/api/v1/users/{user_id}")     # To update first name and/or last name and/or shifts
async def update_user(user_update: UpdateUser, user_id: UUID):
    for user in db:     # For each user in database
        if user.id == user_id:  # If the user is in the database
            if user_update.first_name is not None:  # Update first name if field present in the body request
                user.first_name = user_update.first_name
            if user_update.last_name is not None:   # Update last name if field present in the body request
                user.last_name = user_update.last_name
            if user_update.shifts is not None:      # Update shifts if field present in the body request
                for up_date in user_update.shifts.keys():   # To handle multiple shifts update
                    if up_date not in user.shifts.keys():   # Check if the date is not in the user's shifts already
                        user.shifts[up_date] = user_update.shifts.get(up_date)
                    else:   # If the date already has a shift associated, raise an exception
                        raise HTTPException(
                            status_code=400,
                            detail=f"User ID: {user_id} will already work on {up_date} on the {user.shifts.get(up_date)} shift"
                        )
            return
    # If the user is not found, return an exception
    raise HTTPException(
        status_code=404,
        detail=f"User ID: {user_id} doesn't exist."
        )

