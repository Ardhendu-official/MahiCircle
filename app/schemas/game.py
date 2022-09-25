from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

class Game(BaseModel):
    game_name : Optional[str] = None 
    game_image : Optional[str] = None
    game_end_date_time : Optional[datetime] = None
    game_unit_price : Optional[str] = None
    game_min_ticket_number : Optional[str] = None
    game_winner_price : Optional[int] = None

