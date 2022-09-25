import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from pymysql import NULL
from sqlalchemy.orm.session import Session
from app.models.index import DbCustomer, DbWalletTransaction, DbPin
from app.schemas.index import ReqCustomer, CustomerLogin, CustomerAddMoney, ReqPhone, verifyOtp, ReqextcustOtp
from app.config.database import SessionLocal, engine
from typing import List
import pytz
from datetime import datetime, timedelta
from app.functions.index import otpGenerate,otpVerify
import secrets
import requests
import time
import random


category = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_new_otp(request: ReqPhone, db: Session = Depends(get_db)):
    cust = db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).first()
    otp_valid_datetime = datetime.now(pytz.timezone('Asia/Calcutta'))+ timedelta(minutes=1)
    # # datetime_object = otp_valid_date1time + timedelta(minutes=10)
    len= request.cust_mobile.__len__()    # type: ignore
    if len == 10:
        if not cust:
            new_cust = DbCustomer(
                    cust_mobile=request.cust_mobile,
                    otp_creation_datetime=datetime.now(pytz.timezone('Asia/Calcutta')),
                    otp_valid_time = otp_valid_datetime,
                    otp_code = 111111,
                    # otp_code = otpGenerate.otpcreate(),
                    cust_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                )
            db.add(new_cust)
            db.commit()
            return {'status': 'Success', 'details': 'new user Create and otp send'}
        else:
            otp_code = 111111
            # otp_code = otpGenerate.otpcreate()
            db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).update({"otp_valid_time": f'{otp_valid_datetime}', "otp_creation_datetime": datetime.now(
                                    pytz.timezone('Asia/Calcutta')), "otp_code": f'{otp_code}'}, synchronize_session='evaluate')
            db.commit()
        return {'status': 'Success', 'details': 'otp send'}
    else:
        return {'status': 'Failed', 'details': 'incorrect number'}

    # return len
    # return  otp_valid_date1time

def verify_otp(request: verifyOtp, db: Session = Depends(get_db)):
    cust = db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).first()
    now_datetime = datetime.now(pytz.timezone('Asia/Calcutta'))
    if str(now_datetime) <= str(cust.otp_valid_time):  # type: ignore
        if not cust:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"customer is not available")
        elif not cust.otp_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"otp is not available")
        else:
            otp = otpVerify.otp_verify(request.otp_code,cust.otp_code)  # type: ignore
            if otp == "true":
                db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).update({"otp_valid_time": None,"cust_phone_verified": f'{"verify"}', "otp_creation_datetime": None, "otp_code": None}, synchronize_session='evaluate')
                db.commit()
                user = db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).first()
                return user
            elif otp == "otp is not available":
                return {'status': 'Failed', 'details': 'otp is not available'}
            else:
                return {'status': 'Failed', 'details': 'worng otp'}
    else:
        db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).update({"otp_valid_time": None, "otp_creation_datetime": None, "otp_code": None}, synchronize_session='evaluate')
        db.commit()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"otp is not available")
        

def create_new_customer(request: ReqCustomer, db: Session = Depends(get_db)):
    cust = db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).first()
    if cust and cust.cust_phone_verified == "verify":
        old_cust = CustomerLogin(
            cust_user_id='MC'+uuid.uuid1().hex[:8],  # type: ignore
            cust_fname=request.cust_fname,
            cust_lname=request.cust_lname,
            cust_email= request.cust_email,
            cust_image=request.cust_image,  # type: ignore
            cust_address=request.cust_address,  # type: ignore
            cust_wallet = 0.00,
            cust_last_login_date_time=datetime.now(pytz.timezone('Asia/Calcutta'))
        )
        db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).update(old_cust.dict())
        db.commit()
        return {'status': 'Success', 'details': 'Login SUccessfully', 'Last Login Time': datetime.now(pytz.timezone('Asia/Calcutta'))}
    else:
        return {'status': 'Failed', 'details': 'customer is not available', 'message': '1st create a account using phone number'}
        

    # db.commit()
    # return {'status': 'Success', 'details': 'Login SUccessfully', 'Last Login Time': datetime.now(pytz.timezone('Asia/Calcutta'))}

def show_all_customer(db: Session = Depends(get_db)):
    customer = db.query(DbCustomer).all()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"customer is not available")
    else:
        return customer

def customer_Add_Money(request: CustomerAddMoney, db: Session = Depends(get_db)):
    cust = db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).first()
    if not cust:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with the mobile number {request.cust_mobile} is not available")
    else:
        new_trans = DbWalletTransaction(
            cust_id=cust.cust_id,
            transaction_amount=request.transaction_amount,
            transaction_status=request.transaction_status,
            trans_transaction_id=request.trans_transaction_id,
            transaction_date_time=datetime.now(pytz.timezone('Asia/Calcutta'))
        )
        db.add(new_trans)
        db.commit()
        db.refresh(new_trans)
        if request.transaction_status == 'success':
            wallet = cust.cust_wallet
            cust_updated_bal = wallet+request.transaction_amount  # type: ignore 
            db.query(DbCustomer).filter(DbCustomer.cust_mobile == request.cust_mobile).update({"cust_wallet": f'{cust_updated_bal}', "cust_wallet_balence_updation": datetime.now(
                        pytz.timezone('Asia/Calcutta'))}, synchronize_session='evaluate')
            db.commit()

            return {'status': request.transaction_status, 'balence': round(cust_updated_bal, 2)}
        else:
            return {'status': request.transaction_status, 'balence': round(cust.cust_wallet, 2)}

