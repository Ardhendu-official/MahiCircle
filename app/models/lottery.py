import datetime
from sqlalchemy.orm import relationship
from app.config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey

from app.models.index import DbCustomer, DbGame

class DbLottery(Base):
    __tablename__ = 'lottery'
    lottery_id = Column(Integer, primary_key=True, autoincrement=True)
    lottery_user_id = Column(Integer, ForeignKey(DbCustomer.cust_id))
    lottery_game_id = Column(Integer, ForeignKey(DbGame.game_id))
    lottery_game_name = Column(String(255))
    lottery_number = Column(Text(4294000000))
    lottery_registration_datce_time = Column(DateTime)
    lottery_amount = Column(Float, default=0, nullable=False)
    lottery_wallet_balence_updation = Column(DateTime)

    cust_id_constraint = relationship(
        "DbCustomer", cascade="all,delete", backref="lottery")

    game_id_constraint = relationship(
        "DbGame", cascade="all,delete", backref="lottery")