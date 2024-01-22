from json import load, dump
from rpi_ws281x import Adafruit_NeoPixel

from __init__ import CONFIG_FILE

from util.database.section import fetch_sections, fetch_section

from section import Section

from animations.animation import Animation
from animations.flow import Flow
from animations.shooter import Shooter


class Strip():
    def __init__(self):
        config = self.fetch_config()

        self.brightness = config['brightness']  # 0 to 255
        self.led_count = config['led_count']
        self.frequency = config['frequency']    # LED signal frequency in hertz (usually 800khz)

        self.bpm = config['bpm']                # Animation speed (Beats per minute)

        self.strip = Adafruit_NeoPixel(config['led_count'], config['pin'], config['frequency'], 
                                        config['dma'], config['led_invert'], config['brightness'], 
                                        config['channel'])
        
        self.strip.begin() # Start the strip

        # Init sections
        self.sections =  []
        sections_data = fetch_sections()

        for section_data in sections_data:
            self.sections.append(Section(section_data['name'], section_data['start_led'], section_data['end_led']))
        
        self.running_animations = []
        
    @staticmethod
    def fetch_config() -> dict:
        with open(CONFIG_FILE, 'r') as f:
            return load(f)
    
    @staticmethod
    def update_config(value_name: str, value):
        config = Strip.fetch_config()
        config[value_name] = value

        with open(CONFIG_FILE, 'w') as f:
            dump(config, f)
    
    def set_brightness(self, brightness: int) -> bool:
        if brightness < 0 or brightness > 255:
            return False
        
        self.brightness = brightness
        self.update_config('brightness', self.brightness)
        return True

    def set_led_count(self, led_count: int) -> bool:
        if led_count < 0:
            return False
        
        self.led_count = led_count
        self.update_config('brightness', self.led_count)
        return True
    
    def add_section(self, name: str, start_led: int, end_led: int) -> bool:
        if fetch_section(name):
            return False
        
        section = Section(name, start_led, end_led)

        if not section.sync_changes_to_db(new=True):
            return False
        
        self.sections.append(section)

        return True
    
    def remove_section(self, name: str) -> bool:
        for section in self.sections:
            if section.name == name:
                section.remove_section(name)
                self.sections.remove(section)
                
                return True
            
        return False

    def update_section(self, old_name: str, name: str, start_led: int, end_led: int) -> bool:
        for section in self.sections:
            if section.name == old_name:
                section.set_name(name)
                section.set_start_led(start_led)
                section.set_end_led(end_led)
                
                return True
            
        return False

    @property
    def sleep_time(self):
        return 60 / self.bpm
    
    def color_wipe(self, color):
        """Change color of all pixels.
        """
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

        self.strip.show()

    def animate(self, animation: Animation = None, animation_name: str = None, 
                section: Section = None, section_name: str = None):
        if not animation:
            # Find out which animation is meant
            if animation_name == 'Flow':
                animation = Flow('Flow')
                animation.animate(self.bpm, section)

                self.running_animations.append(animation)
                return
                
            elif animation_name == 'Shooter':
                animation = Shooter('Shooter')
                animation.animate(self.bpm, section)

                self.running_animations.append(animation)
                return
            
            # Add more ...
        
        if not section:
            # Find out which section is meant
            for possible_section in self.sections:
                if possible_section.name == section_name:
                    section = possible_section

        animation.animate(self.bpm, section)
