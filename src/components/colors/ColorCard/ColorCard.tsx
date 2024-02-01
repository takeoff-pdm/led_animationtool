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

export const ColorCard: React.FC<{ colorSequence: ColorSequence }> = ({
  colorSequence,
}) => {
  const [colorSequenceTemp, setColorSequenceTemp] =
    useState<ColorSequence>(colorSequence);

  const [tab, setTab] = useState<"settings" | "preview">("preview");
  const [editMode, setEditMode] = useState<boolean>(false);

  useEffect(() => {
    if (!editMode) {
      console.log(editMode);
      console.log(colorSequence);
      setColorSequenceTemp(colorSequence);
    }
  }, [editMode]);

  return (
    <Card className="max-w-sm min-w-[384px] h-[330px] w-full">
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
          <div className="w-full h-32 space-y-3">
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
            <ColorSequenceBuilder />
          </div>
        )}
      </CardContent>
      <CardFooter className={`flex ${editMode && "mt-8"} justify-between space-x-3`}>
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
          <Button className="" variant={"default"}>
            Update
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};
