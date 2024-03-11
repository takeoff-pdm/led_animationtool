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
import { useToast } from "@/components/ui/use-toast";

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
  const { toast } = useToast();

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
        toast({
          title: "Started animation!",
          duration: 5000,
        });
      } else {
        toast({
          title: "Failed to start animation!",
          variant: "destructive",
          duration: 6000,
        });
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
        toast({
          title: "Failed to update animation!",
          variant: "destructive",
          duration: 6000,
        });
      }
    }
  };

  return (
    <AnimationCardContext animation={animation}>
      <Card className="max-w-sm min-w-[384px] w-full">
        <CardHeader className="">
          <div className="flex items-center justify-between">
            <CardTitle className="">{animation.name}</CardTitle>
            {animation == activeAnimation ||
              (false && (
                <div className="w-3 h-3 rounded-full animate-pulse bg-green-400 "></div>
              ))}
          </div>
          <CardDescription>{animation.description}</CardDescription>
        </CardHeader>
        <CardContent>
          {tab === "preview" ? (
            <div className="w-full h-32">
              <Skeleton className="w-full h-full" />
            </div>
          ) : (
            <div className="w-full h-32 space-y-3">
              <div className="w-full flex space-x-1 justify-between">
                <div className="grid gap-1.5 w-full">
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
                <div className="grid gap-1.5 w-full ">
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
                <div className="grid gap-1.5 w-full ">
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
