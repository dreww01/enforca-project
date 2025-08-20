# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import logging

# routers
from routes.login import router as login_router
from routes.register import router as register_router
from routes.logout import router as logout_router
from routes.logout import router as resend_router


app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(login_router)
app.include_router(register_router)
app.include_router(logout_router)
app.include_router(resend_router)

# root
@app.get("/")
async def root():
    return {"message": "WELCOME TO MY AUTHENTICATION SERVER!"}


# validation Error handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation error: {exc.errors()} | Body: {exc.body}")
    
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid input. Please check your data, and put the correct data."}
    )