import { addScene, getScenes } from "@/api/api-calls";
import { Button } from "@/components/ui/button";
import { PlusIcon } from "@radix-ui/react-icons";
import { toast } from "sonner";
import { useScenesContext } from "../ScenesContext/ScenesContext";

export const ScenesMenuBar: React.FC = () => {
  return (
    <div className="min-h-20 w-full items-center justify-between space-y-2 p-4 sm:px-14 py-6 lg:flex lg:px-14">
      <AddSceneButton />
    </div>
  );
};

const AddSceneButton: React.FC = () => {
  const { scenes, setScenes } = useScenesContext();
  const onAdd = async () => {
    console.log("Adding scene")
    let newScene = {
      name: "New Scene",
      description: "New Scene Description",
    };
    const resp = await addScene(newScene);
    if (!resp.success) {
      toast("Failed to add scene!");
      return;
    }

    getScenes().then((resp) => {
      setScenes(resp.scenes);
    });
    
    toast("Scene added!");
  };

  return (
    <Button onClick={onAdd}>
      <PlusIcon className="w-4 h-4 mr-2" />
      Add Scene
    </Button>
  );
};
