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
import { Skeleton } from "@/components/ui/skeleton";
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
import { getColorsFromSequence } from "@/api/api-calls";

export const ColorCard: React.FC<{ colorSequence: ColorSequence }> = ({
  colorSequence,
}) => {
  const [colorSequenceTemp, setColorSequenceTemp] =
    useState<ColorSequence>(colorSequence);

  const { colorSequences, setColorSequences } = useColorsContext();

  const [tab, setTab] = useState<"settings" | "preview">("preview");
  const [editMode, setEditMode] = useState<boolean>(false);

  const [colors, setColors] = useState([] as Color[]);

  /*[
      {
        id: 123,
        blue: 250,
        color_sequence_id: "",
        green: 150,
        position: 0,
        red: 200,
      },
      {
        id: 1244,
        blue: 120,
        color_sequence_id: "",
        green: 150,
        position: 1,
        red: 200,
      },
    ].sort((a, b) => a.position - b.position)*/

  useEffect(() => {
    getColorsFromSequence(colorSequence.id).then((a: { colors: Color[] }) => {
      setColors(a.colors.sort((a, b) => a.position - b.position));
    });
  }, []);

  useEffect(() => {
    if (!editMode) {
      setColorSequenceTemp(colorSequence);
    }
  }, [editMode]);

  return (
    <Card className="max-w-sm min-w-[384px] min-h-[330px] w-full">
      <CardHeader className="">
        <CardTitle
          contentEditable={editMode}
          onChange={(e) =>
            setColorSequenceTemp({
              ...colorSequenceTemp,
              name: e.currentTarget.innerText,
            })
          }
          className=""
        >
          {colorSequenceTemp.name}
        </CardTitle>
        <CardDescription
          contentEditable={editMode}
          onChange={(e) =>
            setColorSequenceTemp({
              ...colorSequenceTemp,
              description: e.currentTarget.innerText,
            })
          }
        >
          {colorSequenceTemp.description}
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
              <Select>
                <SelectTrigger className="w-1/2">
                  <SelectValue placeholder="Selection"></SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">Regular</SelectItem>
                  <SelectItem value="1">Spectacular</SelectItem>
                  <SelectItem value="2">Random</SelectItem>
                </SelectContent>
              </Select>
              <Select>
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
            <ColorSequenceBuilder colors={colors} setColors={setColors} />
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
          <Button
            onClick={() => {
              setColorSequences([
                ...colorSequences.filter(
                  (item) => item.id !== colorSequenceTemp.id
                ),
                {
                  ...colorSequenceTemp,
                },
              ]);
            }}
            className=""
            variant={"default"}
          >
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
  //make it a gradient
  const gradient = colors
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
