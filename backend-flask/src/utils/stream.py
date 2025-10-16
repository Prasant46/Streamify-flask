from stream_chat import StreamChat
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def get_stream_client():
  api_key = current_app.config.get('STREAM_API_KEY')
  api_secret = current_app.config.get('STREAM_API_SECRET')
  
  if not api_key or not api_secret:
    logger.error("Stream API key or secret not configured.")
    raise None
  return StreamChat(api_key = api_key, api_secret = api_secret)

def upsert_stream_user(user_data):
  try:
    client = get_stream_client()
    if not client:
      return None
    
    client.update_user([user_data])
    logger.info(f"Upserted Stream user: {user_data.get('id')}")
    return user_data
  except Exception as e:
    logger.error(f"Error upserting Stream user: {e}")
    return None
  
def generate_stream_token(user_id):
  try:
    client = get_stream_client()
    if not client:
      return None
    
    user_id_str = str(user_id)
    token = client.create_token(user_id_str)
    logger.info(f"Generated Stream token for user: {user_id}")
    return token
  except Exception as e:
    logger.error(f"Error generating Stream token: {e}")
    return None