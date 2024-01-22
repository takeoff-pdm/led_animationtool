from uvicorn import run as run_api
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Union

from util.database.database import Database
from util.database.section import fetch_sections, fetch_section
from util.database.color_sequence import fetch_color_sequences, fetch_color_sequence
from util.database.color import fetch_colors, fetch_colors_from_sequence, fetch_color
from util.database.animation import fetch_animations, fetch_animation

from section import Section
from color_sequence import ColorSequence
from color import Color
from strip import Strip

app = FastAPI()
database = Database()
strip = Strip()

class Name(BaseModel):
    name: str


class Section(BaseModel):
    old_name: Union[str, None]
    name: str
    start_led: int
    end_led: int


class Color(BaseModel):
    color_sequence: str
    position: int


# API
# Section
@app.get('/api/get/sections', response_class=JSONResponse)
async def get_sections():
    return { 'sections': fetch_sections()}

@app.get('/api/get/section', response_class=JSONResponse)
async def get_section(name: Name):
    return { 'section': fetch_section(name.name)}

@app.post('/api/add/section', response_class=JSONResponse)
async def add_section(section: Section):
    if not strip.add_section(section.name, section.start_led, section.end_led):
        return { 'success': False }
    
    return { 'success': True }

@app.post('/api/remove/section', response_class=JSONResponse)
async def remove_section(name: Name):
    if not strip.remove_section(name.name):
        return { 'success': False }
    
    return { 'success': True }

@app.post('/api/update/section', response_class=JSONResponse)
async def update_section(section: Section):
    if not strip.update_section(section.old_name, section.name, section.start_led, section.end_led):
        return { 'success': False }
    
    return { 'success': True }

# Color Sequence
@app.get('/api/get/color_sequences', response_class=JSONResponse)
async def get_color_sequences():
    return fetch_color_sequence()

@app.get('/api/get/color_sequence', response_class=JSONResponse)
async def get_color_sequence(name: Name):
    return fetch_color_sequence(name.name)

# Color
@app.get('/api/get/colors', response_class=JSONResponse)
async def get_colors():
    return fetch_colors()

@app.get('/api/get/colors_from_sequence', response_class=JSONResponse)
async def get_colors_from_sequence(name: Name):  # name is color-sequence
    return fetch_colors_from_sequence(name.name)

@app.get('/api/get/color', response_class=JSONResponse)
async def get_color(color: Color):
    return fetch_color(color.color_sequence, color.position)

# Animation
@app.get('/api/get/animations', response_class=JSONResponse)
async def get_animations():
    return fetch_animations

@app.get('/api/get/animation', response_class=JSONResponse)
async def get_animation(name: Name):
    return fetch_animation(name.name)

# Settings
@app.get('/api/get/settings', response_class=JSONResponse)
async def get_settings():
    return strip.fetch_config()

def main():
    run_api("main:app", host='0.0.0.0', port=8000, log_level="info")

if __name__ == "__main__":
    main()
