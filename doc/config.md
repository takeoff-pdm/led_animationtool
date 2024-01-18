# Config.json

Parameters:
- **brightness**: of the stripe (0 to 255)
- **led_count**: Number of LED pixels (Examplegiving 2 meters of 60 pixels per meter Stripe has 120 leds)
- **pin**: GPIO pin connected to the pixels (18 uses PWM!)
- **frequency**: LED signal frequency in hertz (usually 800khz)
- **dma**: DMA channel to use for generating signal (try 10)
- **led_invert**: True to invert the signal (when using NPN transistor level shift)
- **channel**: Set to '1' for GPIOs 13, 19, 41, 45 or 53
- **bpm**: Animation speed (Beats per minute)
