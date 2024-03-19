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
import { RocketIcon, UpdateIcon } from "@radix-ui/react-icons";
import { useState } from "react";

export const SceneCard: React.FC<{
  scene: Scene;
}> = ({ scene }) => {
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);

  const onCancel = async () => {};

  const onLoad = async () => {
    setLoaded(false);
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setLoaded(true);
    }, 1000);
  };
  const onSave = async () => {
    setLoaded(false);
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setLoaded(true);
    }, 1000);
  };

  return (
    <Card className="max-w-sm">
      <CardHeader>
        <CardTitle>{scene.name}</CardTitle>
        <CardDescription>{scene.description}</CardDescription>
        <CardContent className="h-32">
          <div className="w-full h-full flex justify-center items-center">
            {loading && (
              <Loading scale={2}>
                <div className="text-sm text-slate-700">Loading</div>
              </Loading>
            )}
            {loaded && !loading && (
              <div className="text-sm text-slate-700 flex items-center space-x-2">
                <RocketIcon className="w-4 h-4" />
                <span>Loaded</span>
              </div>
            )}
            {!loaded && !loading && <Note label={false}>Press <strong>Load</strong></Note>}
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
      </CardHeader>
    </Card>
  );
};
