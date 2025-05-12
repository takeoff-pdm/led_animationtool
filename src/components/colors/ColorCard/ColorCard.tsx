import { Color, ColorSequence } from "@/api/types";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useEffect, useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import ColorSequenceBuilder from "./ColorSequenceBuilder";
import { useColorsContext } from "../ColorsContext/ColorsContext";
import { getColorsFromSequence, updateColorSequence } from "@/api/api-calls";
import { toast } from "sonner";
import { Input } from "@/components/ui/input";

export const ColorCard: React.FC<{ colorSequence: ColorSequence }> = ({
  colorSequence,
}) => {
  const [colorSequenceTemp, setColorSequenceTemp] =
    useState<ColorSequence>(colorSequence);
  const { colorSequences, setColorSequences } = useColorsContext();
  const [tab, setTab] = useState<"settings" | "preview">("preview");
  const [editMode, setEditMode] = useState<boolean>(false);
  const [colors, setColors] = useState([] as Color[]);

  useEffect(() => {
    getColorsFromSequence(colorSequence.id).then((a: { colors: Color[] }) => {
      if (!a.colors) return;
      setColors(a.colors.sort((a, b) => a.position - b.position));
    });
  }, []);

  useEffect(() => {
    if (!editMode) {
      setColorSequenceTemp(colorSequence);
    }
  }, [editMode]);

  const onUpdate = async () => {
    const success = await updateColorSequence(colorSequenceTemp);
    toast(success ? "Color sequence updated" : "Failed to update");
    setColorSequences([
      ...colorSequences.map((item) => {
        if (item.id === colorSequenceTemp.id) {
          return colorSequenceTemp;
        }
        return item;
      }),
    ]);
  };

  return (
    <Card className="max-w-sm min-w-[384px] min-h-[330px] w-full">
      <CardHeader className="">
        <CardTitle
          contentEditable={editMode}
          onInput={(e) => {
            setColorSequenceTemp({
              ...colorSequenceTemp,
              name: e.currentTarget.innerText,
            });
          }}
          className=""
        >
          {(editMode && (
            <Input
              className="h-8 w-full"
              value={colorSequenceTemp.name}
              onChange={(e) =>
                setColorSequenceTemp({
                  ...colorSequenceTemp,
                  name: e.currentTarget.value,
                })
              }
            />
          )) ||
            colorSequenceTemp.name}
        </CardTitle>
        <CardDescription
          contentEditable={editMode}
          onInput={(e) =>
            setColorSequenceTemp({
              ...colorSequenceTemp,
              description: e.currentTarget.innerText,
            })
          }
        >
          {(editMode && (
            <Input
              className="h-8 w-full"
              value={colorSequenceTemp.description}
              onChange={(e) =>
                setColorSequenceTemp({
                  ...colorSequenceTemp,
                  description: e.currentTarget.value,
                })
              }
            />
          )) ||
            colorSequenceTemp.description}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {tab === "preview" ? (
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
              </Select>
              <Select onValueChange={(e) => setColorSequenceTemp({
                  ...colorSequenceTemp,
                  color_amount: e as unknown as number,
                })}>
                <SelectTrigger className="w-1/2">
                  <SelectValue placeholder="Color Amount"></SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">1</SelectItem>
                  <SelectItem value="2">2</SelectItem>
                  <SelectItem value="4">4</SelectItem>
                  <SelectItem value="5">5</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <ColorSequenceBuilder
              sequence={colorSequenceTemp}
              colors={colors}
              setColors={setColors}
            />
          </div>
        )}
      </CardContent>
      <CardFooter
        className={`flex ${editMode && "mt-8"} justify-between space-x-3`}
      >
        <Button
          onClick={() => {
            setEditMode(!editMode);
            setTab(tab === "preview" ? "settings" : "preview");
          }}
          variant={"ghost"}
        >
          {tab === "preview" ? "Settings" : "Preview"}
        </Button>
        {editMode && (
          <Button onClick={onUpdate} className="" variant={"default"}>
            Update
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};

const ColorsPreview: React.FC<{
  colors: Color[];
}> = ({ colors }) => {
  const gradientColors = colors.length === 1 ? [colors[0], colors[0]] : colors;

  //make it a gradient
  const gradient = gradientColors
    .map((color) => `rgb(${color.red}, ${color.green}, ${color.blue})`)
    .join(", ");

  return (
    <div
      className="w-full h-40 rounded-lg"
      style={{
        background: `linear-gradient(to right, ${gradient})`,
      }}
    ></div>
  );
};
