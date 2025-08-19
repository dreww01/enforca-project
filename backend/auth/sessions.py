from datetime import datetime, timedelta
import secrets
from fastapi import HTTPException
import logging
from database.users import load_users

# LOGGER
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# SESSION GENERATION USING SECRETS MODULE
def generate_session_token():
    return secrets.token_urlsafe(32)

# TO CHECK SESSION
async def check_session(username: str, session_token: str):
    users = await load_users()
    user = next((u for u in users if u["username"] == username), None)
    if (
        not user
        or user.get("session_token") != session_token
        or not user.get("session_expiry")
        or datetime.utcnow() > datetime.fromisoformat(user["session_expiry"])
    ):
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    return user

# to log invalid sessions
def validate_session(username: str, session_token: str):
    users = load_users()
    user = next((u for u in users if u["username"] == username), None)

    # Check if user exists
    if not user:
        logging.warning(f"Session validation failed: Username '{username}' not found.")
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    # Check if session token exists
    if not user.get("session_token"):
        logging.warning(f"Session validation failed: No session token for user '{username}'.")
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    # Check if session token is valid
    if user.get("session_token") != session_token:
        logging.warning(f"Session validation failed: Invalid session token for user '{username}'.")
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    # Check if session is expired
    if not user.get("session_expiry") or datetime.utcnow() > datetime.fromisoformat(user.get("session_expiry")):
        logging.warning(f"Session validation failed: Session expired for user '{username}'.")
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    return user