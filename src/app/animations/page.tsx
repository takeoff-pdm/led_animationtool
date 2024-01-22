"use client";
import AnimationsCardWrapper from "@/components/animations/AnimationsCardWrapper";
import AnimationsContext from "@/components/animations/Context";
import MenuBar from "@/components/animations/MenuBar";

const AnimationsPage = () => {

  return (
    <>
      <MenuBar />
      <AnimationsContext>
        <AnimationsCardWrapper />
      </AnimationsContext>
    </>
  );
};

export default AnimationsPage;
