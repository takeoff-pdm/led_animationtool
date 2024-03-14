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
import { useState } from "react";
import { Switch } from "@/components/ui/switch";
import { Settings } from "@/api/types";

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
          value={tempSettings.ledCount}
          placeholder="Led Count"
          type="number"
          onChange={(value) =>
            setTempSettings({ ...tempSettings, ledCount: parseInt(value) })
          }
          label="Led Count"
        />
        <LabeledInput
          value={tempSettings.pin}
          placeholder="Pin"
          type="number"
          onChange={(value) =>
            setTempSettings({ ...tempSettings, pin: parseInt(value) })
          }
          label="Pin"
        />
        <LabeledInput
          value={tempSettings.frequency}
          placeholder="Frequency"
          type="number"
          onChange={(value) =>
            setTempSettings({ ...tempSettings, frequency: parseInt(value) })
          }
          label="Frequency"
        />
        <LabeledInput
          value={tempSettings.dma}
          placeholder="DMA"
          type="number"
          onChange={(value) =>
            setTempSettings({ ...tempSettings, dma: parseInt(value) })
          }
          label="DMA"
        />

        <LabeledInput
          value={tempSettings.channel}
          placeholder="Channel"
          type="number"
          onChange={(value) =>
            setTempSettings({ ...tempSettings, channel: parseInt(value) })
          }
          label="Channel"
        />
        <div className="grid w-full gap-1.5">
          <Label>Invert LED</Label>
          <Switch
            checked={tempSettings.led_invert}
            onChange={(value) =>
              setTempSettings({ ...tempSettings, invert: value })
            }
          />
        </div>
      </CardContent>
      <CardFooter className="justify-end space-x-2">
        <Button
          onClick={() => {
            // TODO: Does not work
            setTempSettings(settings);
          }}
          variant={"ghost"}
        >
          Cancel
        </Button>
        <Button
          onClick={() => {
            // TODO: SEND TO API
            setSettings(tempSettings);
          }}
        >
          Save
        </Button>
      </CardFooter>
    </Card>
  );
};
