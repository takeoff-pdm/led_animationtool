# API

## Urls
Sections:
- ``/api/get/sections/``
    - Values: ``{}``
    - Returns: ``{ sections: List }``
- ``/api/get/section/``
    - Values: ``{ id: Integer }``
    - Returns: ``{ section: Section | null }``
- ``/api/add/section``
    - Values: ``{ name: String, start_led: Integer, end_led: Integer }``
    - Returns: ``{ success: boolean }``
- ``/api/remove/section/``
    - Values: ``{ id: Integer }``
    - Returns: ``{ success: boolean }``
- ``/api/update/section``
    - Values: ``{ id: Integer, name: String, start_led: Integer, end_led: Integer }``
    - Returns: ``{ success: boolean }``

Color Sequence:
- ``/api/get/color_sequences/``
    - Values: ``{}``
    - Returns: ``{ color_sequences: List }``
- ``/api/get/color_sequence/``
    - Values: ``{ id: Integer }``
    - Returns: ``{ color_sequence: ColorSequence | null }``
- ``/api/add/color_sequence``
    - Values: ``{ name: String, description: String, selection: Integer, color_amount: Integer }``
    - Returns: ``{ success: boolean }``
- ``/api/remove/color_sequence/``
    - Values: ``{ id: Integer }``
    - Returns: ``{ success: boolean }``
- ``/api/update/color_sequence``
    - Values: ``{ id: Integer, name: String, description: String, selection: Integer, color_amount: Integer }``
    - Returns: ``{ success: boolean }``

Colors:
- ``/api/get/colors``
    - Values: ``{}``
    - Returns: ``{ colors: List }``
- ``/api/get/colors_from_sequence``
    - Values: ``{ id: Integer }`` (Id of color-sequence)
    - Returns: ``{ colors: List }``
- ``/api/get/color``
    - Values: ``{ id: Integer }`` (Id of color)
    - Returns: ``{ color: Color | null }``
- ``/api/add/color``
    - Values: ``{ color_sequence_id: Integer, position: Integer, red: Integer, green: Integer, blue: Integer }``
    - Returns: ``{ success: boolean }``
- ``/api/remove/color``
    - Values: ``{ id: Integer }`` (Id of color)
    - Returns: ``{ success: boolean }``
- ``/api/update/color``
    - Values: ``{ id: Integer, color_sequence_id: Integer, position: Integer, red: Integer, green: Integer, blue: Integer }``
    - Returns: ``{ success: boolean }``

Animations:
- ``/api/get/animations``
    - Values: ``{}``
    - Returns: ``{ animations: List }``
- ``/api/get/animation``
    - Values: ``{ id: Integer }``
    - Returns: ``{ animation: Animation | null }``
- ``/api/update/animation``
    - Values: ``{ id: Integer, name: String, description: String, animation.variation, animation.direction }``
    - Returns: ``{ success: boolean }``
- ``/api/animate/start``
    - Values: ``{ color_sequence_id: Integer, animation_id: Integer, section_id: Integer }``
    - Returns: ``{ success: boolean }``
- ``/api/animate/stop``
    - Values: ``{ id: Integer }`` (Id of section)
    - Returns: ``{ success: boolean }``

Settings:
- ``/api/get/settings``
    - Values: ``{ value: Integer }``
    - Returns: ``{ success: boolean }``
- ``/api/update/brightness``
    - Values: ``{ value: Integer }``
    - Returns: ``{ success: boolean }``
- ``/api/update/led-count``
    - Values: ``{ value: Integer }``
    - Returns: ``{ success: boolean }``
- ``/api/update/bpm``
    - Values: ``{ value: Integer }``
    - Returns: ``{ success: boolean }``
