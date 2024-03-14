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
import { useAnimationsContext } from "../Context/Context";
import { useState } from "react";
import { Animation } from "@/api/types";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import AnimationCardContext from "../AnimationCardContext";
import { Label } from "@/components/ui/label";
import { startAnimation, updateAnimation } from "@/api/api-calls";
import { toast } from "sonner";

export const AnimationCard: React.FC<{ animation: Animation }> = ({
  animation,
}) => {
  const {
    activeAnimation,
    selectedSequence,
    selectedSection,
    setSelectedSection,
  } = useAnimationsContext();
  const [tab, setTab] = useState<"settings" | "preview">("preview");

  const [variation, setVariation] = useState<string>();
  const [direction, setDirection] = useState<string>();
  const [offset, setOffset] = useState<string>();

  const startAnimationOnclick = async () => {
    const resp = await startAnimation({
      animation_id: animation.id,
      color_sequence_id: selectedSequence.id,
      section_id: selectedSection.id,
    });
    if (resp) {
      if (resp.success) {
        setSelectedSection({ ...selectedSection, isActive: true });
        toast("Started animation!");
      } else {
        toast("Failed to start animation!");
      }
    }
  };

  const updateAnimationOnClick = async () => {
    const resp = await updateAnimation({
      id: animation.id,
      section_id: selectedSection.id,
      name: animation.name,
      description: animation.description,
      variation: variation as unknown as number,
      direction: direction as unknown as number,
      offset: offset as unknown as number,
    });
    if (resp) {
      if (resp.success) {
        toast({
          title: "Updated Animation!",
          duration: 5000,
        });
      } else {
        toast("Failed to update animation!");
      }
    }
  };

  return (
    <AnimationCardContext animation={animation}>
      <Card className="w-full min-w-[384px] max-w-sm">
        <CardHeader className="">
          <div className="flex items-center justify-between">
            <CardTitle className="">{animation.name}</CardTitle>
            {animation == activeAnimation ||
              (false && (
                <div className="h-3 w-3 animate-pulse rounded-full bg-green-400 "></div>
              ))}
          </div>
          <CardDescription>{animation.description}</CardDescription>
        </CardHeader>
        <CardContent>
          {tab === "preview" ? (
            <div className="h-32 w-full">
              <Skeleton className="h-full w-full" />
            </div>
          ) : (
            <div className="h-32 w-full space-y-3">
              <div className="flex w-full justify-between space-x-1">
                <div className="grid w-full gap-1.5">
                  <Label>Variation</Label>
                  <Select onValueChange={setVariation}>
                    <SelectTrigger className="">
                      <SelectValue placeholder="Variation"></SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0">Variant 1</SelectItem>
                      <SelectItem value="1">Variant 2</SelectItem>
                      <SelectItem value="2">Variant 3</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid w-full gap-1.5 ">
                  <Label>Direction</Label>

                  <Select onValueChange={setDirection}>
                    <SelectTrigger className="">
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
                <div className="grid w-full gap-1.5 ">
                  <Label>Direction</Label>

                  <Select onValueChange={setOffset}>
                    <SelectTrigger className="">
                      <SelectValue placeholder="Offset"></SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0">No offset</SelectItem>
                      <SelectItem value="1">One Beat</SelectItem>
                      <SelectItem value="2">Two Beats</SelectItem>
                      <SelectItem value="3">Three Beats</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <Button
                onClick={updateAnimationOnClick}
                className="w-full"
                variant={"secondary"}
              >
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
          <Button onClick={startAnimationOnclick} variant={"default"}>
            Activate
          </Button>
        </CardFooter>
      </Card>
    </AnimationCardContext>
  );
};
