from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Status = Literal["Applied", "Interview", "Offer", "Rejected"]


class JobCreate(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)
    status: Status = "Applied"
    notes: str | None = Field(default=None, max_length=500)

class JobUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=100)
    role: str | None = Field(default=None, min_length=1, max_length=100)
    status: Status | None = None
    notes: str | None = Field(default=None, max_length=500)
    

class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    status: str
    applied_date: date
    notes: str | None