def show_cust_wallet_amount(phone: int , db: Session = Depends(get_db)):
    user = db.query(DbCustomer).filter(DbCustomer.cust_mobile == phone).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with the phone {phone} is not available")     
    else:
        return {'status': 'Success', 'amount': round(user.cust_wallet, 2)}








# def create_customer_address(request: CustomerAddress, db: Session = Depends(get_db)):
#     user = db.query(DbCustomer).filter(DbCustomer.cust_email == request.cust_email).first()

#     if not user.cust_address:
#         all_address_str=''
#         all_address_str_billing = '0,'+request.fullname+','+request.mobile+','+request.pin_code+','+request.house_no+','+request.area+','+request.landmark+','+request.city+','+request.state+',india'
#         all_address_str_shipping = '1,'+request.fullname+','+request.mobile+','+request.pin_code+','+request.house_no+','+request.area+','+request.landmark+','+request.city+','+request.state+',india'
#         all_address_str = all_address_str_billing+';'+ all_address_str_shipping
#         db.query(DbCustomer).filter(DbCustomer.cust_email == request.cust_email).update({DbCustomer.cust_address: all_address_str, DbCustomer.cust_default_address_number:1})
#     else:
#         all_prev_add = user.cust_address.split(";")
#         last_prev_add = all_prev_add[-1]
#         prev_add = last_prev_add.split(",")
#         last_add_id = int(prev_add[0])
#         last_add_id = last_add_id + 1
#         all_address_str=''
#         all_address_str = str(last_add_id)+','+request.fullname+','+request.mobile+','+request.pin_code+','+request.house_no+','+request.area+','+request.landmark+','+request.city+','+request.state+',india'
#         all_address_str = user.cust_address+';'+ all_address_str
#         db.query(DbCustomer).filter(DbCustomer.cust_email == request.cust_email).update({DbCustomer.cust_address: all_address_str})

#     db.commit()
#     return {'status': 'Success', 'details': 'Address Added Successfully'}

# def update_customer_address(request: CustomerAddressUpdate, db: Session = Depends(get_db)):
#     user = db.query(DbCustomer).filter(DbCustomer.cust_email == request.cust_email).first()
    
#     all_prev_add = user.cust_address.split(";")
#     for last_prev_add in all_prev_add:
#         prev_add = last_prev_add.split(",")
#         if prev_add[0] == request.address_id:
#             all_prev_add.pop(str(request.address_id))
#             address = str(request.address_id)+','+request.fullname+','+request.mobile+','+request.pin_code+','+request.house_no+','+request.area+','+request.landmark+','+request.city+','+request.state+',india'+";"
#             all_prev_add.insert(request.address_id, address)
#             break

#         final_address= ''
#     for final_add in all_prev_add:
#         final_address = final_address+final_add+";"


#         db.query(DbCustomer).filter(DbCustomer.cust_email == request.cust_email).update({DbCustomer.cust_address: final_address})
#         db.commit()
#     return last_prev_add
#     # return {'status': 'Success', 'details': 'Address Updated Successfully',}

# def show_all_cust_address(email: str, db: Session = Depends(get_db)):
#     user = db.query(DbCustomer).filter(DbCustomer.cust_email == email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"User with the email {email} is not available")
#     elif not user.cust_address:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"User Address with the email {email} is not available")       
#     else:
#         all_add = user.cust_address.split(";")
#         all_add.pop(0)
#         final_address = []
#         for all_ad in all_add:
#             ad = all_ad.split(",")
#             address = {
#                 'address_id': ad[0],
#                 'fullname': ad[1],
#                 'mobile': ad[2],
#                 'pin_code': ad[3],
#                 'house_no': ad[4],
#                 'area': ad[5],
#                 'landmark': ad[6],
#                 'city': ad[7],
#                 'state': ad[8],
#                 'country': ad[9]
#             }
#             final_address.append(address)
            
#         return final_address

# def show_cust_wallet_amount(email, db: Session = Depends(get_db)):
#     user = db.query(DbCustomer).filter(DbCustomer.cust_email == email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"Customer with the gmail {email} is not available")     
#     else:
#         return {'status': 'Success', 'amount': round(user.cust_wallet, 2)}

