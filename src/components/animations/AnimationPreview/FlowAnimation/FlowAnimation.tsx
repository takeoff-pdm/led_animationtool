import { useEffect, useState } from "react";
import { LED, useLEDStrip } from "../AnimationPreview";
import { Color } from "@/api/types";
import { rgbaToHex } from "@uiw/react-color";

export const FlowAnimation: React.FC<{
  colors: Color[];
  bpm: number;
}> = ({ colors, bpm }) => {
  const { leds, setLEDs } = useLEDStrip();

  useEffect(() => {
    const amountOfSegment = leds.length / 5;

    let segments = [];

    for (let i = 0; i < amountOfSegment; i++) {
      segments.push(leds.slice(i * 5, (i + 1) * 5));
    }

    let colorIndex = 0;
    segments = segments.map((seg, index) => {
      if (colorIndex === colors.length) {
        colorIndex = 0;
      }
      let color = colors[colorIndex];
      colorIndex++;
      return seg.map((led, index) => {
        led.color = rgbaToHex({
          r: color.red,
          g: color.green,
          b: color.blue,
          a: 1,
        });
        return led;
      });
    });

    const setSegmentsToLed = (segments: LED[][]) => {
      let newLEDs: LED[] = [];
      segments.forEach((seg) => {
        newLEDs = [...newLEDs, ...seg];
      });
      setLEDs(newLEDs);
    };

    setSegmentsToLed(segments);
  }, []);

  useEffect(() => {
    // for each led update the index  + 1 and if it's the last led, set it to the first led
    // if its the last led, set it to the first led

    const interval = setInterval(() => {

      const newLed = leds.map((led, index) => {
        if (leds.length - 1 === led.index) {
          return {
            ...led,
            color: led.color,
            index: 0,
          };
        } else {
          return {
            ...led,
            color: led.color,
            index: led.index + 1,
          };
        }
      });

      setLEDs(newLed.sort((a, b) => a.index - b.index));
    }, 60000 / bpm / leds.length);
    return () => clearInterval(interval);
  }, [leds]);

  return <></>;
};
