import { Button } from "@/components/ui/button";
import { PlusIcon } from "@radix-ui/react-icons";

export const AddColorButton: React.FC<{
  addColor: () => void;
}> = ({ addColor }) => {
  return (
    <Button onClick={addColor} className="h-12 w-12" size={"icon"} variant={"ghost"}>
      <PlusIcon className="w-4 h-4" />
    </Button>
  );
};
