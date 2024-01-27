from pydantic import BaseModel
from typing import Union

class Name(BaseModel):
    name: str

class Section(BaseModel):
    old_name: Union[str, None]
    name: str
    start_led: int
    end_led: int

class ColorSequence(BaseModel):
    old_name: Union[str, None]
    name: str
    description: str
    selection: int
    color_amount: int

class Color(BaseModel):
    color_sequence: str
    position: int

class Animation(BaseModel):
    name: str
    variation: int
    direction: int

class FullAnimation(BaseModel):
    name: str
    description: str
    variation: int
    direction: int

class Value(BaseModel):
    value: int
