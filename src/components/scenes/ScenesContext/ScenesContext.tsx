"use client";
import { Scene } from "@/api/types";
import { createContext, useContext, useState } from "react";

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
