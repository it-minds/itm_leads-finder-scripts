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
    Represents a job posting, encapsulating all relevant details extracted from user messages or postings. This model is designed to parse and structure 
    data from natural language inputs, ensuring that information such as job title, salary range, and qualifications are accurately captured and represented.
    
    
    
    These are the enums available to use in the groups property
     *IMPORTANT* Each TechnologyGroup should appear only once in the list!
    The list can be empty if no relevant technology groups apply.
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
    
   
    """
    
    position: Optional[str] = Field(
        description="Exact job title or position name as stated in the posting."
    )
    company: Optional[str] = Field(
        description="Full and official name of the company offering the job."
    )
    job_description: Optional[str] = Field( 
        description="Comprehensive summary of job responsibilities, duties, and expectations."
    )
    contact_name: Optional[str] = Field(
        description="Full name of the person to contact about the job listing."
    )
    contact_phone: Optional[str] = Field(
        description="Complete phone number with country code for the contact person."
    )
    contact_email: Optional[str] = Field(
        description="Professional email address for inquiries about the position."
    )
    technologies: List[str] = Field(
        description="Specific technical skills, programming languages, or software mentioned as required or preferred for the role. List each separately."
    )
    groups: List[TechnologyGroupEnum] = Field(
        description="Categorize the technologies listed above into the most relevant TechnologyGroupEnum categories. Multiple categories can be selected if applicable. You can only use the enums represented in TechnologyGroupEnum, If none found leave as an empty list"
    )
    experience: Optional[str] = Field(
        description="Specific years or level of experience required, e.g., '3-5 years in software development' or 'Senior level'."
    )
    required_qualifications: List[str] = Field(
        description="Essential skills, certifications, or abilities needed for the job. List each qualification separately."
    )
    education: Optional[str] = Field(
        description="Minimum educational requirement, including degree level and field of study if specified."
    )
    location: Optional[str] = Field(
        description="Specific work location including city and country"
    )
    fulltime: Optional[bool] = Field(
        description="True if the job is explicitly stated as full-time, False if part-time. Default to True if not specified."
    )
    industry: Optional[str] = Field(
        description="Primary industry sector of the company, e.g., 'Financial Services', 'Healthcare Technology'."
    )
    application_deadline: Optional[str] = Field(
        description="Last date to apply for the position in UTC time, formatted as 'YYYY-MM-DDTHH:MM:SSZ'."
    )
    posting_time: Optional[str] = Field(
        description="Date and time when the job was initially posted, in UTC time, formatted as 'YYYY-MM-DDTHH:MM:SSZ'."
    )
