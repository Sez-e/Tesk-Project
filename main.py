from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request

from auth.models import User
from auth.schemas import RegisterUserSchemaRequest
from auth.security import manager, pwd_context, limiter
from core.database import create_session
from post.endpoints import router as post_router # noqa

app = FastAPI(
    title="Test App"
)

app.include_router(post_router, prefix="/post", tags=["Posts",])


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@manager.user_loader()
def query_user(username: str):
    return create_session().query(User).filter(User.username == username).first()


@app.post("/register")
@limiter.limit("50/minute")
async def register(request: Request, user: RegisterUserSchemaRequest):
    db = create_session()
    existing_user = db.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User is already registered.")

    user.password = pwd_context.hash(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.id


@app.post("/login")
@limiter.limit("50/minute")
def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = query_user(username)
    if not user:
        raise InvalidCredentialsException
    elif not pwd_context.verify(password, user.password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": username})
    return {"access_token": access_token}


