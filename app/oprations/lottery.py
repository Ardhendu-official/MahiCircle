import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from pymysql import NULL
from sqlalchemy.orm.session import Session
from app.models.index import DbCustomer, DbWalletTransaction, DbPin, DbGame, DbLottery, DbTransaction
from app.schemas.index import Lottery
from app.config.database import SessionLocal, engine
from typing import List
import pytz
from datetime import datetime, timedelta
from app.functions.index import otpGenerate,otpVerify
import secrets
import requests
import time
import random, string



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_new_lottery(request: Lottery, db: Session = Depends(get_db)):
    cust = db.query(DbCustomer).filter(DbCustomer.cust_id == request.lottery_user_id).first()
    # if cust and cust.cust_phone_verified == "verify":
    # number = request.lottery_number.split(",") # type: ignore
    # amount= float(request.lottery_amount) / float(number.__len__()) # type: ignore
    if request.transaction_type == "wallet" and request.transaction_status == "Success":  
        if float(request.lottery_amount) <=  cust.cust_wallet :  # type: ignore
            new_trans = DbWalletTransaction(
                trans_transaction_id=request.trans_transaction_id,
                transaction_status=request.transaction_status,
                transaction_type=request.transaction_type,
                transaction_amount=request.transaction_amount,
                cust_id=request.lottery_user_id,
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta'))
            )
            db.add(new_trans)
            db.commit()
            update_bal = cust.cust_wallet - float(request.transaction_amount)   # type: ignore
            db.query(DbCustomer).filter(DbCustomer.cust_id == request.lottery_user_id).update({"cust_wallet": f'{update_bal}', "cust_wallet_balence_updation": datetime.now(
                                pytz.timezone('Asia/Calcutta'))}, synchronize_session='evaluate')
            db.commit()
            # recharge_happen = True
            for var in request.lottery_number:      # type: ignore
                new_lottery = DbLottery(
                    lottery_user_id = request.lottery_user_id,
                    lottery_game_id = request.lottery_game_id,
                    lottery_game_name = request.lottery_game_name,
                    lottery_number = var,  
                    lottery_registration_datce_time = datetime.now(pytz.timezone('Asia/Calcutta')),
                    lottery_amount = request.lottery_amount
                )
                db.add(new_lottery)
                db.commit()
            db.query(DbCustomer).filter(DbCustomer.cust_id == request.lottery_user_id).update({"cust_lottery_number": f'{request.lottery_number}', "cust_current_game_id": datetime.now(
                                pytz.timezone('Asia/Calcutta'))}, synchronize_session='evaluate')
            db.commit()
            return {'status': 'Success', 'msg': 'payment completed', 'details': 'New lottery Created', 'Creation Time': datetime.now(pytz.timezone('Asia/Calcutta'))}
            # return {'status': 'Success', 'details': 'payment completed'
        else:
            recharge_happen = False
            return {'status': 'Failed', 'details': 'inefficient wallet balence'}

    elif request.transaction_type == "online" and request.transaction_status == "Success":
        new_trans = DbTransaction(
            trans_transaction_id=request.trans_transaction_id,
            transaction_status=request.transaction_status,
            transaction_type=request.transaction_type,
            transaction_amount=request.transaction_amount,
            cust_id=request.lottery_user_id,
            transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta'))
        )
        db.add(new_trans)
        db.commit()
        for var in request.lottery_number:      # type: ignore
            new_lottery = DbLottery(
                lottery_user_id = request.lottery_user_id,
                lottery_game_id = request.lottery_game_id,
                lottery_game_name = request.lottery_game_name,
                lottery_number = var,  
                lottery_registration_datce_time = datetime.now(pytz.timezone('Asia/Calcutta')),
                lottery_amount = request.lottery_amount
            )
            db.add(new_lottery)
            db.commit()
        db.refresh(new_lottery)          # type: ignore

                # return number
        return {'status': 'Success', 'msg': 'payment completed', 'details': 'New lottery Created', 'Creation Time': datetime.now(pytz.timezone('Asia/Calcutta'))}

    else:
        return {'status': f'{request.transaction_status}', 'details': 'payment not completed'}

    # if recharge_happen:
    #     for var in number:
    #             new_lottery = DbLottery(
    #                 lottery_user_id = request.lottery_user_id,
    #                 lottery_game_id = request.lottery_game_id,
    #                 lottery_game_name = request.lottery_game_name,
    #                 lottery_number = var,  
    #                 lottery_registration_datce_time = datetime.now(pytz.timezone('Asia/Calcutta')),
    #                 lottery_amount = request.lottery_amount
    #             )
    #             db.add(new_lottery)
    #             db.commit()
    #     return {'status': 'Success', 'details': 'New lottery Created', 'Creation Time': datetime.now(pytz.timezone('Asia/Calcutta'))}
    # else:
    #         return {'status': 'Failed', 'details': 'lottery error'}

    # # db.refresh(new_lottery)
    # # return number.__len__()

#     # db.query(DbGame).filter(DbCustomer.cust_mobile == request.cust_mobile).update(old_cust.dict())
#     # else:
#     #     return {'status': 'Failed', 'details': 'customer is not available', 'message': '1st create a account using phone number'}
        

def lottery_genarete(number: int, db: Session = Depends(get_db)):
    lottery_number = []
    for _ in range(number):
        num = random.randint(111111,999999)
        alpha = ''.join("O"+random.choice(string.ascii_uppercase) for _ in range(1))
        code = alpha + str(num)
        lottery_number.append(code)
    return lottery_number















# for var in number:
        #     new_lottery = DbLottery(
        #         lottery_user_id = request.lottery_user_id,
        #         lottery_game_id = request.lottery_game_id,
        #         lottery_game_name = request.lottery_game_name,
        #         lottery_number = var,  
        #         lottery_registration_datce_time = datetime.now(pytz.timezone('Asia/Calcutta')),
        #         lottery_amount = amount
        #     )
        #     db.add(new_lottery)
        #     db.commit()