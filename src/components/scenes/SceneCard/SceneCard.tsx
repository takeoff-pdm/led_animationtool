import { Scene } from "@/api/types";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Loading, Note } from "@geist-ui/core";
import {
  CheckIcon,
  LightningBoltIcon,
  Pencil1Icon,
  TrashIcon,
} from "@radix-ui/react-icons";
import { useState } from "react";
import { useScenesContext } from "../ScenesContext/ScenesContext";
import { deleteScene, loadScene, saveScene, updateScene } from "@/api/api-calls";
import { toast } from "sonner";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

export const SceneCard: React.FC<{
  scene: Scene;
}> = ({ scene: sceneInput }) => {
  const [scene, setScene] = useState<Scene>(sceneInput);
  const { setActiveScene, activeScene, setScenes, scenes } = useScenesContext();
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [saved, setSaved] = useState(false);
  const [editing, setEditing] = useState(false);
  const [tempScene, setTempScene] = useState<Scene>(scene);

  const onLoad = async () => {
    if (!confirm("Are you sure you want to load the scene?")) return;
    setSaved(false);
    setLoaded(false);
    setLoading(true);

    const resp = await loadScene(scene);
    if (!resp.success) {
      toast("Failed to load scene!");
      setLoading(false);
      return;
    }

    setActiveScene(scene);
    setLoading(false);
    setLoaded(true);
  };

  const onSave = async () => {
    if (!confirm("Are you sure you want to update the scene?")) return;
    setSaved(true);
    setLoaded(false);
    setLoading(true);

    const resp = await saveScene(scene);
    if (!resp.success) {
      toast("Failed to save scene!");
      setSaved(false);
      setLoading(false);
      return;
    }

    setLoading(false);
    setLoaded(true);
    setSaved(true);
  };

  const onDelete = async () => {
    if (!confirm("Are you sure you want to delete this scene?")) {
      return;
    }

    const resp = await deleteScene(scene);
    if (resp.success) {
      toast("Scene deleted!");
      setScenes(scenes.filter((s) => s.id !== scene.id));
      if (scene.id === activeScene.id) {
        setActiveScene({} as Scene);
      }
    } else {
      toast("Failed to delete scene!");
    }
  };

  return (
    <Card className={`max-w-sm ${scene.id === activeScene.id && "border-green-400 border-2"}`}>
      <CardHeader className="relative">
        <CardTitle className="">{scene.name}</CardTitle>
        <CardDescription>{scene.description}</CardDescription>
        <Button
          onClick={() => {
            setTempScene(scene);
            setEditing(!editing);
          }}
          className="absolute top-3 right-14"
          size={"icon"}
          variant="ghost"
        >
          <Pencil1Icon className="w-4 h-4" />
        </Button>
        <Button
          onClick={onDelete}
          className="absolute top-3 right-3"
          size={"icon"}
          variant="secondary"
        >
          <TrashIcon className="w-4 h-4" />
        </Button>
      </CardHeader>
      <CardContent className="h-32">
        {!editing ? (
          <div className="w-full h-full flex justify-center items-center">
            {loading && (
              <Loading scale={2}>
                <div className="text-sm text-slate-700">Loading</div>
              </Loading>
            )}
            {loaded && !loading && !saved && (
              <div className="text-sm text-slate-700 flex items-center space-x-2">
                <LightningBoltIcon className="w-4 h-4" />
                <span>Loaded</span>
              </div>
            )}
            {!loaded && !loading && (
              <Note label={false}>
                Press <strong>Load</strong>
              </Note>
            )}
            {loaded && saved && (
              <div className="text-sm text-slate-700 flex items-center space-x-2">
                <CheckIcon className="w-4 h-4" />
                <span>Saved</span>
              </div>
            )}
          </div>
        ) : (
          <div className="w-full h-full space-y-2">
            <div className="grid gap-1.5 w-full">
              <Label>Name</Label>
              <Input
                placeholder="Scene Name"
                className="w-full"
                value={tempScene.name}
                onChange={(e) => {
                  setTempScene({ ...tempScene, name: e.target.value });
                }}
              />
            </div>
            <div className="grid gap-1.5 w-full">
              <Label>Description</Label>
              <Input
                placeholder="Scene Description"
                className="w-full"
                value={tempScene.description}
                onChange={(e) => {
                  setTempScene({ ...tempScene, description: e.target.value });
                }}
              />
            </div>
          </div>
        )}
      </CardContent>
      <CardFooter className="justify-between space-x-3">
        {!editing ? (
          <>
            <Button
              variant={loaded ? "default" : "secondary"}
              className="grow"
              onClick={onSave}
            >
              Save
            </Button>
            <Button
              variant={loaded ? "secondary" : "default"}
              className="grow"
              onClick={onLoad}
            >
              Load
            </Button>
          </>
        ) : (
          <>
            <Button
              variant={"secondary"}
              className="grow"
              onClick={() => {
                setTempScene(scene);
                setEditing(false);
              }}
            >
              Cancel
            </Button>
            <Button
              onClick={async () => {
                setLoading(true);
                const resp = await updateScene(tempScene);
                if (!resp.success) {
                  toast("Failed to update scene!");
                  return;
                }

                setLoading(false);
                setScene(tempScene);
              }}
              variant={"default"}
              className="grow"
            >
              Update
            </Button>
          </>
        )}
      </CardFooter>
    </Card>
  );
};
