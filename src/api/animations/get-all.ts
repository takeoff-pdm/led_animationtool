import { Animation } from "../types";

const getMockData = (): Animation[] => {
  return [
    {
      name: "Bounce",
      description: "A bouncing animation",
      variation: 1,
      direction: 90,
      color_sequence: "red-green-blue",
    },
    {
      name: "Fade",
      description: "A fading animation",
      variation: 2,
      direction: 45,
      color_sequence: "blue-yellow",
    },
  ];
};

export const getAllAnimations = async (): Promise<Animation[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(getMockData());
    }, 300); // Delay of 0.3 second
  });
};
