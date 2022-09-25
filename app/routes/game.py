from fastapi import APIRouter, Depends, responses, status, Response, HTTPException
from sqlalchemy.orm.session import Session
from app.models.index import DbCustomer, DbGame
from app.schemas.index import Game
from app.config.database import SessionLocal, engine
from typing import List
import pytz
from datetime import datetime

from app.oprations.index import create_new_game, create_new_otp, verify_otp, show_all_game

game = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@game.get('/game/', status_code=status.HTTP_200_OK)
def allGame(db: Session = Depends(get_db)):
    return show_all_game(db)

# @game.post('/opt/create', status_code=status.HTTP_201_CREATED)
# def createOtp(request: Game, db: Session = Depends(get_db)):
#     return create_new_otp(request,db)

# @game.post('/opt/verify', status_code=status.HTTP_201_CREATED)
# def verificationOtp(request: Game, db: Session = Depends(get_db)):
#     return verify_otp(request, db ) # type: ignore

@game.post('/game', status_code=status.HTTP_201_CREATED)
def createGame(request: Game, db: Session = Depends(get_db)):
    return create_new_game(request, db)  


# @customer.get('/customer/wallet/{email}', status_code=status.HTTP_200_OK)
# def Customerwallet(email, db: Session = Depends(get_db)):
#     return show_cust_wallet_amount(email,db)


# @customer.post('/customer/wallet/addMoney/', status_code=status.HTTP_201_CREATED)
# def custAddMoney(request: CustomerAddMoney, db: Session = Depends(get_db)):
#     return customer_Add_Money(request,db)


# @customer.get('/pincode/finder/{pincode}')
# def all(pincode, db: Session = Depends(get_db)):  # type: ignore
#    return pincode_finder(pincode,db)

