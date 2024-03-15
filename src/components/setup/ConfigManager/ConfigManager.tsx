import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useSetupContext } from "../SetupContext/SetupContext";
import { useState } from "react";
import { Switch } from "@/components/ui/switch";
import { Settings } from "@/api/types";
import { updateBrightness, updateLedCount } from "@/api/api-calls";


const LabeledInput: React.FC<{
  value: any;
  placeholder: string;
  onChange: (value: string) => void;
  type?: string;
  label: string;
}> = ({ value, placeholder, onChange, label, type }) => {

  const [value1, setValue1] = useState<string>(value);

  return (
    <div className="grid w-full gap-1.5">
      <Label>{label}</Label>
      <div className="flex space-x-2 items-center">
        <Input
          value={value1}
          type={type}
          placeholder={placeholder}
          onChange={(e) => setValue1(e.target.value)}
        />
        <Button onChange={() => {
          setValue1(value);
        }} variant="secondary" size="sm" className="shrink-0 px-5">Cancel</Button>
        <Button onClick={(e) => {
          onChange(value1);
        }} size="sm">Save</Button>
      </div>
      
    </div>
  );
};

export const ConfigManager: React.FC = () => {
  const { settings, setSettings } = useSetupContext();
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
          value={settings.brightness}
          placeholder="Brightness"
          type="number"
          onChange={(value) => {
            setSettings({
              ...settings,
              brightness: parseInt(value)
            });
            updateBrightness(value);
          }}
          label="Brightness"
        />
        <LabeledInput
          value={settings.ledCount}
          placeholder="Led Count"
          type="number"
          onChange={(value) => {
            setSettings({
              ...settings,
              ledCount: parseInt(value)
            });

            updateLedCount(value);
          }}
          label="Led Count"
        />
      </CardContent>
    </Card>
  );
};
