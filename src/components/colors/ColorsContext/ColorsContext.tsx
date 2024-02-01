import { getAllCollorSequences } from "@/api/colors/get-all";
import { ColorSequence } from "@/api/types";
import { createContext, useContext, useEffect, useState } from "react";

interface ColorsContextProps {
  setColorSequences: (data: ColorSequence[]) => void;
  colorSequences: ColorSequence[];
  loaded: boolean;
}

// Create the context with default values
const ColorsCtx = createContext<ColorsContextProps>({
  colorSequences: [],
  setColorSequences: () => {},
  loaded: false,
});

export const useColorsContext = () => {
  const context = useContext(ColorsCtx);
  if (!context) {
    throw new Error("error using animations context");
  }
  return context;
};

export const ColorsContext: React.FC<{ children: any }> = ({ children }) => {
  const [colorSequences, setColorSequences] = useState<ColorSequence[]>([]);
  const [loaded, setLoaded] = useState<boolean>(false);

  useEffect(() => {
    getAllCollorSequences().then((a) => {
      setColorSequences(a);
      setLoaded(true);
    });
  }, []);

  return (
    <ColorsCtx.Provider
      value={{
        colorSequences,
        setColorSequences,
        loaded,
      }}
    >
      {children}
    </ColorsCtx.Provider>
  );
};
