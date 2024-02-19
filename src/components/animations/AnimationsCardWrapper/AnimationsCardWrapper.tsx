import AnimationCard from "../AnimationCard";
import { useAnimationsContext } from "../Context/Context";

export const AnimationsCardWrapper: React.FC<{}> = ({}) => {
  const { loaded, animations } = useAnimationsContext();
  return (
    <div className="gap-2 flex sm:px-14 px-4 transition-all flex-col md:flex-row">
      {animations.map((a) => (
        <AnimationCard animation={a} />
      ))}
    </div>
  );
};

