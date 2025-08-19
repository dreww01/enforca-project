import secrets
import string

# FUNCTION TO GENERATE OTP FROM SECRETES MODULE
def generate_otp():
    num = string.digits
    OTP = ''.join(secrets.choice(num) for _ in range(6))
    return OTP