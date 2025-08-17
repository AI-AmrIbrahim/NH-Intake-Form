from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional, Union
import datetime

class UserProfile(BaseModel):
    profile_code: str
    security_question_1: str
    security_answer_1: str
    security_question_2: str
    security_answer_2: str
    security_question_3: str
    security_answer_3: str
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

    @validator('weight_lbs', pre=True, allow_reuse=True)
    def validate_weight(cls, v):
        if v is None or v == '':
            return None
        try:
            weight = float(v)
            if weight <= 0:
                raise ValueError('Weight must be a positive number.')
            return weight
        except (ValueError, TypeError):
            raise ValueError('Please enter a valid number for weight.')

    @validator('security_answer_1', 'security_answer_2', 'security_answer_3', pre=True, allow_reuse=True)
    def validate_security_answers(cls, v):
        if not v or not v.strip():
            raise ValueError('Please answer all three security questions.')
        return v

    @root_validator(pre=True)
    def validate_unique_security_questions(cls, values):
        q1 = values.get('security_question_1')
        q2 = values.get('security_question_2')
        q3 = values.get('security_question_3')
        if len({q1, q2, q3}) != 3:
            raise ValueError('Please select three unique security questions.')
        return values
