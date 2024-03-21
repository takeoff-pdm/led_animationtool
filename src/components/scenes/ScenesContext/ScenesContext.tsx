"use client";
import { getScenes , getActiveScene} from "@/api/api-calls";
import { Scene } from "@/api/types";
import { createContext, useContext, useEffect, useState } from "react";

const ScenesCtx = createContext<{
  scenes: Scene[];
  setScenes: (scenes: Scene[]) => void;
  activeScene: Scene;
  setActiveScene: (scene: Scene) => void;
}>({
  scenes: [],
  setScenes: () => {},
  activeScene: {} as Scene,
  setActiveScene: () => {},
});

export const useScenesContext = () => {
  return useContext(ScenesCtx);
};

export const ScenesContext: React.FC<{
  children: any;
}> = ({ children }) => {
  const [scenes, setScenes] = useState<Scene[]>([]);
  const [activeScene, setActiveScene] = useState<Scene>({} as Scene);

  useEffect(() => {
    getScenes().then((res) => {
      setScenes(res.scenes);
      getActiveScene().then(scene => {
        if (scene.id == -1) return;
        let activeSceneApi = res.scenes.find(s => s.id === scene.id);
        if (!activeSceneApi) return;
        setActiveScene(activeSceneApi);
      });  
    });    
  }, []);

  return (
    <ScenesCtx.Provider
      value={{
        scenes,
        setScenes,
        activeScene,
        setActiveScene,
      }}
    >
      {children}
    </ScenesCtx.Provider>
  );
};
