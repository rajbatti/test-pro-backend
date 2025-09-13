from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError

from app.services import auth_service

app = FastAPI(title="Docx2HTML Converter API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import JSONResponse

@app.middleware("http")
async def verify_token(request: Request, call_next):
    if request.method == "OPTIONS" or request.url.path in ["/", "/api/auth/google", "/api/auth/test"]:
        return await call_next(request)

    token = request.cookies.get("access_token")
    if not token:
        response = await call_next(request)  # Process with next middleware to apply CORS
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or missing token"},
            headers=response.headers  # attach CORS headers
        )

    try:
        payload = auth_service.decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise JWTError("Invalid token payload")

        user = await auth_service.get_user_by_email(email)
        if user is None:
            raise JWTError("User not found")

        request.state.user = user
        response = await call_next(request)

        # Optional: refresh token logic here

        return response

    except JWTError:
        response = await call_next(request)
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid token"},
            headers=response.headers  # attach CORS headers
        )



# Include routers after middleware setup
from app.routes import auth, tests
from app.services import questions_service

app.include_router(questions_service.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(tests.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Docx2HTML Converter API running"}
