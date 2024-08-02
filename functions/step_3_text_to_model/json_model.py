from enum import Enum
from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field

class TechnologyGroupEnum(str, Enum):
    BUSINESS_INTELLIGENCE = "Business Intelligence and Data Visualization"
    CLOUD_PLATFORMS = "Cloud Platforms and Services"
    ERP = "Enterprise Resource Planning (ERP)"
    PROGRAMMING_LANGUAGES = "Programming Languages"
    DATABASE_TECHNOLOGIES = "Database Technologies"
    DEVOPS = "DevOps and CI/CD"
    CONTAINERIZATION = "Containerization and Orchestration"
    NETWORKING_SECURITY = "Networking and Security"
    BACKEND_DEVELOPMENT = "Backend Development"
    FRONTEND_DEVELOPMENT = "Frontend Development"
    AUTOMATION_SCRIPTING = "Automation and Scripting"
    MACHINE_LEARNING = "Machine Learning and AI"
    BIG_DATA = "Big Data Technologies"
    SOFTWARE_DEVELOPMENT_PRACTICES = "Software Development Practices"
    IDES_AND_TOOLS = "Integrated Development Environments (IDEs) and Tools"
    MOBILE_DEVELOPMENT = "Mobile Development"
    GAME_DEVELOPMENT = "Game Development"
    BUSINESS_APPLICATIONS = "Business Applications"
    HARDWARE_EMBEDDED = "Hardware and Embedded Systems"
    IOT = "Internet of Things (IoT)"
    PROJECT_MANAGEMENT = "Project Management and Collaboration"
    VISUALIZATION_DESIGN = "Visualization and Design"
    NETWORKING_INFRASTRUCTURE = "Networking and Infrastructure"
    TESTING_QA = "Testing and Quality Assurance"
    EMERGING_TECHNOLOGIES = "Emerging Technologies"
    ECOMMERCE = "E-Commerce Technologies"
    MISCELLANEOUS_TECHNOLOGIES = "Miscellaneous Technologies"

class JobPostingModel(BaseModel):
    """
    Model for job postings with strict enforcement of technology groups.
    
    Instructions for filling out the JobPostingModel:
    1. List all specific technologies mentioned in the job description in the 'technologies' field.
    2. For each technology, identify the most appropriate TechnologyGroupEnum and include it in the 'groups' field.
    3. Ensure that each group in 'groups' corresponds to at least one technology in 'technologies'.
    4. Use ONLY the predefined TechnologyGroupEnum values for the 'groups' field.
    5. If a technology doesn't clearly fit into any group, use the MISCELLANEOUS_TECHNOLOGIES group.

    Available TechnologyGroupEnum values:
    - BUSINESS_INTELLIGENCE: "Business Intelligence and Data Visualization"
    - CLOUD_PLATFORMS: "Cloud Platforms and Services"
    - ERP: "Enterprise Resource Planning (ERP)"
    - PROGRAMMING_LANGUAGES: "Programming Languages"
    - DATABASE_TECHNOLOGIES: "Database Technologies"
    - DEVOPS: "DevOps and CI/CD"
    - CONTAINERIZATION: "Containerization and Orchestration"
    - NETWORKING_SECURITY: "Networking and Security"
    - BACKEND_DEVELOPMENT: "Backend Development"
    - FRONTEND_DEVELOPMENT: "Frontend Development"
    - AUTOMATION_SCRIPTING: "Automation and Scripting"
    - MACHINE_LEARNING: "Machine Learning and AI"
    - BIG_DATA: "Big Data Technologies"
    - SOFTWARE_DEVELOPMENT_PRACTICES: "Software Development Practices"
    - IDES_AND_TOOLS: "Integrated Development Environments (IDEs) and Tools"
    - MOBILE_DEVELOPMENT: "Mobile Development"
    - GAME_DEVELOPMENT: "Game Development"
    - BUSINESS_APPLICATIONS: "Business Applications"
    - HARDWARE_EMBEDDED: "Hardware and Embedded Systems"
    - IOT: "Internet of Things (IoT)"
    - PROJECT_MANAGEMENT: "Project Management and Collaboration"
    - VISUALIZATION_DESIGN: "Visualization and Design"
    - NETWORKING_INFRASTRUCTURE: "Networking and Infrastructure"
    - TESTING_QA: "Testing and Quality Assurance"
    - EMERGING_TECHNOLOGIES: "Emerging Technologies"
    - ECOMMERCE: "E-Commerce Technologies"
    - MISCELLANEOUS_TECHNOLOGIES: "Miscellaneous Technologies"
    """
    position: Optional[str] = Field(None, description="Exact job title or position name as stated in the posting.")
    company: Optional[str] = Field(None, description="Full and official name of the company offering the job.")
    job_description: Optional[str] = Field(None, description="Comprehensive summary of job responsibilities, duties, and expectations.")
    contact_name: Optional[str] = Field(None, description="Full name of the person to contact about the job listing.")
    contact_phone: Optional[str] = Field(None, description="Complete phone number with country code for the contact person.")
    contact_email: Optional[str] = Field(None, description="Professional email address for inquiries about the position.")
    technologies: List[str] = Field(default_factory=list, description="Specific technical skills, programming languages, or software mentioned as required or preferred for the role.")
    groups: List[str] = Field(default_factory=list, description="Categorize the technologies listed above into the most relevant TechnologyGroupEnum categories. Use ONLY the predefined enum values.")
    experience: Optional[str] = Field(None, description="Specific years or level of experience required, e.g., '3-5 years in software development' or 'Senior level'.")
    required_qualifications: List[str] = Field(default_factory=list, description="Essential skills, certifications, or abilities needed for the job.")
    education: Optional[str] = Field(None, description="Minimum educational requirement, including degree level and field of study if specified.")
    location: Optional[str] = Field(None, description="Specific work location including city and country")
    fulltime: Optional[bool] = Field(None, description="True if the job is explicitly stated as full-time, False if part-time. Default to True if not specified.")
    industry: Optional[str] = Field(None, description="Primary industry sector of the company, e.g., 'Financial Services', 'Healthcare Technology'.")
    application_deadline: Optional[str] = Field(None, description="Last date to apply for the position in UTC time, formatted as 'YYYY-MM-DDTHH:MM:SSZ'.")
    posting_time: Optional[str] = Field(None, description="Date and time when the job was initially posted, in UTC time, formatted as 'YYYY-MM-DDTHH:MM:SSZ'.")

    class Config:
        schema_extra = {
            "example": {
                "position": "Senior Software Engineer",
                "company": "TechCorp Inc.",
                "technologies": ["Python", "AWS", "Docker", "Kubernetes"],
                "groups": [
                    TechnologyGroupEnum.PROGRAMMING_LANGUAGES,
                    TechnologyGroupEnum.CLOUD_PLATFORMS,
                    TechnologyGroupEnum.CONTAINERIZATION
                ],
                "experience": "5+ years in software development",
                "required_qualifications": ["Bachelor's degree in Computer Science", "Experience with microservices"],
                "location": "San Francisco, USA"
            }
        }