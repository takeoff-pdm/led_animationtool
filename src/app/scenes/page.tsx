"use client";
import ScenesContext from "@/components/scenes/ScenesContext";
import ScenesMenuBar from "@/components/scenes/ScenesMenuBar";
import ScenesWrapper from "@/components/scenes/ScenesWrapper";

const ScenesPage: React.FC = () => {
  return (
    <ScenesContext>
      <ScenesMenuBar />
      <ScenesWrapper />
    </ScenesContext>
  );
};

export default ScenesPage;
