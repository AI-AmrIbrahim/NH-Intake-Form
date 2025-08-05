from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Union
import datetime

class UserProfile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
    dob: Optional[datetime.date] = None
    sex: Optional[str] = None
    height_ft: Optional[int] = Field(None, ge=4, le=7)
    height_in: Optional[int] = Field(None, ge=0, le=11)
    weight_lbs: Optional[Union[float, int]] = Field(None, description="Weight in pounds")
    physical_activity: Optional[str] = None
    energy_level: Optional[str] = None
    diet: Optional[str] = None
    meals_per_day: Optional[str] = None
    sleep_quality: Optional[str] = None
    stress_level: Optional[str] = None
    pregnant_or_breastfeeding: Optional[str] = None
    medical_conditions: List[str] = []
    current_medications: List[str] = []
    natural_supplements: List[str] = []
    allergies: List[str] = []
    health_goals: List[str] = []
    other_health_goal: Optional[str] = None
    interested_supplements: List[str] = []
    additional_info: Optional[str] = None

    @validator('first_name', 'last_name', pre=True, allow_reuse=True)
    def validate_name(cls, v):
        if v and not v.isalpha():
            raise ValueError("Name must only contain letters.")
        return v

    @validator('phone_number', pre=True, allow_reuse=True)
    def validate_phone_number(cls, v):
        if v:
            if not v.isdigit() or len(v) != 10:
                raise ValueError("Please enter a valid 10-digit phone number.")
        return v

    @validator('weight_lbs', pre=True)
    def validate_weight(cls, v):
        if v is None or v == '':
            return None
        try:
            weight = float(v)
        except (ValueError, TypeError):
            raise ValueError('Please enter a valid number for weight.')
        if weight <= 0:
            raise ValueError('Weight must be a positive number.')
        return weight
