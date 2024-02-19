"use client";
import AnimationsCardWrapper from "@/components/animations/AnimationsCardWrapper";
import AnimationsContext from "@/components/animations/Context";
import MenuBar from "@/components/animations/MenuBar";

const AnimationsPage = () => {
  return (
    <AnimationsContext>
      <MenuBar />
      <AnimationsCardWrapper />
    </AnimationsContext>
  );
};

export default AnimationsPage;
