import { Animation, ColorSequence } from "@/api/types";
import { createContext, useContext, useState } from "react";

interface AnimationContextProps {
  loaded: boolean;
  animation: Animation;
  setAnimation: (a: Animation) => void;
}

const AnimationContext = createContext<AnimationContextProps>({
  loaded: false,
  animation: {} as Animation,
  setAnimation: (a) => {},
});

export const AnimationCardContext: React.FC<{
  animation: Animation;
  children: any;
}> = ({ animation: animProp, children }) => {
  const [loaded, setLoaded] = useState<boolean>(false);
  const [animation, setAnimation] = useState<Animation>(animProp);
  const [colorSequence, setColorSequence] = useState<ColorSequence>(
    {} as ColorSequence
  );

  /* useEffect(() => {
        getColor
    },[colorSequence])*/

  return (
    <AnimationContext.Provider
      value={{
        loaded,
        animation,
        setAnimation,
      }}
    >
      {children}
    </AnimationContext.Provider>
  );
};

export const useAnimationContext = () => {
  const context = useContext(AnimationContext);
  if (!context) {
    throw new Error("error using animations context");
  }
  return context;
};
