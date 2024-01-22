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

export const AnimationCard: React.FC<{ animation: Animation }> = ({
  animation,
}) => {
  return (
    <Card className="max-w-sm min-w-[384px] w-full">
      <CardHeader>
        <CardTitle className="">{animation.name}</CardTitle>
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
