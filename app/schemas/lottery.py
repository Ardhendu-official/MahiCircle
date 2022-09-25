from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

class Lottery(BaseModel):
    lottery_user_id : Optional[int] = None 
    lottery_game_id : Optional[int] = None 
    lottery_number : Optional[list[str]] = None 
    lottery_game_name : Optional[str] = None 
    lottery_amount : Optional[str] = None 
    trans_transaction_id: Optional[str] = None
    transaction_status: Optional[str] = None
    transaction_type: Optional[str] = None
    transaction_amount: str

