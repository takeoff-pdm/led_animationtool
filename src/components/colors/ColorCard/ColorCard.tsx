import { ColorSequence } from "@/api/types";
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

export const ColorCard: React.FC<{ colorSequence: ColorSequence }> = ({
  colorSequence,
}) => {
  const [colorSequenceTemp, setColorSequenceTemp] =
    useState<ColorSequence>(colorSequence);

  const { colorSequences, setColorSequences } = useColorsContext();

  const [tab, setTab] = useState<"settings" | "preview">("preview");
  const [editMode, setEditMode] = useState<boolean>(false);

  const [colors, setColors] = useState(
    [
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
      {
        id: 1245,
        blue: 50,
        color_sequence_id: "",
        green: 100,
        position: 2,
        red: 150,
      },
      {
        id: 1246,
        blue: 200,
        color_sequence_id: "",
        green: 50,
        position: 3,
        red: 100,
      },
      {
        id: 1247,
        blue: 100,
        color_sequence_id: "",
        green: 200,
        position: 4,
        red: 50,
      },
    ].sort((a, b) => a.position - b.position)
  );

  useEffect(() => {
    if (!editMode) {
      setColorSequenceTemp(colorSequence);
    }
  }, [editMode]);

  return (
    <Card className="max-w-sm min-w-[384px] overflow-scroll h-[330px] w-full">
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
            <Skeleton className="w-full h-full" />
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
