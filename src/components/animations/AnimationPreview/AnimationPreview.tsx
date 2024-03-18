import React, { useEffect, useState } from "react";

export type LED = {
  index: number;
  color: string; // Color in hex format
};

const initialLEDs: LED[] = Array(60)
  .fill(null)
  .map((_, index) => ({
    index,
    color: index === 0 ? "#FF0000" : "#000000", // Start with the first LED colored and the rest turned off
  }));

const LEDStrip: React.FC<{
  leds: LED[];
  brightness: number;
  children?: any;
}> = ({ leds, children, brightness }) => {
  return (
    <div style={{ display: "flex", flexDirection: "row" }}>
      {leds.map((led) => (
        <div
          key={led.index}
          style={{
            backgroundColor: led.color,
            width: "20px",
            height: "20px",
            margin: "0px",
            borderRadius: "0%",
            opacity: brightness / 100,
          }}
        ></div>
      ))}
      {children}
    </div>
  );
};

// led strip context

const LEDStripContext = React.createContext<{
  leds: LED[];
  setLEDs: React.Dispatch<React.SetStateAction<LED[]>>;
}>({
  leds: [],
  setLEDs: () => {},
});

export const useLEDStrip = () => React.useContext(LEDStripContext);

export const AnimationPreview: React.FC<{
  led_count: number;
  brightness: number;
  children: React.ReactNode;
}> = ({ led_count, brightness, children:animation }) => {
  const [leds, setLEDs] = useState<LED[]>(
    Array(led_count)
      .fill(null)
      .map((_, index) => ({
        index,
        color: index === 0 ? "#000000" : "#000000", // Start with the first LED colored and the rest turned off
      }))
  );



  return (
    <LEDStripContext.Provider
      value={{
        leds,
        setLEDs,
      }}
    >
      <LEDStrip leds={leds} brightness={brightness}>{animation}</LEDStrip>
    </LEDStripContext.Provider>
  );
};
