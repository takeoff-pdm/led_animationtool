import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useSetupContext } from "../SetupContext/SetupContext";
import { useState, useEffect } from "react";
import { Switch } from "@/components/ui/switch";
import { Settings } from "@/api/types";
import { getSettings, updateBrightness, updateLedCount } from "@/api/api-calls";

const LabeledInput: React.FC<{
  value: any;
  placeholder: string;
  onChange: (value: string) => void;
  type?: string;
  label: string;
}> = ({ value, placeholder, onChange, label, type }) => {
  return (
    <div className="grid w-full gap-1.5">
      <Label>{label}</Label>
      <Input
        value={value}
        type={type}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
};

export const ConfigManager: React.FC = () => {
  const { settings, setSettings } = useSetupContext();
  const [tempSettings, setTempSettings] = useState<Settings>(settings);

  useEffect(() => {
    const fetchSections = async () => {
      getSettings().then((settings) => {
        setTempSettings({brightness: settings.brightness, led_count: settings.led_count});
      });
    };
    fetchSections();
  }, []);


  return (
    <Card className="max-w-4xl">
      <CardHeader>
        <CardTitle>Configurations</CardTitle>
        <CardDescription>
          It can happen that you need to restart the application to apply the
          new configurations.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <LabeledInput
          value={tempSettings.brightness}
          placeholder="Brightness"
          type="number"
          onChange={(value) =>
            setTempSettings({ ...tempSettings, brightness: parseInt(value) })
          }
          label="Brightness"
        />
        <LabeledInput
          value={tempSettings.led_count}
          placeholder="Led Count"
          type="number"
          onChange={(value) =>
            setTempSettings({ ...tempSettings, led_count: parseInt(value) })
          }
          label="Led Count"
        />
      </CardContent>
      <CardFooter className="justify-end space-x-2">
        {/* <Button
          onClick={() => {
            // TODO: Does not work
            setTempSettings(settings);
          }}
          variant={"ghost"}
        >
          Cancel
        </Button> */}
        <Button
          onClick={() => {
            updateBrightness({ value: tempSettings['brightness'] })
            updateLedCount({ value: tempSettings['led_count'] })
            
            setSettings(tempSettings);
          }}
        >
          Save
        </Button>
      </CardFooter>
    </Card>
  );
};
