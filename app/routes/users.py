from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserCreate
from app.auth import get_password_hash, verify_password, create_access_token
from app.models import users
from app.database import database
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register")
async def register_user(user: UserCreate):
    existing = await database.fetch_one(users.select().where(users.c.username == user.username))
    if existing:
        raise HTTPException(status_code=400, detail="Username exists")
    hashed_pw = get_password_hash(user.password)
    query = users.insert().values(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_pw
    )
    await database.execute(query)
    return {"msg": "User registered"}

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    query = users.select().where(users.c.username == form.username)
    user = await database.fetch_one(query)
    if not user or not verify_password(form.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}
