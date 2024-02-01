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
import { useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export const ColorCard: React.FC<{ colorSequence: ColorSequence }> = ({
  colorSequence,
}) => {
  const [tab, setTab] = useState<"settings" | "preview">("preview");

  return (
    <Card className="max-w-sm min-w-[384px] w-full">
      <CardHeader className="">
        <CardTitle className="">{colorSequence.name}</CardTitle>
        <CardDescription>{colorSequence.description}</CardDescription>
      </CardHeader>
      <CardContent>
        {tab === "preview" ? (
          <div className="w-full h-32">
            <Skeleton className="w-full h-full" />
          </div>
        ) : (
          <div className="w-full h-32 space-y-3">
            <div className="w-full flex space-x-1 justify-between">
              <Select>
                <SelectTrigger className="w-1/2">
                  <SelectValue placeholder="Variation"></SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">Variant 1</SelectItem>
                  <SelectItem value="1">Variant 2</SelectItem>
                  <SelectItem value="2">Variant 3</SelectItem>
                </SelectContent>
              </Select>
              <Select>
                <SelectTrigger className="w-1/2">
                  <SelectValue placeholder="Direction"></SelectValue>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">Normal</SelectItem>
                  <SelectItem value="1">Reverse</SelectItem>
                  <SelectItem value="2">Switching</SelectItem>
                  <SelectItem value="3">Switching 2</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Sequence"></SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="0">Red-Blue</SelectItem>
                <SelectItem value="1">Green-Yellow-Red</SelectItem>
                <SelectItem value="2">Blue-Purple-Yellow</SelectItem>
              </SelectContent>
            </Select>
            <Button className="w-full" variant={"secondary"}>
              Update
            </Button>
          </div>
        )}
      </CardContent>
      <CardFooter className="flex justify-between space-x-3">
        <Button
          onClick={() => setTab(tab === "preview" ? "settings" : "preview")}
          variant={"ghost"}
        >
          {tab === "preview" ? "Settings" : "Preview"}
        </Button>
        <Button variant={"default"}>Activate</Button>
      </CardFooter>
    </Card>
  );
};
