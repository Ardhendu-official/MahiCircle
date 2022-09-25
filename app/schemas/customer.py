from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional
from fastapi import UploadFile, File

class Customer(BaseModel):
    cust_fname: str
    cust_lname: str
    cust_email: str
    cust_mobile: str
    cust_registration_date_time: Optional[datetime] = None
    cust_last_login_date_time: Optional[datetime] = None

class ReqPhone(BaseModel):
    cust_mobile: Optional[str] = None

class verifyOtp(BaseModel):
    cust_mobile: str
    otp_code: str

    class Config:
        orm_mode = True


class ReqextcustOtp(BaseModel):
    otp_creation_datetime :Optional[datetime] = None
    otp_valid_time :Optional[time] = None
    otp_code:Optional[str] = None

class CustomerLogin(BaseModel):
    cust_fname: str
    cust_lname: str
    cust_email: str
    cust_address: Optional[str]
    cust_image: Optional[str]
    cust_user_id: Optional[str]
    cust_wallet: float
    cust_last_login_date_time: Optional[datetime] = None

class ReqCustomer(BaseModel):
    cust_fname: str
    cust_lname: str
    cust_email: str
    cust_mobile: str
    cust_address: Optional[str]
    cust_image: Optional[str]

class ShowCustomer(BaseModel):
    cust_user_id: str
    cust_fname: str
    cust_lname: str
    cust_email: str
    cust_mobile: str
    cust_image: Optional[str]

    class Config:
        orm_mode = True


class CustomerAddMoney(BaseModel):
    cust_mobile : str
    transaction_amount: float
    transaction_status: str
    trans_transaction_id: str

