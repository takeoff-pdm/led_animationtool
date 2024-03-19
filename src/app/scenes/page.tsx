"use client";
import ScenesContext from "@/components/scenes/ScenesContext";
import ScenesWrapper from "@/components/scenes/ScenesWrapper";

const ScenesPage: React.FC = () => {
  return (
    <ScenesContext>
      <ScenesWrapper />
    </ScenesContext>
  );
};

export default ScenesPage;
