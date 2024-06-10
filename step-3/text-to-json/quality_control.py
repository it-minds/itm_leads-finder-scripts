from json_model import JobPostingModel

def json_model_quality_control(object: JobPostingModel, id: str):
    # Check if company is None
    if not object.company:
        return "company failure"
    
    # Check if job description is None or its length is less than 100 chars
    if not object.job_description or len(object.job_description) < 100:
        return "job description failure"
    
    # Check if required qualifications and technologies combined are less than 3
    if len(object.required_qualifications) + len(object.technologies) < 3:
        return "qualifications + technologies failure"
    
    # Check if both application deadline and posting time are None
    if not object.application_deadline and not object.posting_time:
        return "deadline + posting time failure"
    
    # If no checks fail, return False and let the object be updated
    return None
