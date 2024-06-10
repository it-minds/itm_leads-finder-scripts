from json_model import JobPostingModel
def json_model_quality_control(object: JobPostingModel):
    
    if(object.company == None):
        return True
    
    if(len(object.job_description) < 150):
        return True
    
    if((len(object.required_qualifications) + len(object.technologies)) < 3):
        return True
    
    if(object.application_deadline == None & object.posting_time == None):
        return True
    
    
    #If no checks fail return false and let object be updated
    return False