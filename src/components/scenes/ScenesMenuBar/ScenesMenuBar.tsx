import { Button } from "@/components/ui/button";
import { PlusIcon } from "@radix-ui/react-icons";

export const ScenesMenuBar: React.FC = () => {
  return (
    <div className="min-h-20 w-full items-center justify-between space-y-2 p-4 sm:px-14 py-6 lg:flex lg:px-14">
      <AddSceneButton />
    </div>
  );
};

const AddSceneButton: React.FC = () => {
  const onClick = () => {};

  return (
    <Button onClick={onClick}>
      <PlusIcon className="w-4 h-4 mr-2" />
      Add Scene
    </Button>
  );
};
