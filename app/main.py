from fastapi import FastAPI, Depends, responses, status, Response, HTTPException
from sqlalchemy.orm.session import Session
from app.routes.index import customer, game, lottery
from app.config.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(login,tags=['Login'], include_in_schema=False)
app.include_router(customer,tags=['Customer'])
app.include_router(game,tags=['Game'])
app.include_router(lottery,tags=['Lottery'])
# app.include_router(otp,tags=['OTP'])
# app.include_router(user,tags=['User'], include_in_schema=False)
