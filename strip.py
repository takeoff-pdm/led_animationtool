from json import load, dump
from time import time_ns, sleep
from rpi_ws281x import Adafruit_NeoPixel
from threading import Thread

from __init__ import CONFIG_FILE, ANIMATION_DATA, ANIMATION_STEPS

from util.database.database import Database
from util.database.section import fetch_sections, fetch_section, remove_section
from util.database.color_sequence import fetch_color_sequences, fetch_color_sequence, remove_color_sequence
from util.database.color import fetch_color, remove_color, update_color
from util.database.animation import fetch_animation, fetch_animations
from util.database.scene import fetch_scenes, remove_scene
from util.database.scene_animation import remove_scene_animations

from util.api.models import Color as ApiColor
from util.udp.udp import UDP

from section import Section
from color_sequence import ColorSequence
from frequency_colors import FrequencyColors
from color import Color
from scene import Scene

from animations.mono_color import MonoColor
from animations.animation import Animation
from animations.flow import Flow
from animations.shooter import Shooter
from animations.strobe import Strobe
from animations.squeeze import Squeeze
# Add more...


class Strip:
    def __init__(self):
        config = self.fetch_config()

        self.brightness = config['brightness']  # 0 to 255
        self.led_count = config['led_count']
        self.frequency = config['frequency']  # LED signal frequency in hertz (usually 800khz)

        self.bpm = config['bpm']  # Animation speed (Beats per minute)
        self.step = 0

        # Initialize sections
        self.sections = []
        sections_data = fetch_sections()

        for section_data in sections_data:
            self.sections.append(Section(section_data['id'], section_data['name'],
                                         section_data['start_led'], section_data['end_led']))

        # Initialize color sequences
        self.color_sequences = []
        color_sequences_data = fetch_color_sequences()

        for color_sequence_data in color_sequences_data:
            self.color_sequences.append(ColorSequence(color_sequence_data['id'], color_sequence_data['name'],
                                                      color_sequence_data['description'],
                                                      color_sequence_data['selection'],
                                                      color_sequence_data['color_amount']))
            
        # Initialze freqency color sequences
        self.frequency_colors = FrequencyColors(-1)

        # Initialize scenes
        self.scenes = []
        scenes_data = fetch_scenes()

        for scene_data in scenes_data:
            self.scenes.append(Scene(scene_data['id'], scene_data['name'], scene_data['description']))

        self.active_scene: int = -1

        self.running_animations = []
        self.beat = 0

        self.udp_server = UDP('0.0.0.0', 5005)

        self.init_animations()

        self.init_strip()  # Initialize strip

        self.strip.begin()  # Start the strip

        self.stop = False  # Add variable to kill animation thread
        self.animating = None

        self.show_strip = False

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
                                       config['dma'], config['led_invert'], 255,
                                       config['channel'])

        for animation in self.running_animations:
            animation.strip = self.strip

    def restart_strip(self):
        # Stop all running animations
        self.stop = True
        sleep(self.sleep_time * 2.1)  # Wait for all animations to stop

        self.strip = None

        self.init_strip()

        self.strip.begin()  # Restart the strip

        # Restart all animations
        self.stop = False
        self.animating = Thread(target=self.animate, args=(lambda: self.stop,))
        self.animating.start()

    def create_animations(self):
        for x in range(len(ANIMATION_DATA)):
            if fetch_animation(x):
                continue

            Database.push_to_db('INSERT INTO animations VALUES(:id, :name, :description)',
                                {
                                    'id': x,
                                    'name': ANIMATION_DATA[x]['name'],
                                    'description': ANIMATION_DATA[x]['description']
                                })

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
        if brightness < 0 or brightness > 100:
            return False

        self.brightness = brightness / 100
        self.update_config('brightness', self.brightness)

        # Update brightness in every running animation
        for animation in self.running_animations:
            animation.brightness = self.brightness

        return True

    def set_led_count(self, led_count: int) -> bool:
        if led_count < 0:
            return False

        self.led_count = int(led_count)  # Ensure that led-count is an integer
        self.update_config('led_count', self.led_count)

        self.restart_strip()  # Update strip

        return True

    def set_bpm(self, bpm: int) -> bool:
        if bpm < 1:
            return False

        self.bpm = bpm
        self.update_config('bpm', bpm)

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
                
                if section.start_led != start_led or section.end_led != end_led:
                    section.start_led = start_led
                    section.end_led = end_led

                    # Check if any animation is running on the section
                    for animation in self.running_animations:
                        if animation.section_id == section.id:
                            animation.color_wipe(0)

                        animation.start_led = start_led
                        animation.end_led = end_led

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
        for animation in self.running_animations:
            if animation.color_sequence.id == id:
                animation.color_sequence.name = name
                animation.color_sequence.description = description
                animation.color_sequence.selection = selection
                animation.color_sequence.color_amount = color_amount

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
                for color_in_list in color_sequence.color_list:
                    if color_in_list.id == color.id:
                        color_sequence.color_list.remove(color_in_list)

                    elif color_in_list.position > color.position:  # Rearrange color positions
                        color_in_list.position -= 1
                        color_in_list.sync_changes_to_db()

                for animation in self.running_animations:
                    if animation.color_sequence.id == color_sequence.id:
                        animation.color_sequence = color_sequence

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
        """Change color of all pixels.
        """
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

        self.strip.show()

    def update_animation(self, id: int, section_id: int, name: str, description: str, variation: int, direction: int,
                         offset: int) -> bool:
        animation = Animation(id, section_id, name, description, variation, direction, offset)

        # Update running animations
        for anim in self.running_animations:
            if anim.id == animation.id and anim.section_id == animation.section_id:
                anim.name = animation.name
                anim.description = animation.description
                anim.variation = animation.variation
                anim.direction = animation.direction
                anim.offset = animation.offset

        return animation.sync_changes_to_db()

    def add_animation(self, animation: Animation, section: Section, color_sequence: ColorSequence):
        """Adds animation to animate (not a new animation).
        """
        animation.bpm = self.bpm
        animation.section_id = section.id
        animation.start_led = section.start_led
        animation.end_led = section.end_led

        animation.color_sequence = color_sequence

        animation.strip = self.strip
        animation.brightness = self.brightness

        self.running_animations.append(animation)

    def animate(self, stop):
        try:
            Thread(target=self.show_strip_handler, args=(stop,)).start()
            Thread(target=self.udp_server.receive, args=(stop,)).start()
            starting_time = time_ns() // 1_000_000

            while stop() == False:
                if len(self.running_animations) > 0:
                    # Check if bpm of animations is off
                    if self.running_animations[0].bpm != self.bpm:
                        # Rearrange beats
                        for animation in self.running_animations:
                            animation.bpm = self.bpm

                    # Check if brightness of animations is off
                    if self.running_animations[0].brightness != self.brightness:
                        # Rearrange brightness
                        for animation in self.running_animations:
                            animation.brightness = self.brightness

                for animation in self.running_animations:
                    Thread(target=animation.animate,
                           args=(self.beat + animation.offset, self.step)).start()

                if self.udp_server.data_received:
                    self.udp_server.data_received = False

                    print(f"Server echoed: {self.udp_server.data.decode()}")
                    # TODO: Implement UDP data handling
                    # 1st Byte: BPM; 2nd Byte: Color Sequence To Select

                sleep_time_adjusted = self.sleep_time - (((time_ns() // 1_000_000) - starting_time) / 1_000)

                if sleep_time_adjusted > 0:
                    sleep(sleep_time_adjusted / 100)

                else:
                    print('Code too slow!')
                
                starting_time = time_ns() // 1_000_000

                self.show_strip_request()

                self.step += 1

                if self.step % ANIMATION_STEPS == 0:
                    self.beat += 1
                    if self.beat == 16:
                        self.beat = 0

                    self.step = 0

        except:
            self.color_wipe(0)

    def stop_animate(self, section_id: int, start_new: bool = False) -> bool:
        # Fetch section
        for possible_section in self.sections:
            if possible_section.id == section_id:
                section = possible_section
                break

        if not section:
            return False

        # Find running animation and stop it
        for animation in self.running_animations:
            if animation.section_id == section.id:
                self.running_animations.remove(animation)

                sleep(self.sleep_time * 1.1)

                if not start_new:
                    animation.color_wipe(0)  # Turn part of strip off

                return True

        return False

    def start_animate(self, color_sequence_id: int, animation: Animation = None, animation_id: int = None,
                      section: Section = None, section_id: int = None) -> bool:  # Animation and Section there for later
        if not section:
            # Find out which section is meant
            for possible_section in self.sections:
                if possible_section.id == section_id:
                    section = possible_section

        if not section:
            return False

        self.stop_animate(section.id, start_new=True)  # Stop current animation if there is one

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
                self.add_animation(MonoColor(id=0, section_id=section.id), section, color_sequence)

            elif animation_id == 1:
                self.add_animation(Flow(id=1, section_id=section.id), section, color_sequence)

            elif animation_id == 2:
                self.add_animation(Shooter(id=2, section_id=section.id), section, color_sequence)

            elif animation_id == 3:
                self.add_animation(Squeeze(id=3, section_id=section.id), section, color_sequence)

            elif animation_id == 4:
                self.add_animation(Squeeze(id=4, section_id=section.id), section, color_sequence)

            # Add more ...
        else:
            self.add_animation(animation, section, color_sequence)

        if self.animating == None:
            self.animating = Thread(target=self.animate, args=(lambda: self.stop,))
            self.animating.start()

        return True

    def show_strip_handler(self, stop):
        while stop() == False:
            if self.show_strip == True:
                self.show_strip = False
                self.strip.show()

            sleep(0.08)

    def show_strip_request(self):
        self.show_strip = True

    # Scene handling
    def add_scene(self, name: str, description: str) -> bool:
        scene = Scene(name=name, description=description)

        if not scene.sync_changes_to_db(new=True):
            return False

        self.scenes.append(scene)

        return True

    def remove_scene(self, scene_id: int) -> bool:
        for scene in self.scenes:
            if scene.id == scene_id:
                if not remove_scene(scene_id):
                    return False

                remove_scene_animations(scene_id)

                self.scenes.remove(scene)

                return True

        return False

    def update_scene(self, id: int, name: str, description: str) -> bool:
        for scene in self.scenes:
            if scene.id == id:
                scene.name = name
                scene.description = description

                return scene.sync_changes_to_db()

        return False

    def save_scene(self, scene_id: int) -> bool:
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene.save(self.running_animations)

        return False

    def load_scene(self, scene_id: int) -> bool:
        for scene in self.scenes:
            if scene.id == scene_id:
                animations_data_to_run = scene.load()  # Load scene into workspace

                self.running_animations = []  # Stop all running animations

                if animations_data_to_run:
                    for animation_data in animations_data_to_run:
                        self.start_animate(color_sequence_id=animation_data['color_sequence_id'],
                                           animation_id=animation_data['animation_id'],
                                           section_id=animation_data['section_id'])

                self.active_scene = scene_id

                return True

        return False

    def get_frequency_color_sequences(self):
        return {
            'color_sequence_id_1': self.frequency_colors.color_sequence_id_1,
            'color_sequence_id_2': self.frequency_colors.color_sequence_id_2,
            'color_sequence_id_3': self.frequency_colors.color_sequence_id_3
        }
