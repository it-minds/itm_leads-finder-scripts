from .json_model import JobPostingModel

def check_quality(self: JobPostingModel):
    prioritized_properties = ['company', 'position', 'job_description']

    # Check prioritized properties
    for prop in prioritized_properties:
        if not getattr(self, prop):
            return {
                'marked': True,
                'reasons': [prop]  # Return the specific property that is null or empty
            }

    # If all prioritized properties are not null or empty, check the rest
    remaining_properties = [
        'technologies',
        'experience', 'required_qualifications', 'education', 'location',
        'fulltime', 'industry',
    ]

    null_count = 0
    null_properties = []

    for prop in remaining_properties:
        if not getattr(self, prop):
            null_count += 1
            null_properties.append(prop)
    
    if null_count >= 5:
        return {
            'marked': True,
            'reasons': null_properties
        }

    return {
        'marked': False,
        'reason': 'Quality meets expectations'
    }
