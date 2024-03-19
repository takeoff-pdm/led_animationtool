import SceneCard from "../SceneCard";
import { useScenesContext } from "../ScenesContext/ScenesContext";

export const ScenesWrapper: React.FC = () => {
  const { scenes } = useScenesContext();
  return (
    <div className="w-full sm:px-14 px-4 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      {scenes.map((scene) => (
        <SceneCard
          scene={scene}
        />
      ))}
    </div>
  );
};
