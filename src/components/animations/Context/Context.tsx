import { getAllAnimations } from "@/api/animations/get-all";
import { getAnimations } from "@/api/api-calls";
import { Animation, Color, ColorSequence, Section } from "@/api/types";
import { createContext, useContext, useEffect, useState } from "react";

interface AnimationsContextProps {
  setAnimations: (data: Animation[]) => void;
  animations: Animation[];
  loaded: boolean;
  activeAnimation: Animation;
  setActiveAnimation: (animation: Animation) => void;
  selectedSection: Section;
  setSelectedSection: (section: Section) => void;
  selectedSequence: ColorSequence;
  setSelectedSequence: (sequence: ColorSequence) => void;
}

// Create the context with default values
const AnimationsContext = createContext<AnimationsContextProps>({
  selectedSection: {} as Section,
  setSelectedSection: () => {},
  animations: [],
  setAnimations: () => {},
  loaded: false,
  activeAnimation: {} as Animation,
  setActiveAnimation: () => {},
  selectedSequence: {} as ColorSequence,
  setSelectedSequence: () => {},
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
  const [activeAnimation, setActiveAnimation] = useState<Animation>(
    {} as Animation
  );
  const [selectedSection, setSelectedSection] = useState<Section>(
    {} as Section
  );
  const [selectedSequence, setSelectedSequence] = useState<ColorSequence>(
    {} as ColorSequence
  );
  useEffect(() => {
    getAnimations().then((d) => {
      if (d.animations) {
        setAnimations(d.animations);
      }
      setLoaded(true);
    });
  }, []);

  return (
    <AnimationsContext.Provider
      value={{
        selectedSequence,
        setSelectedSequence,
        selectedSection,
        setSelectedSection,
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
