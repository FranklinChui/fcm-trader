from pydantic import BaseModel
from datetime import date

# Pydantic schema for Signal
class SignalBase(BaseModel):
    signal_type: str
    reason: str

class SignalCreate(SignalBase):
    instrument_id: int
    date: date

class Signal(SignalBase):
    id: int
    instrument_id: int
    date: date

    class Config:
        from_attributes = True
