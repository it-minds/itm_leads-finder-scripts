def html_text_quality_control(html_text_str: str | None):
    
    # Check if html_text_str is None, then the scraping failed
    if not html_text_str:
        return "Scraping failed" 
    
    # Check if text string is too short for context to make sense
    if len(html_text_str) < 300:
        return "Text too short"
    
    # If no checks fail, return False and let the object be updated
    return None
