from datetime import datetime
from app.config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Time, true

class DbCustomer(Base):
    __tablename__ = 'customer'
    cust_id = Column(Integer, primary_key=True, autoincrement=True)
    otp_code = Column(String(255), nullable=True)
    otp_creation_datetime = Column(DateTime, nullable=True)
    otp_valid_time = Column(DateTime, nullable=True)
    cust_user_id = Column(String(255))
    cust_phone_verified = Column(String(255))
    cust_fname = Column(String(255))
    cust_lname = Column(String(255))
    cust_mobile = Column(String(255))
    cust_email = Column(String(255))
    cust_image = Column(String(255), default=0, nullable=False)
    cust_address = Column(Text(4294000000))
    cust_registration_date_time = Column(DateTime)
    cust_last_login_date_time = Column(DateTime)
    cust_wallet = Column(Float, default=0, nullable=False)
    cust_wallet_balence_updation = Column(DateTime)
    cust_UPI_id = Column(String(255))
    cust_current_game_id = Column(String(255))
    cust_game_history = Column(String(255))
    cust_lottery_number = Column(String(255))
    