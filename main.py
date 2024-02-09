from uvicorn import run as run_api
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from util.api.models import Id, Section, ColorSequence, Color, Animation, Value

from util.database.database import Database
from util.database.section import fetch_sections, fetch_section
from util.database.color_sequence import fetch_color_sequences, fetch_color_sequence
from util.database.color import fetch_colors, fetch_colors_from_sequence, fetch_color
from util.database.animation import fetch_animations, fetch_animation, update_animation, add_animation, remove_animation

from section import Section
from color_sequence import ColorSequence
from strip import Strip

app = FastAPI()
database = Database()
strip = Strip()

# API
# Section
@app.get('/api/get/sections', response_class=JSONResponse)
async def get_sections():
    return { 'sections': fetch_sections()}

@app.get('/api/get/section', response_class=JSONResponse)
async def get_section(id: Id):
    return { 'section': fetch_section(id.id)}

@app.post('/api/add/section', response_class=JSONResponse)
async def add_section(section: Section):
    return { 'success': strip.add_section(section.name, section.start_led, section.end_led) }

@app.post('/api/remove/section', response_class=JSONResponse)
async def remove_section(id: Id):
    return { 'success': strip.remove_section(id.id) }

@app.post('/api/update/section', response_class=JSONResponse)
async def update_section(section: Section):
    return { 'success': strip.update_section(section.id, section.name, 
                                             section.start_led, section.end_led) }

# Color Sequence
@app.get('/api/get/color_sequences', response_class=JSONResponse)
async def get_color_sequences():
    return { 'color_sequences': fetch_color_sequences() }

@app.get('/api/get/color_sequence', response_class=JSONResponse)
async def get_color_sequence(id: Id):
    return { 'color_sequence': fetch_color_sequence(id.id) }

@app.post('/api/add/color_sequence', response_class=JSONResponse)
async def add_color_sequence(color_sequence: ColorSequence):
    return { 'success': strip.add_color_sequence(color_sequence.name, color_sequence.description, 
                                                 color_sequence.selection, color_sequence.color_amount) }

@app.post('/api/remove/color_sequence', response_class=JSONResponse)
async def remove_color_sequence(id: Id):
    # Remove all colors of given sequence
    for color in fetch_colors_from_sequence(id.id):
        if not strip.remove_color(color['id']):
            return { 'success': False }
    
    return { 'success': strip.remove_color_sequence(id.id) }

@app.post('/api/update/color_sequence', response_class=JSONResponse)
async def update_color_sequence(color_sequence: ColorSequence):
    return { 'success': strip.update_color_sequence(color_sequence.id, color_sequence.name, 
                                                    color_sequence.description, color_sequence.selection, 
                                                    color_sequence.color_amount) }

# Color
@app.get('/api/get/colors', response_class=JSONResponse)
async def get_colors():
    return { 'colors': fetch_colors() }

@app.get('/api/get/colors_from_sequence', response_class=JSONResponse)
async def get_colors_from_sequence(id: Id): # Id from color_sequence
    return { 'colors': fetch_colors_from_sequence(id.id) }

@app.get('/api/get/color', response_class=JSONResponse)
async def get_color(id: Id):
    return { 'color': fetch_color(id.id) }

@app.get('/api/add/color', response_class=JSONResponse)
async def add_color(color: Color):
    return { 'success': strip.add_color(color.id, color.color_sequence_id, color.red, color.green, color.blue) }

@app.get('/api/remove/color', response_class=JSONResponse)
async def remove_color(id: Id):
    return { 'success': strip.remove_color(id.id) }

@app.get('/api/update/color', response_class=JSONResponse)
async def update_color(color: Color):
    return { 'success': strip.update_color(color) } 

# Animation
@app.get('/api/get/animations', response_class=JSONResponse)
async def get_animations():
    return { 'animations': fetch_animations() }

@app.get('/api/get/animation', response_class=JSONResponse)
async def get_animation(id: Id):
    return { 'animation': fetch_animation(id.id) }

@app.post('/api/update/animation', response_class=JSONResponse)
async def update_anim(animation: Animation):
    if not fetch_animation(animation.id):
        return { 'success': False }
    
    return { 'success': update_animation(animation.id, animation.name, animation.description, 
                                         animation.variation, animation.direction) }

@app.post('/api/animate/start', response_class=JSONResponse)
async def animate_section(animate: Animate):
    return { 'success': strip.start_animate(color_sequence_id=animate.color_sequence_id, 
                                            animation_name=animate.id, section_id=animate.section_id) }
    
@app.post('/api/animate/stop', response_class=JSONResponse)
async def stop_animate_section(id: Id):
    return { 'success': strip.stop_animate(id.id) }

# Settings
@app.get('/api/get/settings', response_class=JSONResponse)
async def get_settings():
    return strip.fetch_config()

@app.post('/api/update/brightness', response_class=JSONResponse)
async def update_brightness(brightness: Value):
    return { 'success': strip.set_brightness(brightness.value) }

@app.post('/api/update/led-count', response_class=JSONResponse)
async def update_led_count(led_count: Value):
    return { 'success': strip.set_led_count(led_count.value) }

@app.post('/api/update/bpm', response_class=JSONResponse)
async def update_bpm(bpm: Value):
    return { 'success': strip.set_bpm(bpm.value) }

def main():
    run_api("main:app", host='0.0.0.0', port=8000, log_level="info")

if __name__ == "__main__":
    main()
