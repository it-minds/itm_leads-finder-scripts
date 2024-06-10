from json_model import JobPostingModel

def json_model_quality_control(object: JobPostingModel, id: str):
    # Check if company is None
    if not object.company:
        return True
    
    # Check if job description is None or its length is less than 100 chars
    if not object.job_description or len(object.job_description) < 100:
        print(f"job description failure, {id}")
        return True
    
    # Check if required qualifications and technologies combined are less than 3
    if len(object.required_qualifications) + len(object.technologies) < 3:
        print(f"qualifications + technologies failure, {id}")
        return True
    
    # Check if both application deadline and posting time are None
    if not object.application_deadline and not object.posting_time:
        print(f"deadline + posting time failure, {id}")
        return True
    
    # If no checks fail, return False and let the object be updated
    return False
