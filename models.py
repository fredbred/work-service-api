from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum
import datetime

# Just an example of other fields we could add
class Gender(str, Enum):
    male = "male"
    female = "female"

class Shift(str, Enum):
    night = "0-8"
    day = "8-16"
    evening = "16-24"

# The base model for our users in the database
class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    gender: Gender
    shifts: dict[datetime.date, Shift]

# The class used to update a user, every field is Optional
class UpdateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    shifts: Optional[dict[datetime.date, Shift]]
