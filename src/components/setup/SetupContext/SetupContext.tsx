import { getSettings } from "@/api/api-calls";
import { Settings } from "@/api/types";
import { createContext, useContext, useEffect, useState } from "react";

const SetupContext = createContext<{
  settings: Settings;
  setSettings: (settings: Settings) => void;
}>({
  settings: {} as Settings,
  setSettings: () => {},
});

export const useSetupContext = () => {
  const context = useContext(SetupContext);
  if (!context) {
    throw new Error(
      "useSetupContext must be used within a SetupContextProvider"
    );
  }
  return context;
};

export const SetupContextBuilder: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  const [settings, setSettings] = useState<Settings>({} as Settings);

  useEffect(() => {
    const fetchSettings = async () => {
      const settings = await getSettings();
      setSettings(settings);
    };

    fetchSettings();
  }, []);

  return (
    <SetupContext.Provider value={{ settings, setSettings }}>
      {children}
    </SetupContext.Provider>
  );
};
