import AnimationCard from "../AnimationCard";
import { useAnimationsContext } from "../Context/Context";

export const AnimationsCardWrapper: React.FC<{}> = ({}) => {
  const { loaded, animations } = useAnimationsContext();
  return (
    <div className="w-full grid gap-5 md:grid-cols-2 xl:grid-cols-3 3xl:grid-cols-4">
      {animations.map((a) => (
        <AnimationCard animation={a} />
      ))}
    </div>
  );
};

