

Installation guide:
```
sudo apt-get install libsqlite3-dev

sudo apt-get install libjsoncpp-dev

sudo apt install nlohmann-json-dev

sudo apt install librpi-ws281x-dev

git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
make
sudo make install

sudo apt-get install build-essential python-dev git scons

sudo scons
sudo scons install
```

## Art-Net Input

- Configure `config.json` (or `src/config.json` for defaults) with an `artnet` block:
  - `port`: UDP port to listen on (default `6454`).
  - `universe`: Expected Art-Net universe number.
  - `start_address`: First DMX channel used for control (alpha, red, green, blue, bpm, animation-kind).
  - `strip_start_led` / `strip_end_led`: LED range controlled by Art-Net.
  - `debug`: Enable verbose logging for incoming Art-Net frames.
- Channels are mapped in order: alpha (brightness %), red, green, blue, bpm, animation-kind.
  - Animation kind `0` renders a static color.
  - Values `>=1` trigger a strobe animation; different values select variations and directions.
