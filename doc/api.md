# API

## Urls
Sections:
- ``/api/get/sections/``
    - Values: ``{}``
    - Returns: ``{ sections: List }``
- ``/api/get/section/``
    - Values: ``{ name: String }``
    - Returns: ``{ section: Map | None }``
- ``/api/add/section``
    - Values: ``{ name: String, start_led: Integer, end_led: Integer }``
- ``/api/remove/section/``
    - Values: ``{ name: String }``
- ``/api/update/section``


Color Sequence:
- ``/api/get/color_sequences/``
    - Values: ``{}``
- ``/api/get/color_sequence/``
    - Values: ``{ name: String }``
- ``/api/add/color_sequence``
    - Values: ``{ name: String, description: String, selection: Integer, color_amount: Integer }``
- ``/api/remove/color_sequence/``
    - Values: ``{ name: String }``
- ``/api/update/color_sequence``


Colors:
- ``/api/get/colors``

- ``/api/get/colors_from_sequence``

- ``/api/get/color``

Animations:
- ``/api/get/animations``

- ``/api/get/animation``

- ``/api/update/animation``

- ``/api/update/full-animation``

- ``/api/animate/start``

- ``/api/animate/stop``

Settings:
- ``/api/get/settings``

- ``/api/update/brightness``

- ``/api/update/led-count``

- ``/api/update/bpm``

