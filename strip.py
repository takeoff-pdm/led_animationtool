from json import load, dump
from time import time_ns, sleep
from rpi_ws281x import Adafruit_NeoPixel
from threading import Thread

from __init__ import CONFIG_FILE, ANIMATION_DATA

from util.database.database import Database
from util.database.section import fetch_sections, fetch_section, remove_section
from util.database.color_sequence import fetch_color_sequences, fetch_color_sequence, remove_color_sequence
from util.database.color import fetch_color, remove_color, update_color
from util.database.animation import fetch_animations

from util.api.models import Color as ApiColor

from section import Section
from color_sequence import ColorSequence
from color import Color

from animations.animation import Animation
from animations.flow import Flow
from animations.shooter import Shooter
# Add more...


class Strip():
    def __init__(self):
        config = self.fetch_config()

        self.brightness = config['brightness']  # 0 to 255
        self.led_count = config['led_count']
        self.frequency = config['frequency']    # LED signal frequency in hertz (usually 800khz)

        self.bpm = config['bpm']                # Animation speed (Beats per minute)

        # Initialize sections
        self.sections =  []
        sections_data = fetch_sections()

        for section_data in sections_data:
            self.sections.append(Section(section_data['id'], section_data['name'], 
                                         section_data['start_led'], section_data['end_led']))
        
        # Initialize color sequences
        self.color_sequences =  []
        color_sequences_data = fetch_color_sequences()

        for color_sequence_data in color_sequences_data:
            self.color_sequences.append(ColorSequence(color_sequence_data['id'], color_sequence_data['name'], 
                                                      color_sequence_data['description'], color_sequence_data['selection'], 
                                                      color_sequence_data['color_amount']))

        self.running_animations = []

        self.init_animations()
        
        self.init_strip()  # Initialize strip
        
        self.strip.begin() # Start the strip
        
        self.animating = None

    @staticmethod
    def fetch_config() -> dict:
        with open(CONFIG_FILE, 'r') as f:
            return load(f)  # Loads config in json-format
    
    @staticmethod
    def update_config(value_name: str, value):
        config = Strip.fetch_config()
        config[value_name] = value

        with open(CONFIG_FILE, 'w') as f:
            dump(config, f)
            
    def init_strip(self):
        config = self.fetch_config()
        
        self.strip = Adafruit_NeoPixel(config['led_count'], config['pin'], config['frequency'], 
                                        config['dma'], config['led_invert'], config['brightness'], 
                                        config['channel'])
        
        for animation in self.running_animations:
            animation.strip = self.strip

    def create_animations(self):
        for x in range(len(ANIMATION_DATA)):
            try:
                Database.push_to_db('INSERT INTO animations VALUES(:id, :name, :description, :variation, :direction)',
                                    {
                                        'id': x,
                                        'name': ANIMATION_DATA[x]['name'],
                                        'description': ANIMATION_DATA[x]['description'],
                                        'variation': ANIMATION_DATA[x]['variation'],
                                        'direction': ANIMATION_DATA[x]['direction']
                                    })
            except:
                pass

    
    def init_animations(self):
        animations = fetch_animations()

        if not animations:
            self.create_animations()

        check = 0
        
        for animation in animations:
            if animation['name'] == 'Flow':
                check += 1
            
            elif animation['name'] == 'Shooter':
                check += 1
            
            elif animation['name'] == 'Strobo':
                check += 1
            
            # Add more...
        
        if check == len(ANIMATION_DATA):
            self.create_animations()

    
    def set_brightness(self, brightness: int) -> bool:
        if brightness < 0 or brightness > 255:
            return False
        
        self.brightness = brightness
        self.update_config('brightness', self.brightness)

        self.init_strip()  # Update strip
        
        return True

    def set_led_count(self, led_count: int) -> bool:
        if led_count < 0:
            return False
        
        self.led_count = led_count
        self.update_config('led_count', self.led_count)
        
        self.init_strip()  # Update strip
        
        return True

    def set_bpm(self, bpm: int) -> bool:
        if bpm < 1:
            return False
        
        self.bpm = bpm
        self.update_config('bpm', bpm.value)

        self.init_strip()  # Update strip
        
        return True
    
    # Sections
    def add_section(self, name: str, start_led: int, end_led: int) -> bool:
        if fetch_section(name):
            return False
        
        section = Section(name=name, start_led=start_led, end_led=end_led)
        
        if not section.sync_changes_to_db(new=True):
            return False
        
        self.sections.append(section)

        return True
    
    def remove_section(self, id: int) -> bool:
        for section in self.sections:
            if section.id == id:
                if not remove_section(id):
                    return False
                
                self.sections.remove(section)
                
                for animation in self.running_animations:
                    if animation.start_led == section.start_led and \
                       animation.end_led == section.end_led:
                        self.running_animations.remove(animation)
                        
                        # No break, because it is (currently) possible to have 
                        # a part of the strip listed twice in sections list
                
                return True
            
        return False

    def update_section(self, id: int, name: str, start_led: int, end_led: int) -> bool:
        for section in self.sections:
            if section.id == id:
                section.name = name
                section.start_led = start_led
                section.end_led = end_led
                
                return section.sync_changes_to_db()
            
        return False
    
    # Color Sequences
    def add_color_sequence(self, name: str, description: str, selection: int, color_amount: int) -> bool:
        if fetch_color_sequence(name):
            return False
        
        color_sequence = ColorSequence(name=name, description=description, 
                                       selection=selection, color_amount=color_amount)
        
        if not color_sequence.sync_changes_to_db(new=True):
            return False
        
        self.color_sequences.append(color_sequence)

        return True
    
    def remove_color_sequence(self, id: int) -> bool:
        for color_sequence in self.color_sequences:
            if color_sequence.id == id:
                remove_color_sequence(id)
                self.color_sequences.remove(color_sequence)
                
                return True
            
        return False

    def update_color_sequence(self, id: int, name: str, description: str, 
                              selection: int, color_amount: int) -> bool:
        for color_sequence in self.color_sequences:
            if color_sequence.id == id:
                color_sequence.name = name
                color_sequence.description = description
                color_sequence.selection = selection
                color_sequence.color_amount = color_amount
                
                return color_sequence.sync_changes_to_db()
            
        return False
    
    # Colors
    def add_color(self, color_sequence_id: int, red: int, green: int, blue: int) -> bool:
        for color_sequence in self.color_sequences:
            if color_sequence.id == color_sequence_id:
                return color_sequence.add_color(Color(color_sequence_id=color_sequence_id, 
                                                      position=None, red=red, green=green, blue=blue))
            
        return False
    
    def remove_color(self, id: int) -> bool:
        color = Color(id=id)
        
        if not remove_color(id):
            return False
        
        # Also remove from color_sequence cache
        for color_sequence in self.color_sequences:
            if color_sequence.id == color.color_sequence_id:
                color_sequence.color_list.pop(color.position)
                
        return True
                
    def update_color(self, color: ApiColor) -> bool:
        success = update_color(color.id, color.color_sequence_id, color.position, 
                               color.red, color.green, color.blue)
        
        # Update color in sequence
        for color_sequence in self.color_sequences:
            if color_sequence.id == color.color_sequence_id:
                color_sequence.update_colors()
                
                return success
            
        return False

    # Animations
    @property
    def sleep_time(self):
        return 60 / self.bpm
    
    def color_wipe(self, color):
        '''Change color of all pixels.
        '''
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

        self.strip.show()
    
    def add_animation(self, animation: Animation, section: Section, color_sequence: ColorSequence):
        '''Adds animation to animate (not a new animation).
        '''
        animation.bpm = self.bpm
        animation.start_led = section.start_led
        animation.end_led = section.end_led
        
        animation.color_sequence = color_sequence
        
        animation.strip = self.strip
        
        self.running_animations.append(animation)
        
    def animate(self):
        try:
            while True:
                starting_time = time_ns() // 1_000_000
                
                # Check if bpm of animations is off
                if len(self.running_animations) > 0:
                    if self.running_animations[0].bpm != self.bpm:
                        # Rearange beats
                        for animation in self.running_animations:
                            animation.bpm = self.bpm
                
                for animation in self.running_animations:
                    Thread(target=animation.animate).start()
                
                if self.sleep_time - (((time_ns() // 1_000_000) - starting_time) // 1_000) > 0:
                    sleep(self.sleep_time - (((time_ns() // 1_000_000) - starting_time) // 1_000))
                
                else:
                    print('Code too slow!')
        
        except:
            self.color_wipe(0)
    
    def stop_animate(self, section_id: int) -> bool:
        # Fetch section
        for possible_section in self.sections:
                if possible_section.id == section_id:
                    section = possible_section
        
        if not section:
            return False
        
        # Find running animation and stop it
        for animation in self.running_animations:
            if animation.start_led == section.start_led:
                self.running_animations.remove(animation)
                
                return True
            
        return False

    def start_animate(self, color_sequence_id: int, animation: Animation = None, animation_id: int = None, 
                      section: Section = None, section_id: int = None) -> bool:
        if not section:
            # Find out which section is meant
            for possible_section in self.sections:
                if possible_section.id == section_id:
                    section = possible_section
                    
        if not section:
            return False
        
        self.stop_animate(section.id)  # Stop current animation if there is one
        
        # Find out which color sequence is meant
        color_sequence = None
        
        for possible_sequence in self.color_sequences:
            if possible_sequence.id == color_sequence_id:
                color_sequence = possible_sequence
                
        if not color_sequence:
            return False
        
        if not animation:
            # Find out which animation is meant
            if animation_id == 0:
                self.add_animation(Flow(id=0), section, color_sequence)
                
            elif animation_id == 1:
                self.add_animation(Shooter(id=1), section, color_sequence)
            
            # Add more ...
        else:
            self.add_animation(animation, section, color_sequence)

        if self.animating == None:
            self.animating = Thread(target=self.animate)
            self.animating.start()
        
        return True
