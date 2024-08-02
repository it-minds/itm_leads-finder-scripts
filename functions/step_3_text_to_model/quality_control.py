from enum import Enum
import logging
from typing import List, Union
from difflib import get_close_matches
from .json_model import JobPostingModel, TechnologyGroupEnum

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
    
def clean_job_posting_groups(job_posting: JobPostingModel) -> JobPostingModel:
    def get_enum_value(item: Union[str, Enum]) -> str:
        return item.value if isinstance(item, Enum) else str(item)

    valid_groups = {get_enum_value(group): group for group in TechnologyGroupEnum}
    
    original_groups = job_posting.groups
    cleaned_groups: List[TechnologyGroupEnum] = []
    
    for group in original_groups:
        group_value = get_enum_value(group)
        if group_value in valid_groups:
            cleaned_groups.append(valid_groups[group_value])
        else:
            # Try to find a close match for the group name
            close_matches = get_close_matches(group_value, valid_groups.keys(), n=1, cutoff=0.6)
            if close_matches:
                matched_group = valid_groups[close_matches[0]]
                cleaned_groups.append(matched_group)
                logging.info(f"Matched '{group_value}' to '{matched_group.value}'")
            else:
                logging.warning(f"Removed invalid group: {group_value}")

    # Remove duplicates while preserving order
    cleaned_groups = list(dict.fromkeys(cleaned_groups))

    if cleaned_groups != original_groups:
        logging.info(f"Updated groups from {[get_enum_value(group) for group in original_groups]} to {[group.value for group in cleaned_groups]}")
        job_posting.groups = cleaned_groups

    return job_posting