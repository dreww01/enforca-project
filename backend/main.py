# FastAPI and dependencies
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# JSON user storage
import json
import os

# Utilities
from datetime import datetime, timedelta
import asyncio
import smtplib
from email.mime.text import MIMEText
import logging
import string
import secrets
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = FastAPI()

# Path to JSON file - simple json database
USER_DB_PATH = "users.json"

# Helper to load users from JSON
def load_users():
    if not os.path.exists(USER_DB_PATH):
        return []
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)

# Helper to save users to JSON
def save_users(users):
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f, indent=2)


# ---------------- SCHEMAS ----------------
class RegisterRequest(BaseModel):
    name: str
    username: str
    password: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str


class VerifyOTPRequest(BaseModel):
    username: str
    otp: str

class ResendOTPRequest(BaseModel):
    email: str

class LogoutRequest(BaseModel):
    email: str


class VerifyLoginOTPRequest(BaseModel):
    email: str
    otp: str


# ---------------- HELPERS ----------------
def generate_otp():
    num = string.digits
    OTP = ''.join(secrets.choice(num) for _ in range(6))
    return OTP
    

# Send email using GMAIL SMTP server
SENDER_MAIL = os.getenv("EMAIL_USER", "")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_MAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_MAIL, os.getenv("EMAIL_PASSWORD"))
            server.sendmail(msg["From"], [to_email], msg.as_string())
        logging.info(f"Email sent to {to_email} with subject '{subject}'")
    except Exception as e:
        logging.error(f"Email send failed to {to_email}: {e}")

# OTP GENERATION USING SECRETS MODULE
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


# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- ROUTES ----------------
@app.get("/")
async def root():
    return {"message": "WELCOME TO MY AUTHENTICATION SERVER!"}

@app.post("/register")
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


@app.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest):
    try:
        users =  load_users()
        user = next((u for u in users if u["username"] == request.username), None)
        if not user:
            logging.warning(f"OTP verification failed: User '{request.username}' not found.")
            raise HTTPException(status_code=404, detail="User not found")
        if user["otp"] != request.otp:
            logging.warning(f"OTP verification failed: Invalid OTP for user '{request.username}'.")
            raise HTTPException(status_code=400, detail="Invalid OTP")
        if datetime.utcnow() > datetime.fromisoformat(user["otp_expiry"]):
            logging.warning(f"OTP verification failed: OTP expired for user '{request.username}'.")
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

        logging.info(f"User '{request.username}' verified successfully. Session token generated: {session_token}, expires: {session_expiry}")

        return {"message": "OTP verified. Account activated.", "session_token": session_token, "session_expiry": session_expiry}
    except Exception as e:
        logging.error(f"OTP verification error for user '{request.username}': {e}")
        raise HTTPException(status_code=500, detail="OTP verification failed.")


@app.post("/resend-otp")
def resend_otp(request: ResendOTPRequest):
    """Resend OTP to user's email."""
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
        logging.info(f"OTP resent to user '{user['username']}'.")
        return {"message": "OTP resent successfully"}
    except Exception as e:
        logging.error(f"Resend OTP error: {e}")
        raise HTTPException(status_code=500, detail="Resend OTP failed.")



@app.post("/login")
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

@app.post("/verify-login-otp")
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

@app.post("/logout")
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