# def fatch_all_recharge(email,db: Session = Depends(get_db)):
#     user = db.query(DbCustomer).filter(DbCustomer.cust_email == email).first()
#     all_mobile_transaction = db.query(DbRechargeTransaction).filter(DbRechargeTransaction.cust_id == user.cust_id).order_by(DbRechargeTransaction.transaction_id.desc()).all()

#     all_mobile_transaction_data = []

#     for mobile_transaction in all_mobile_transaction:

#         cust_details = db.query(DbCustomer).filter(DbCustomer.cust_id == mobile_transaction.cust_id).first()

#         opr_details = db.query(DbRechargeOperator).filter(DbRechargeOperator.opr_id == mobile_transaction.trans_operator_id).first()

#         final_data = {
#         "trans_txn_id": mobile_transaction.trans_txn_id,
#         "trans_mobile_or_dth": mobile_transaction.trans_mobile_or_dth,
#         "trans_recharge_status": mobile_transaction.trans_recharge_status,
#         "transaction_status": mobile_transaction.transaction_status,
#         "trans_zone_name": mobile_transaction.trans_zone_name,
#         "transaction_date_time": mobile_transaction.transaction_date_time,
#         "transaction_mode": mobile_transaction.transaction_mode,
#         "trans_operator_id": {
#             "opr_operator_name": opr_details.opr_operator_name,
#             "opr_operator_type": opr_details.opr_operator_type,
#             "opr_operator_image": opr_details.opr_operator_image,
#             "opr_operator_short_name": opr_details.opr_operator_short_name,
#             "opr_id": opr_details.opr_id,
#             "opr_operator_commission": opr_details.opr_operator_commission},
#         "cust_id": {
#             "cust_image": cust_details.cust_image,
#             "cust_user_id": cust_details.cust_user_id,
#             "cust_id": cust_details. cust_id,
#             "cust_wallet": cust_details.cust_wallet,
#             "cust_fname": cust_details.cust_fname,
#             "cust_lname": cust_details.cust_lname,
#             "cust_mobile": cust_details.cust_mobile,
#             "cust_email_verified": cust_details.cust_email_verified,
#             "cust_email": cust_details.cust_email,
#             "cust_recharge_amount_mobile": cust_details.cust_recharge_amount_mobile},
#         "wallet_opening_balence": mobile_transaction.wallet_opening_balence,
#         "transaction_amount": mobile_transaction.transaction_amount,
#         "wallet_debit": mobile_transaction.wallet_debit,
#         "trans_transaction_id": mobile_transaction.trans_transaction_id,
#         "transaction_wallet_amount": mobile_transaction.transaction_wallet_amount,
#         "wallet_closing_balence": mobile_transaction.wallet_closing_balence,
#         "transaction_id": mobile_transaction.transaction_id,
#         "transaction_online_amount": mobile_transaction.transaction_online_amount,
#         "wallet_cashback_ammount": mobile_transaction.wallet_cashback_ammount,
#         "trans_mobile_dth_number": mobile_transaction.trans_mobile_dth_number,
#         "trans_recharge_txn_id": mobile_transaction.trans_recharge_txn_id
#         }

#         all_mobile_transaction_data.append(final_data)

#     if not all_mobile_transaction_data:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                              detail=f"No Data Found")
#     else:
#         return all_mobile_transaction_data

# def customer_Add_Money(request: CustomerAddMoney, db: Session = Depends(get_db)):
#     cust = db.query(DbCustomer).filter(DbCustomer.cust_email == request.cust_email).first()
#     if not cust:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"Customer with the gmail {request.cust_email} is not available")
#     else:
#         new_trans = DbWalletTransaction(
#             cust_id=cust.cust_id,
#             transaction_amount=request.transaction_amount,
#             transaction_status=request.transaction_status,
#             trans_transaction_id=request.trans_transaction_id,
#             transaction_date_time=datetime.now(pytz.timezone('Asia/Calcutta'))
#         )
#         db.add(new_trans)
#         db.commit()
#         db.refresh(new_trans)
#         if request.transaction_status == 'success':
#             wallet = cust.cust_wallet
#             cust_updated_bal = wallet+request.transaction_amount
#             db.query(DbCustomer).filter(DbCustomer.cust_email == request.cust_email).update({"cust_wallet": f'{cust_updated_bal}', "cust_wallet_balence_updation": datetime.now(
#                         pytz.timezone('Asia/Calcutta'))}, synchronize_session='evaluate')
#             db.commit()

#             return {'status': request.transaction_status, 'balence': round(cust_updated_bal, 2)}
#         else:
#             return {'status': request.transaction_status, 'balence': round(cust.cust_wallet, 2)}

# def pincode_finder(pincode, db: Session = Depends(get_db)):
#     url= 'https://api.postalpincode.in/pincode/'+pincode
    
#     response = requests.get(url).json()

#     store = db.query(DbPin).filter(DbPin.pincode_code == pincode).first()

#     data = {
#         'status' : 'success',
#         'name' : response[0]['PostOffice'][0]['Name'],
#         'stored': True if store else False
#     }
    
#     return data

