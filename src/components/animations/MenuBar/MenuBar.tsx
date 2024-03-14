import {
  getColorSequences,
  getSections,
  startAnimation,
  stopAnimation,
  updateBpm,
} from "@/api/api-calls";
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
import { PauseIcon, ResumeIcon } from "@radix-ui/react-icons";
import { toast } from "sonner";

export const MenuBar: React.FC = () => {
  return (
    <div className="min-h-20 w-full items-center justify-between space-y-2 px-4 py-2 lg:flex  lg:px-14">
      <div className="flex w-full space-x-2 lg:mr-2">
        <SectionPauseResumeButton />
        <SectionSelector />
        <ColorSequenceSelector />
      </div>
      <div className="flex w-full">
        <BPMController />
      </div>
    </div>
  );
};

const SectionPauseResumeButton: React.FC = () => {
  const { selectedSection, activeAnimation, selectedSequence } =
    useAnimationsContext();
  const [active, setActive] = useState<boolean>(
    selectedSection.isActive || false,
  );

  const onClick = async () => {
    if (active) {
      const resp = await stopAnimation({
        id: selectedSection.id,
      });
      if (resp.success) {
        setActive(!active);
      } else {
        toast("Failed to stop animation!");
      }
    } else {
      const resp = await startAnimation({
        section_id: selectedSection.id,
        animation_id: activeAnimation ? activeAnimation.id : 0,
        color_sequence_id: selectedSequence.id,
      });
      if (resp.success) {
        setActive(!active);
      } else {
        toast("Failed to start animation!");
      }
    }
  };

  return (
    <div className="mt-5">
      <Button
        //  disabled={!selectedSection.isActive}
        variant={"default"}
        onClick={onClick}
        className="pr-5"
      >
        {active ? (
          <PauseIcon className="h-4 w-4 sm:mr-2" />
        ) : (
          <ResumeIcon className="h-4 w-4 sm:mr-2" />
        )}
        <div className="hidden sm:block">{active ? "Pause" : "Resume"}</div>
      </Button>
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
    const section = sections.find((s) => s.id === parseInt(section_name));
    if (!section) {
      throw new Error("section not found");
    }
    setSelectedSection(section);
  };

  return (
    <div className="grid w-full gap-1.5 lg:w-fit">
      <Label>Sections</Label>
      <Select
        value={JSON.stringify(selectedSection?.id)}
        onValueChange={onSelect}
      >
        <SelectTrigger className="w-full lg:w-56">
          <SelectValue placeholder="Section"></SelectValue>
        </SelectTrigger>
        <SelectContent>
          {sections.map((section) => (
            <SelectItem value={JSON.stringify(section.id)}>
              {section.name}
            </SelectItem>
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

  const { selectedSequence, setSelectedSequence } = useAnimationsContext();

  const onSelect = (section_name: string) => {
    const section = sequences.find((s) => s.id === parseInt(section_name));
    if (!section) {
      throw new Error("section not found");
    }
    setSelectedSequence(section);
  };

  return (
    <div className="grid w-full gap-1.5 lg:w-fit">
      <Label>Sequence</Label>

      <Select
        value={JSON.stringify(selectedSequence?.id)}
        onValueChange={onSelect}
      >
        <SelectTrigger className="w-full lg:w-56">
          <SelectValue placeholder="Sequence"></SelectValue>
        </SelectTrigger>
        <SelectContent>
          {sequences.map((sequence) => (
            <SelectItem value={JSON.stringify(sequence.id)}>
              {sequence.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

const BPMController: React.FC = () => {
  const [bpmValue, setBpmValue] = useState<number>(128);

  const [tapCount, setTapCount] = useState<number>(0);
  const [firstTap, setFirstTap] = useState<number>(0);
  const [lastTap, setLastTap] = useState<number>(0);

  const calculateBpm = () => {
    const avgMs = (lastTap - firstTap) / (tapCount - 1);

    return Math.round((60 * 1000) / avgMs);
  };

  const tapped = (e: any) => {
    setTapCount(tapCount + 1);
    setFirstTap(firstTap || e.timeStamp);
    setLastTap(e.timeStamp);
    setBpmValue(calculateBpm());

    if (tapCount % 5 == 0) {
      updateBpm({
        value: bpmValue,
      });
    }
  };

  const autoDetectBPM = () => {};

  const onSave = () => {
    updateBpm({
      value: bpmValue,
    });
  };

  // call tapped.bind(this) when command + B is pressed

  useEffect(() => {
    window.addEventListener("keydown", (e) => {
      if (e.key === "b" && e.metaKey) {
        tapped({ timeStamp: e.timeStamp });
      }
    });
  }, []);

  return (
    <div className="w-full shrink-0 items-center justify-end space-y-2 pt-3 sm:flex sm:space-x-2 sm:space-y-0">
      <Button
        onClick={tapped.bind(this)}
        className="relative w-full lg:w-52 lg:justify-start"
      >
        BPM Tapper
        <div className="absolute right-4 top-2 ml-2 text-slate-400">⌘ + B</div>
      </Button>
      <div className="flex items-center justify-end space-x-2  ">
        <Button onClick={autoDetectBPM} variant={"secondary"} className="grow">
          Auto Detect
        </Button>
        <Input
          className="w-20"
          placeholder="120"
          value={bpmValue}
          onChange={(e) => {
            setBpmValue(parseInt(e.target.value));
          }}
          type="number"
        />
        <Button
          onClick={() => {
            onSave();
          }}
          className="max-w-40 grow md:max-w-96"
        >
          Save
        </Button>
      </div>
    </div>
  );
};
