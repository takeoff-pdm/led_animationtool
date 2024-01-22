import { Animation } from "@/api/types";
import AnimationCard from "../AnimationCard";
import { useContext } from "react";
import { useAnimationsContext } from "../Context/Context";

export const AnimationsCardWrapper: React.FC<{}> = ({}) => {
  const { loaded, animations } = useAnimationsContext();
  return (
    <div className="gap-4 flex px-14">
      {animations.map((a) => (
        <AnimationCard animation={a} />
      ))}
    </div>
  );
};

