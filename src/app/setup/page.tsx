"use client";

import ConfigManager from "@/components/setup/ConfigManager";
import SectionManager from "@/components/setup/SectionManager";
import { SetupContextBuilder } from "@/components/setup/SetupContext/SetupContext";

const Setup: React.FC = () => {
  return (
    <SetupContextBuilder>
      <div className="w-full justify-center space-y-4 p-4 sm:p-10">
        <SectionManager />
        <ConfigManager />
      </div>
    </SetupContextBuilder>
  );
};

export default Setup;
