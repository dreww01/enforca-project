from fastapi import APIRouter, HTTPException, Depends
import logging
from models.user_models import RegisterRequest, VerifyOTPRequest
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





@router.post("/register")
def register(request: RegisterRequest):
    """Register a new user and send OTP to email."""
    try:
        users = load_users()
        if any(u["username"] == request.username for u in users):
            logging.warning(f"Registration failed: Username '{request.username}' already exists.")
            raise HTTPException(status_code=400, detail="Username already exists")

        otp = generate_otp()
        otp_expiry = (datetime.utcnow() + timedelta(minutes=20)).isoformat()

        new_user = {
            "name": request.name,
            "username": request.username,
            "password": request.password,
            "email": request.email,
            "otp": otp,
            "otp_expiry": otp_expiry,
            "is_verified": False,
        }
        users.append(new_user)
        save_users(users)

        # Send OTP email
        message = f"Your OTP code is: {otp}, Code expires in 20 minutes."
        send_email(request.email, "Account Verification OTP", message)
        logging.info(f"User '{request.username}' registered and OTP sent.")
        return {"message": "User registered. OTP sent to email."}
    
    except Exception as e:
        logging.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed.")


@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest):
    try:
        users =  load_users()
        user = next((u for u in users if u["email"] == request.email), None)
        if not user:
            logging.warning(f"OTP verification failed: User '{request.email}' not found.")
            raise HTTPException(status_code=404, detail="User not found")
        if user["otp"] != request.otp:
            logging.warning(f"OTP verification failed: Invalid OTP for user '{request.email}'.")
            raise HTTPException(status_code=400, detail="Invalid OTP")
        if datetime.utcnow() > datetime.fromisoformat(user["otp_expiry"]):
            logging.warning(f"OTP verification failed: OTP expired for user '{request.email}'.")
            raise HTTPException(status_code=400, detail="OTP expired")

        # Session logic
        session_token = generate_session_token()
        session_expiry = (datetime.utcnow() + timedelta(minutes=20)).isoformat()

        user["is_verified"] = True
        user["otp"] = None
        user["otp_expiry"] = None
        user["session_token"] = session_token
        user["session_expiry"] = session_expiry
        save_users(users)

        # Send email to user
        message = f"Your account was registered successfully."
        send_email(user["email"], "Registrstion Notification", message)

        logging.info(f"User '{request.email}' verified successfully. Session token generated: {session_token}, expires: {session_expiry}")

        return {"message": "OTP verified. Account activated.", "session_token": session_token, "session_expiry": session_expiry}
    except Exception as e:
        logging.error(f"OTP verification error for user '{request.email}': {e}")
        raise HTTPException(status_code=500, detail="OTP verification failed.")
