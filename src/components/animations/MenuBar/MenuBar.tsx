import { ColorSequence, Section } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useState } from "react";

export const MenuBar: React.FC = () => {
  return (
    <div className="w-full min-h-20 space-y-2 py-2 sm:flex justify-between px-14 items-center">
      <div className="space-y-2 sm:space-y-0 sm:flex sm:space-x-5 items-center sm:mr-2">
        <SectionSelector />
        <ColorSequenceSelector />
      </div>
      <BPMController />
    </div>
  );
};

const ColorSequenceSelector: React.FC = () => {
  const [sequences, setSequences] = useState<ColorSequence[]>([]);
  const [selectedSequence, setSelectedSequence] =
    useState<ColorSequence | null>(null);

  const onSelect = (section_name: string) => {
    const section = sequences.find((s) => s.name === section_name);
    if (!section) {
      throw new Error("section not found");
    }
    setSelectedSequence(section);
  };

  return (
    <Select value={selectedSequence?.name} onValueChange={onSelect}>
      <SelectTrigger className="w-56">
        <SelectValue placeholder="Select Sequence"></SelectValue>
      </SelectTrigger>
      <SelectContent>
        {sequences.map((sequence) => (
          <SelectItem value={sequence.name}>{sequence.name}</SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};

const SectionSelector: React.FC = () => {
  const [sections, setSections] = useState<Section[]>([]);
  const [selectedSelection, setSelectedSection] = useState<Section | null>(
    null
  );

  const onSelect = (section_name: string) => {
    const section = sections.find((s) => s.name === section_name);
    if (!section) {
      throw new Error("section not found");
    }
    setSelectedSection(section);
  };

  return (
    <Select value={selectedSelection?.name} onValueChange={onSelect}>
      <SelectTrigger className="w-56">
        <SelectValue placeholder="Select Section"></SelectValue>
      </SelectTrigger>
      <SelectContent>
        {sections.map((section) => (
          <SelectItem value={section.name}>{section.name}</SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};

const BPMController: React.FC = () => {
  const [bpmValue, setBpmValue] = useState<number>(120);

  const autoDetectBPM = () => {};

  const onSave = () => {
    //setBPM to api
  };

  return (
    <div className="flex items-center space-x-2">
      <Input
        className="w-20"
        placeholder="120"
        value={bpmValue}
        onChange={(e) => {
          setBpmValue(parseInt(e.target.value));
        }}
        type="number"
      />
      <Button onClick={autoDetectBPM} variant={"secondary"}>
        Auto Detect
      </Button>
      <Button onClick={onSave}>Save</Button>
    </div>
  );
};
