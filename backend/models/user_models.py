from pydantic import BaseModel, EmailStr
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging



# LOGGER
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# pydantic models
class RegisterRequest(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class ResendOTPRequest(BaseModel):
    email: EmailStr

class LogoutRequest(BaseModel):
    email: EmailStr


class VerifyLoginOTPRequest(BaseModel):
    email: EmailStr
    otp: str




