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
import { CheckIcon, LightningBoltIcon, TrashIcon } from "@radix-ui/react-icons";
import { useState } from "react";
import { useScenesContext } from "../ScenesContext/ScenesContext";
import { deleteScene, loadScene, updateScene } from "@/api/api-calls";
import { toast } from "sonner";

export const SceneCard: React.FC<{
  scene: Scene;
}> = ({ scene }) => {
  const { setActiveScene, activeScene, setScenes, scenes } = useScenesContext();
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [saved, setSaved] = useState(false);

  const onCancel = async () => {};

  const onLoad = async () => {
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
    setSaved(true);
    setLoaded(false);
    setLoading(true);

    const resp = await updateScene(scene);
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
    <Card className="max-w-sm">
      <CardHeader className="relative">
        <div className="flex items-center justify-between">
          <CardTitle className="">{scene.name}</CardTitle>
          {scene.id === activeScene.id && (
            <div className="h-3 w-3 animate-pulse rounded-full bg-green-400 "></div>
          )}
        </div>
        <CardDescription>{scene.description}</CardDescription>
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
      </CardContent>
      <CardFooter className="justify-between space-x-3">
        <Button variant={"secondary"} className="grow" onClick={onCancel}>
          Cancel
        </Button>
        <Button variant={"default"} className="grow" onClick={onSave}>
          Save
        </Button>
        <Button variant={"secondary"} className="grow" onClick={onLoad}>
          Load
        </Button>
      </CardFooter>
    </Card>
  );
};
