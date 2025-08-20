from fastapi import APIRouter, HTTPException
import logging
from models.user_models import ResendOTPRequest
from database.users import load_users, save_users
from auth.otp import generate_otp
from datetime import datetime, timedelta
from utils.email_utils import send_email

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)



@router.post("/resend-otp")
def resend_otp(request: ResendOTPRequest):
    try:
        users = load_users()
        user = next((u for u in users if u["email"] == request.email), None)
        if not user:
            logging.warning(f"Resend OTP failed: User with email '{request.email}' not found.")
            raise HTTPException(status_code=404, detail="User not found")

        if user["is_verified"]:
            logging.warning(f"Resend OTP failed: User '{user['username']}' already verified.")
            raise HTTPException(status_code=400, detail="User already verified")

        otp = generate_otp()
        user["otp"] = otp
        user["otp_expiry"] = (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        save_users(users)

        message = f"Your OTP code is: {otp}"
        send_email(user["email"], "Resend OTP", message)
        logging.info(f"OTP resent to user '{user['username']}', email: {user['email']}.")
        return {"message": "OTP resent successfully"}
    
    except Exception as e:
        logging.error(f"Resend OTP error: {e}")
        raise HTTPException(status_code=500, detail="Resend OTP failed.")