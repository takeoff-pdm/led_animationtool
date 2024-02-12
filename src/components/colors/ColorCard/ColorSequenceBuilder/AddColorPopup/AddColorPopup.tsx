import { Button } from "@/components/ui/button";
import { PlusIcon } from "@radix-ui/react-icons";

export const AddColorPopup: React.FC = () => {
  return (
    <Button className="" size={"icon"}>
      <PlusIcon className="w-4 h-4" />
    </Button>
  );
};
