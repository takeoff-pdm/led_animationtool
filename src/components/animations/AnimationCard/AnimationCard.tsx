import { Animation } from "@/api/types";
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

export const AnimationCard: React.FC<{ animation: Animation }> = ({
  animation,
}) => {
  const { loaded, animations, activeAnimation } = useAnimationsContext();

  return (
    <Card className="max-w-sm min-w-[384px] w-full">
      <CardHeader className="">
        <div className="flex items-center justify-between">
          <CardTitle className="">{animation.name}</CardTitle>
          {animation == activeAnimation ||
            (true && (
              <div className="w-3 h-3 rounded-full animate-pulse bg-green-400 "></div>
            ))}
        </div>
        <CardDescription>{animation.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="w-full h-32">
          <Skeleton className="w-full h-full" />
        </div>
      </CardContent>
      <CardFooter className="flex justify-between space-x-3">
        <Button variant={"ghost"}>Settings</Button>
        <Button variant={"default"}>Activate</Button>
      </CardFooter>
    </Card>
  );
};
