from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(email: str, password: str):
    return {
        "message": "Login API is working",
        "email": email,
        "status": "success"
    }