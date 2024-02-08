from pydantic import BaseModel
from typing import Union

class Id(BaseModel):
    id: int

class Section(BaseModel):
    id: Union[int, None]
    name: str
    start_led: int
    end_led: int

class ColorSequence(BaseModel):
    id: Union[int, None]
    name: str
    description: str
    selection: int
    color_amount: int

class Color(BaseModel):
    id: Union[int, None]
    color_sequence_id: int
    position: Union[int, None]
    red: int
    green: int
    blue: int

class Animation(BaseModel):
    id: int
    name: str
    description: str
    variation: int
    direction: int
    
class Animate(BaseModel):
    color_sequence_id: int
    animation_id: int
    section_id: int

class Value(BaseModel):
    value: int
