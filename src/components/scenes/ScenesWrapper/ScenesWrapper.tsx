import SceneCard from "../SceneCard";

export const ScenesWrapper: React.FC = () => {
  return (
    <div className="w-full sm:px-14 p-8 px-4 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      <SceneCard
        scene={{
          id: 1,
          name: "Scene 1",
          description: "Scene 1 description",
        }}
      />
    </div>
  );
};
