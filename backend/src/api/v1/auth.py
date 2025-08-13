from api.v1.docs.auth_docs import login_docs, signup_docs
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", **signup_docs)
async def signup():
    # Logic for user signup
    return {"message": "User signed up successfully"}


@router.post("/login", **login_docs)
async def login():
    return {"message": "User logged in successfully"}
