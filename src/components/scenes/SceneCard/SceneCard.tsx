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
} from "@radix-ui/react-icons";
import { useState } from "react";
import { useScenesContext } from "../ScenesContext/ScenesContext";

export const SceneCard: React.FC<{
  scene: Scene;
}> = ({ scene }) => {
  const { activeScene } = useScenesContext();
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [saved, setSaved] = useState(false);

  const onCancel = async () => {};

  const onLoad = async () => {
    setSaved(false);
    setLoaded(false);
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setLoaded(true);
    }, 1000);
  };
  const onSave = async () => {
    setSaved(true);
    setLoaded(false);
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setLoaded(true);
      setSaved(true);
    }, 1000);
  };

  return (
    <Card className="max-w-sm">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="">{scene.name}</CardTitle>

          {scene.id === activeScene.id && (
            <div className="h-3 w-3 animate-pulse rounded-full bg-green-400 "></div>
          )}
        </div>

        <CardDescription>{scene.description}</CardDescription>
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
        <Button variant={"destructive"} className="grow" onClick={onCancel}>
          Cancel
        </Button>
        <Button variant={"secondary"} className="grow" onClick={onSave}>
          Save
        </Button>
        <Button variant={"default"} className="grow" onClick={onLoad}>
          Load
        </Button>
      </CardFooter>
    </Card>
  );
};
