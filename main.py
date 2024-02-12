from uvicorn import run as run_api
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from util.api.models import Id, Section, ColorSequence, Color, Animation, Animate, Value

from util.database.database import Database
from util.database.section import fetch_sections, fetch_section
from util.database.color_sequence import fetch_color_sequences, fetch_color_sequence
from util.database.color import fetch_colors, fetch_colors_from_sequence, fetch_color
from util.database.animation import fetch_animations, fetch_animation, update_animation, add_animation, remove_animation

from strip import Strip

app = FastAPI()
database = Database()
strip = Strip()

# API
# Section
@app.get('/api/get/sections')
async def get_sections():
    return JSONResponse(content={ 'sections': fetch_sections()})

@app.get('/api/get/section')
async def get_section(id: Id):
    return JSONResponse(content={ 'section': fetch_section(id.id)})

@app.post('/api/add/section')
async def add_section(section: Section):
    return JSONResponse(content={ 'success': strip.add_section(section.name, section.start_led, section.end_led) })

@app.post('/api/remove/section')
async def remove_section(id: Id):
    return JSONResponse(content={ 'success': strip.remove_section(id.id) })

@app.post('/api/update/section')
async def update_section(section: Section):
    return JSONResponse(content={ 'success': strip.update_section(section.id, section.name, 
                                             section.start_led, section.end_led) })

# Color Sequence
@app.get('/api/get/color_sequences')
async def get_color_sequences():
    return JSONResponse(content={ 'color_sequences': fetch_color_sequences() })

@app.get('/api/get/color_sequence')
async def get_color_sequence(id: Id):
    return JSONResponse(content={ 'color_sequence': fetch_color_sequence(id.id) })

@app.post('/api/add/color_sequence')
async def add_color_sequence(color_sequence: ColorSequence):
    return JSONResponse(content={ 'success': strip.add_color_sequence(color_sequence.name, color_sequence.description, 
                                                 color_sequence.selection, color_sequence.color_amount) })

@app.post('/api/remove/color_sequence')
async def remove_color_sequence(id: Id):
    # Remove all colors of given sequence
    colors = fetch_colors_from_sequence(id.id)
    
    if colors:
        for color in colors:
            if not strip.remove_color(color['id']):
                return JSONResponse(content={ 'success': False })
    
    return JSONResponse(content={ 'success': strip.remove_color_sequence(id.id) })

@app.post('/api/update/color_sequence')
async def update_color_sequence(color_sequence: ColorSequence):
    return JSONResponse(content={ 'success': strip.update_color_sequence(color_sequence.id, color_sequence.name, 
                                                    color_sequence.description, color_sequence.selection, 
                                                    color_sequence.color_amount) })

# Color
@app.get('/api/get/colors')
async def get_colors():
    return JSONResponse(content={ 'colors': fetch_colors() })

@app.get('/api/get/colors_from_sequence')
async def get_colors_from_sequence(id: Id): # Id from color_sequence
    return JSONResponse(content={ 'colors': fetch_colors_from_sequence(id.id) })

@app.get('/api/get/color')
async def get_color(id: Id):
    return JSONResponse(content={ 'color': fetch_color(id.id) })

@app.post('/api/add/color')
async def add_color(color: Color):
    return JSONResponse(content={ 'success': strip.add_color(color.color_sequence_id, color.red, color.green, color.blue) })

@app.post('/api/remove/color')
async def remove_color(id: Id):
    return JSONResponse(content={ 'success': strip.remove_color(id.id) })

@app.post('/api/update/color')
async def update_color(color: Color):
    return JSONResponse(content={ 'success': strip.update_color(color) } )

# Animation
@app.get('/api/get/animations')
async def get_animations():
    return JSONResponse(content={ 'animations': fetch_animations() })

@app.get('/api/get/animation')
async def get_animation(id: Id):
    return JSONResponse(content={ 'animation': fetch_animation(id.id) })

@app.post('/api/update/animation')
async def update_anim(animation: Animation):
    if not fetch_animation(animation.id):
        return JSONResponse(content={ 'success': False })
    
    return JSONResponse(content={ 'success': update_animation(animation.id, animation.name, animation.description, 
                                         animation.variation, animation.direction) })

@app.post('/api/animate/start')
async def animate_section(animate: Animate):
    return JSONResponse(content={ 'success': strip.start_animate(color_sequence_id=animate.color_sequence_id, 
                                            animation_id=animate.animation_id, section_id=animate.section_id) })
    
@app.post('/api/animate/stop')
async def stop_animate_section(id: Id):
    return JSONResponse(content={ 'success': strip.stop_animate(id.id) })

# Settings
@app.get('/api/get/settings')
async def get_settings():
    return JSONResponse(content=strip.fetch_config())

@app.post('/api/update/brightness')
async def update_brightness(brightness: Value):
    return JSONResponse(content={ 'success': strip.set_brightness(brightness.value) })

@app.post('/api/update/led-count')
async def update_led_count(led_count: Value):
    return JSONResponse(content={ 'success': strip.set_led_count(led_count.value) })

@app.post('/api/update/bpm')
async def update_bpm(bpm: Value):
    return JSONResponse(content={ 'success': strip.set_bpm(bpm.value) })

def main():
    run_api("main:app", host='0.0.0.0', port=8000, log_level="info")

if __name__ == "__main__":
    main()
