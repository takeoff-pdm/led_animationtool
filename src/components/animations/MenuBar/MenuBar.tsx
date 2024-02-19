import { getColorSequences, getSections, updateBpm } from "@/api/api-calls";
import { getAllCollorSequences } from "@/api/colors/get-all";
import { ColorSequence, Section } from "@/api/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useEffect, useState } from "react";
import { useAnimationsContext } from "../Context/Context";

export const MenuBar: React.FC = () => {
  return (
    <div className="w-full min-h-20 space-y-2 py-2 sm:flex justify-between sm:px-14 px-4  items-center">
      <div className="flex space-x-2 sm:mr-2">
        <SectionSelector />
        <ColorSequenceSelector />
      </div>
      <BPMController />
    </div>
  );
};

interface SectionsResponse {
  sections?: Section[];
}

const SectionSelector: React.FC = () => {
  const [sections, setSections] = useState<Section[]>([]);

  useEffect(() => {
    const fetchSections = async () => {
      try {
        const data: SectionsResponse = await getSections();
        // Check if 'data' is not null and 'color_sequences' is present
        if (data && data.sections) {
          // Directly use 'data.color_sequences' to ensure type correctness
          setSections(data.sections);
        }
      } catch (error) {
        console.error("Failed to fetch sections:", error);
        // Handle error (e.g., setting state, showing a message to the user)
      }
    };

    fetchSections();
  }, []);

  const { selectedSection, setSelectedSection } = useAnimationsContext();

  const onSelect = (section_name: string) => {
    const section = sections.find((s) => s.name === section_name);
    if (!section) {
      throw new Error("section not found");
    }
    setSelectedSection(section);
  };

  return (
    <div className="grid gap-1.5">
      <Label>Sections</Label>
      <Select value={selectedSection?.name} onValueChange={onSelect}>
        <SelectTrigger className="sm:w-56 w-1/2">
          <SelectValue placeholder="Select Section"></SelectValue>
        </SelectTrigger>
        <SelectContent>
          {sections.map((section) => (
            <SelectItem value={section.name}>{section.name}</SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

interface ColorSequencesResponse {
  color_sequences?: ColorSequence[];
}

const ColorSequenceSelector: React.FC = () => {
  const [sequences, setSequences] = useState<ColorSequence[]>([]);

  useEffect(() => {
    const fetchColorSequences = async () => {
      try {
        const data: ColorSequencesResponse = await getColorSequences();
        // Check if 'data' is not null and 'color_sequences' is present
        if (data && data.color_sequences) {
          // Directly use 'data.color_sequences' to ensure type correctness
          setSequences(data.color_sequences);
        }
      } catch (error) {
        console.error("Failed to fetch color sequences:", error);
        // Handle error (e.g., setting state, showing a message to the user)
      }
    };

    fetchColorSequences();
  }, []);

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
    <div className="grid gap-1.5">
      <Label>Sequence</Label>

      <Select value={selectedSequence?.name} onValueChange={onSelect}>
        <SelectTrigger className="sm:w-56 w-1/2">
          <SelectValue placeholder="Select Sequence"></SelectValue>
        </SelectTrigger>
        <SelectContent>
          {sequences.map((sequence) => (
            <SelectItem value={sequence.name}>{sequence.name}</SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

const BPMController: React.FC = () => {
  const [bpmValue, setBpmValue] = useState<number>(120);

  const autoDetectBPM = () => {};

  const onSave = () => {
    updateBpm({
      value: bpmValue,
    });
  };

  return (
    <div className="sm:flex items-center sm:space-x-2 space-y-2 md:space-y-0 pt-3">
      <Button className="w-full sm:w-40">BPM Tapper</Button>
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
        <Button
          onClick={() => {
            onSave();
          }}
        >
          Save
        </Button>
      </div>
    </div>
  );
};
