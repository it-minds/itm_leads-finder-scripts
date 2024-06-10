from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import datetime


class JobPostingModel(BaseModel):
    position: Optional[str] = Field(description="Job position")
    company: Optional[str] = Field(description="Company name")
    job_description: Optional[str] = Field(description="Job description")
    contact_name: Optional[str] = Field(description="Contact person's name")
    contact_phone: Optional[str] = Field(description="Contact person's phone number")
    contact_email: Optional[str] = Field(description="Contact person's email")
    technologies: List[str] = Field(
        description="List of technologies required for the job, if there are no technologies leave it as an empty list"
    )
    experience: Optional[str] = Field(description="Experience required for the job")
    required_qualifications: List[str] = Field(
        description="List of required qualifications for the job, if none is found, leave it as an empty list"
    )
    location: Optional[str] = Field(description="Job location")
    work_hours: Optional[str] = Field(description="Work hours")
    industry: Optional[str] = Field(description="Industry of the company")
    application_deadline: Optional[datetime] = Field(
        description="Application deadline in UTC-0 and ISO 8601 format"
    )
    posting_time: Optional[datetime] = Field(
        description="Job posting time in UTC-0 and ISO 8601 format"
    )
    website_source: Optional[str] = Field(
        description="Website source of the job posting"
    )