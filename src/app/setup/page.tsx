"use client";

import SectionManager from "@/components/setup/SectionManager";
import { SetupContextBuilder } from "@/components/setup/SetupContext/SetupContext";

const Setup: React.FC = () => {
  return (
    <SetupContextBuilder>
      <div className="sm:p-10 w-full p-4 justify-center">
        <SectionManager />
      </div>
    </SetupContextBuilder>
  );
};

export default Setup;
