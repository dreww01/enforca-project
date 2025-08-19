from fastapi import APIRouter, HTTPException
import logging
from models.user_models import LogoutRequest
from database.users import load_users, save_users
from utils.email_utils import send_email


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


@router.post("/logout")
def logout(request: LogoutRequest):
    try:
        users = load_users()
        user = next((u for u in users if u["email"] == request.email), None)
        if not user:
            logging.warning(f"Logout failed: User with email '{request.email}' not found.")
            raise HTTPException(status_code=404, detail="User not found")

        # Invalidate all session and OTP data for this user
        session_cleared = user.get("session_token") or user.get("session_expiry")
        otp_cleared = user.get("otp") or user.get("otp_expiry")

        user["session_token"] = None
        user["session_expiry"] = None
        user["otp"] = None
        user["otp_expiry"] = None
        save_users(users)

        if session_cleared or otp_cleared:
            
            # Logout notification sent to email
            message = f"You have been logged out successfully."
            send_email(user["email"], "Logout notification", message)

            logging.info(f"User with email '{request.email}' logged out and relevant tokens cleared.")
        else:
            logging.info(f"Logout called for user with email '{request.email}', but no session or OTP was set.")
        
        return {
            "message": "Logout successful. All sessions and OTPs for this email have been cleared."
        }
    except Exception as e:
        logging.error(f"Logout error for user with email '{request.email}': {e}")
        raise HTTPException(status_code=500, detail="Logout failed.")