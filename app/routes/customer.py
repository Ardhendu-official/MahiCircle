from fastapi import APIRouter, Depends, responses, status, Response, HTTPException
from sqlalchemy.orm.session import Session
from app.models.index import DbCustomer
from app.schemas.index import Customer, ShowCustomer, ReqCustomer, CustomerLogin, CustomerAddMoney, ReqPhone, verifyOtp
from app.config.database import SessionLocal, engine
from typing import List
import pytz
from datetime import datetime

from app.oprations.index import create_new_customer, create_new_otp, verify_otp, show_all_customer, customer_Add_Money, show_cust_wallet_amount

customer = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@customer.get('/customer/', status_code=status.HTTP_200_OK)
def allCustomer(db: Session = Depends(get_db)):
    return show_all_customer(db)

@customer.post('/opt/create', status_code=status.HTTP_201_CREATED)
def createOtp(request: ReqPhone, db: Session = Depends(get_db)):
    return create_new_otp(request,db)

@customer.post('/opt/verify', status_code=status.HTTP_201_CREATED)
def verificationOtp(request: verifyOtp, db: Session = Depends(get_db)):
    return verify_otp(request, db ) # type: ignore

@customer.post('/customer/auth', status_code=status.HTTP_201_CREATED)
def createCustomer(request: ReqCustomer, db: Session = Depends(get_db)):
    return create_new_customer(request,db)


@customer.get('/customer/wallet/{phone}', status_code=status.HTTP_200_OK)
def Customerwallet(phone: int, db: Session = Depends(get_db)):
    return show_cust_wallet_amount(phone,db)


@customer.post('/customer/wallet/addMoney/', status_code=status.HTTP_201_CREATED)
def custAddMoney(request: CustomerAddMoney, db: Session = Depends(get_db)):
    return customer_Add_Money(request,db)


# @customer.get('/pincode/finder/{pincode}')
# def all(pincode, db: Session = Depends(get_db)):  # type: ignore
#    return pincode_finder(pincode,db)

