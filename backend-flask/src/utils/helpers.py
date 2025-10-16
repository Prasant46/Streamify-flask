import re
from flask import current_app

def validate_email(email):
  """Validate email format"""
  email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
  return re.match(email_regex, email) is not None
  
def paginate_query(query, page=1, per_page=None):
  if per_page is None or page < 1:
    per_page = current_app.config.get('ITEMS_PER_PAGE', 20)
    
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    ) 