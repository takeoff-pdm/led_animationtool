from pydantic import BaseModel


class Id(BaseModel):
    id: int


class Section(BaseModel):
    id: int | None = None
    name: str
    start_led: int
    end_led: int


class ColorSequence(BaseModel):
    id: int | None = None
    name: str
    description: str
    selection: int
    color_amount: int


class Color(BaseModel):
    id: int | None = None
    color_sequence_id: int
    position: int | None = None
    red: int
    green: int
    blue: int


class Animation(BaseModel):
    id: int
    section_id: int | None = None
    name: str
    description: str
    variation: int
    direction: int
    offset: int


class Animate(BaseModel):
    color_sequence_id: int
    animation_id: int
    section_id: int


class SectionAnimation(BaseModel):
    section_id: int
    animation_id: int


class Value(BaseModel):
    value: int
