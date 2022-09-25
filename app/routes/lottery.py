from fastapi import APIRouter, Depends, responses, status, Response, HTTPException
from sqlalchemy.orm.session import Session
from app.models.index import DbCustomer, DbGame, DbLottery
from app.schemas.index import Lottery
from app.config.database import SessionLocal, engine
from typing import List
import pytz
from datetime import datetime

from app.oprations.index import  lottery_genarete, verify_otp, show_all_game, create_new_lottery

lottery = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lottery.get('/lottery/{number}', status_code=status.HTTP_200_OK)
def lotteryGenarete(number: int, db: Session = Depends(get_db)):
    return lottery_genarete(number,db)

# @game.post('/opt/create', status_code=status.HTTP_201_CREATED)
# def createOtp(request: Game, db: Session = Depends(get_db)):
#     return create_new_otp(request,db)

# @game.post('/opt/verify', status_code=status.HTTP_201_CREATED)
# def verificationOtp(request: Game, db: Session = Depends(get_db)):
#     return verify_otp(request, db ) # type: ignore

@lottery.post('/lottery', status_code=status.HTTP_201_CREATED)
def createLottery(request: Lottery, db: Session = Depends(get_db)):
    return create_new_lottery(request, db)  


# @customer.get('/customer/wallet/{email}', status_code=status.HTTP_200_OK)
# def Customerwallet(email, db: Session = Depends(get_db)):
#     return show_cust_wallet_amount(email,db)


# @customer.post('/customer/wallet/addMoney/', status_code=status.HTTP_201_CREATED)
# def custAddMoney(request: CustomerAddMoney, db: Session = Depends(get_db)):
#     return customer_Add_Money(request,db)


# @customer.get('/pincode/finder/{pincode}')
# def all(pincode, db: Session = Depends(get_db)):  # type: ignore
#    return pincode_finder(pincode,db)

