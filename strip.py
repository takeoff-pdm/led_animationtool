from json import load, dump
from rpi_ws281x import Adafruit_NeoPixel

from __init__ import CONFIG_FILE

from util.database.section import fetch_sections, fetch_section, remove_section
from util.database.color_sequence import fetch_color_sequences, fetch_color_sequence, remove_color_sequence

from section import Section
from color_sequence import ColorSequence

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
                                                      color_sequence_data['start_led'], color_sequence_data['end_led']))
            
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

        config = self.fetch_config()
        self.strip = Adafruit_NeoPixel(config['led_count'], config['pin'], config['frequency'], 
                                        config['dma'], config['led_invert'], config['brightness'], 
                                        config['channel'])
        
        return True

    def set_led_count(self, led_count: int) -> bool:
        if led_count < 0:
            return False
        
        self.led_count = led_count
        self.update_config('led_count', self.led_count)
        
        config = self.fetch_config()
        self.strip = Adafruit_NeoPixel(config['led_count'], config['pin'], config['frequency'], 
                                        config['dma'], config['led_invert'], config['brightness'], 
                                        config['channel'])
        return True

    def set_bpm(self, bpm: int) -> bool:
        if bpm < 1:
            return False
        
        self.bpm = bpm
        self.update_config('bpm', bpm.value)

        config = self.fetch_config()
        self.strip = Adafruit_NeoPixel(config['led_count'], config['pin'], config['frequency'], 
                                        config['dma'], config['led_invert'], config['brightness'], 
                                        config['channel'])
        return True
    
    # Sections
    def add_section(self, name: str, start_led: int, end_led: int) -> bool:
        if fetch_section(name):
            return False
        
        section = Section(name, start_led, end_led)

        if not section.sync_changes_to_db(new=True):
            return False
        
        self.sections.append(section)

        return True
    
    def remove_section(self, id: int) -> bool:
        for section in self.sections:
            if section.id == id:
                remove_section(id)
                self.sections.remove(section)
                
                return True
            
        return False

    def update_section(self, id: int, name: str, start_led: int, end_led: int) -> bool:
        for section in self.sections:
            if section.id == id:
                section.name = name
                section.start_led = start_led
                section.end_led = end_led
                
                section.sync_changes_to_db()
                
                return True
            
        return False
    
    # Color Sequences
    def add_color_sequence(name: str, description: str, selection: int, color_amount: int) -> bool:
        if fetch_color_sequence(name):
            return False
        
        color_sequence = ColorSequence(name, description, selection, color_amount)

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

                return True
            
        return False

    # Animations
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
        
        self.running_animations.append(animation)
