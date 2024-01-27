# API

## Urls
Sections:
- ``/api/get/sections/``
    - Values: ``{}``
- ``/api/get/section/``
    - Values: ``{ name: String }``
- ``/api/add/section``
    - Values: ``{ name: String, start_led: Integer, end_led: Integer }``
- ``/api/remove/section/``
    - Values: ``{ name: String }``
- update

Color Sequence:
- ``/api/get/color_sequences/``
    - Values: ``{}``
- ``/api/get/color_sequence/``
    - Values: ``{ name: String }``
- ``/api/add/color_sequence``
    - Values: ``{ name: String, description: String, selection: Integer, color_amount: Integer }``
- ``/api/remove/color_sequence/``
    - Values: ``{ name: String }``
- update
