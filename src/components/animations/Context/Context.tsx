import { getAllAnimations } from "@/api/animations/get-all";
import { Animation } from "@/api/types";
import { createContext, useContext, useEffect, useState } from "react";

interface AnimationsContextProps {
  setAnimations: (data: Animation[]) => void;
  animations: Animation[];
  loaded: boolean;
  activeAnimation: Animation | null;
  setActiveAnimation: (animation: Animation) => void;
}

// Create the context with default values
const AnimationsContext = createContext<AnimationsContextProps>({
  animations: [],
  setAnimations: () => {},
  loaded: false,
  activeAnimation: null,
  setActiveAnimation: () => {},
});

export const useAnimationsContext = () => {
  const context = useContext(AnimationsContext);
  if (!context) {
    throw new Error("error using animations context");
  }
  return context;
};

export const Context: React.FC<{ children: any }> = ({ children }) => {
  const [animations, setAnimations] = useState<Animation[]>([]);
  const [loaded, setLoaded] = useState<boolean>(false);
  const [activeAnimation, setActiveAnimation] = useState<Animation | null>(
    null
  );

  useEffect(() => {
    getAllAnimations().then((a) => {
      setAnimations(a);
      setLoaded(true);
    });
  }, []);

  return (
    <AnimationsContext.Provider
      value={{
        animations,
        setAnimations,
        loaded,
        activeAnimation,
        setActiveAnimation,
      }}
    >
      {children}
    </AnimationsContext.Provider>
  );
};
