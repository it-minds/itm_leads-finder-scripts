from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import datetime


class JobPostingModel(BaseModel):
    # """
    # Represents a job posting, encapsulating all relevant details extracted from user messages or postings. This model is designed to parse and structure 
    # data from natural language inputs, ensuring that information such as job title, salary range, and qualifications are accurately captured and represented.
    # """
    position: Optional[str] = Field(
        description="The job position/title within the company."
    )
    company: Optional[str] = Field(
        description="The name of the company offering the job."
    )
    job_description: Optional[str] = Field( 
        description="A detailed description of the job responsibilities and role."
    )
    contact_name: Optional[str] = Field(
        description="The name of the contact person responsible for the job listing."
    )
    contact_phone: Optional[str] = Field(
        description="Phone number of the contact person."
    )
    contact_email: Optional[str] = Field(
        description="Email address of the contact person."
    )
    technologies: List[str] = Field(
        description="List of technologies required and/or used for the job. Leave as an empty list if none."
    )
    experience: Optional[str] = Field(
        description="Experience level (e.g., '3 years of experience') required for the job."
    )
    required_qualifications: List[str] = Field(
        description="List of required qualifications (e.g., skills, certifications) for the job. Leave as an empty list if none."
    )
    education: Optional[str] = Field(
        description="Level of education required for the job (e.g., 'Bachelor's degree')."
    )
    location: Optional[str] = Field(
        description="Location where the job is based (e.g., city, country)."
    )
    fulltime: Optional[bool] = Field(
        description="Boolean indicating if the job is full-time (True) or part-time (False), if nothing suggests that the job is part-time, it is most likely full-time."
    )
    industry: Optional[str] = Field(
        description="Industry to which the company belongs (e.g., 'Technology', 'Healthcare')."
    )
    application_deadline: Optional[str] = Field(
        description="Deadline for submitting applications in UTC-0 and ISO 8601 format (e.g., '2024-12-31T23:59:59Z')."
    )
    posting_time: Optional[str] = Field(
        description="Date and time when the job was posted in UTC-0 and ISO 8601 format (e.g., '2024-06-14T12:00:00Z')."
    )