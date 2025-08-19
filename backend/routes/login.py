from fastapi import APIRouter, HTTPException, Depends
import logging
from models.user_models import LoginRequest, VerifyLoginOTPRequest
from database.users import load_users, save_users
from auth.otp import generate_otp
from auth.sessions import generate_session_token
from datetime import datetime, timedelta
from utils.email_utils import send_email


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')




@router.post("/login")
def login(request: LoginRequest):
    try:
        users = load_users()
        user = next((u for u in users if u["email"] == request.email), None)
        if not user:
            logging.warning(f"Login failed: User with email '{request.email}' not found.")
            raise HTTPException(status_code=404, detail="User not found")
        if user["password"] != request.password:
            logging.warning(f"Login failed: Invalid password for user '{request.email}'.")
            raise HTTPException(status_code=400, detail="Invalid password")

        otp = generate_otp()
        otp_expiry = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
        user["otp"] = otp
        user["otp_expiry"] = otp_expiry
        save_users(users)

        # Send email to user
        message = f"Your login OTP code is: {otp}, code expires in 10 minutes."
        send_email(user["email"], "Login Verification OTP", message) 

        logging.info(f"Login OTP sent to user with email '{request.email}'. OTP: {otp}")
        return {"message": "OTP sent to your email. Please verify to complete login."}
    except Exception as e:
        logging.error(f"Login error for user with email '{request.email}': {e}")
        raise HTTPException(status_code=500, detail="Login failed.")

@router.post("/verify-login-otp")
def verify_login_otp(request: VerifyLoginOTPRequest):
    try:
        users = load_users()
        user = next((u for u in users if u["email"] == request.email), None)
        if not user:
            logging.warning(f"OTP verification failed: User with email '{request.email}' not found.")
            raise HTTPException(status_code=404, detail="User not found")
        if user.get("otp") != request.otp:
            logging.warning(f"OTP verification failed: Invalid OTP for user with email '{request.email}'.")
            raise HTTPException(status_code=400, detail="Invalid OTP")
        if not user.get("otp_expiry") or datetime.utcnow() > datetime.fromisoformat(user["otp_expiry"]):
            logging.warning(f"OTP verification failed: OTP expired for user with email '{request.email}'.")
            raise HTTPException(status_code=400, detail="OTP expired")

        # OTP correct, create session
        session_token = generate_session_token()
        session_expiry = (datetime.utcnow() + timedelta(minutes=10)).isoformat()

        user["session_token"] = session_token
        user["session_expiry"] = session_expiry
        user["otp"] = None
        user["otp_expiry"] = None
        save_users(users)

        # Send email to user
        message = f"You have successfully logged in."
        send_email(user["email"], "Login Notification", message)

        logging.info(f"User with email '{request.email}' successfully logged in. Session token generated: {session_token}")
        return {
            "message": "Login verified. You are now logged in.",
            "session_token": session_token,
            "session_expiry": session_expiry,
        }
    except Exception as e:
        logging.error(f"OTP login verification error for user with email '{request.email}': {e}")
        raise HTTPException(status_code=500, detail="OTP verification for login failed.")
