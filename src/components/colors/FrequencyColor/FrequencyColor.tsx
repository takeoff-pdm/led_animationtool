import { useEffect, useState } from "react";
import { toast } from "sonner";

import {
    getColorSequences,
} from "@/api/api-calls";
import { Button } from "@/components/ui/button";
import { ColorSequence, FrequencyColor } from "@/api/types";
import { getFrequencyColors, updateFrequencyColors } from "@/api/api-calls";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";

interface ColorSequencesResponse {
    color_sequences?: ColorSequence[];
}

interface FrequencyColorResponse {
    scene_id: number;
    color_sequence_id_1: number;
    color_sequence_id_2: number;
    color_sequence_id_3: number;
}

const ColorSequenceSelector: any = (selectedSequence: ColorSequence, setSelectedSequence: any) => {
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

export const FrequencyColorCard: React.FC<{}> = ({}) => {
    const [tab, setTab] = useState<"settings" | "preview">("preview");
    const [editMode, setEditMode] = useState<boolean>(false);
    const [frequencyColor, setFrequencyColor] = useState<FrequencyColor>({
        scene_id: -1,
        color_sequence_id_1: 0,
        color_sequence_id_2: 0,
        color_sequence_id_3: 0,
    });
    const [selectedSequence1, setSelectedSequence1] = useState<ColorSequence>();
    const [selectedSequence2, setSelectedSequence2] = useState<ColorSequence>();
    const [selectedSequence3, setSelectedSequence3] = useState<ColorSequence>();

    useEffect(() => {
        getFrequencyColors(-1).then((a: { frequencyColor: FrequencyColor }) => {
            if (!a.frequencyColor) return;
            setFrequencyColor(a.frequencyColor);
        });
    }, []);

    const onUpdate = async () => {
        const success = await updateFrequencyColors(frequencyColor);
        toast(success ? "Color sequence updated" : "Failed to update");
    };

    return (
        <Card className="max-w-sm min-w-[384px] min-h-[330px] w-full">
        <CardHeader className="">
            <CardTitle
            contentEditable={editMode}
            className=""
            >
            Frequency Colors
            </CardTitle>
        </CardHeader>
        <CardContent>

            <ColorSequenceSelector selectedSequence={selectedSequence1} setSelectedSequence={setSelectedSequence1} />
            <ColorSequenceSelector selectedSequence={selectedSequence2} setSelectedSequence={setSelectedSequence2} />
            <ColorSequenceSelector selectedSequence={selectedSequence3} setSelectedSequence={setSelectedSequence3} />
            {/* {tab === "preview" ? (
            <div className="w-full h-40">
                <ColorsPreview colors={colors} />
            </div>
            ) : (
            <div className="w-full min-h-32 space-y-3">
                <div className="w-full flex space-x-1 justify-between">
                <Select onValueChange={(e) => setColorSequenceTemp({
                    ...colorSequenceTemp,
                    selection: e as unknown as number,
                    })}>
                    <SelectTrigger className="w-1/2">
                    <SelectValue placeholder="Selection"></SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                    <SelectItem value="0">Skip all selected</SelectItem>
                    <SelectItem value="1">Skip One</SelectItem>
                    <SelectItem value="2">Skip Two</SelectItem>
                    <SelectItem value="3">Skip Three</SelectItem>
                    <SelectItem value="4">Skip Four</SelectItem>
                    <SelectItem value="5">Skip Five</SelectItem>
                    <SelectItem value="6">Skip Six</SelectItem>
                    <SelectItem value="7">Skip Seven</SelectItem>
                    <SelectItem value="8">Skip Eight</SelectItem>
                    </SelectContent>
                </Select>
                <Select onValueChange={(e) => setColorSequenceTemp({
                    ...colorSequenceTemp,
                    color_amount: e as unknown as number,
                    })}>
                    <SelectTrigger className="w-1/2">
                    <SelectValue placeholder="Color Amount"></SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                    <SelectItem value="1">One</SelectItem>
                    <SelectItem value="2">Two</SelectItem>
                    <SelectItem value="4">Four</SelectItem>
                    <SelectItem value="5">Five</SelectItem>
                    </SelectContent>
                </Select>
                </div>
                <ColorSequenceBuilder
                sequence={colorSequenceTemp}
                colors={colors}
                setColors={setColors}
                /> 
            </div>
            )}*/}
        </CardContent>
        <CardFooter
        className={`flex ${editMode && "mt-8"} justify-between space-x-3`}
        >
        
            <Button onClick={onUpdate} className="" variant={"default"}>
                Update
            </Button>
        </CardFooter>
        </Card>
    );
};
