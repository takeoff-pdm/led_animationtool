import { ColorSequence } from "../types";

const getMockData = (): ColorSequence[] => {
  return [
    {
      color_amount: 3,
      description: "A red-green-blue color sequence",
      name: "Red-Green-Blue",
      selection: 1,
      id: 1,
    },
    {
      color_amount: 1,
      description: "A green-blue-red color sequence",
      name: "Green-Blue-Red",
      selection: 2,
      id: 2,
    },
  ];
};

export const getAllCollorSequences = async (): Promise<ColorSequence[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(getMockData());
    }, 1000); // Delay of 1 second
  });
};
