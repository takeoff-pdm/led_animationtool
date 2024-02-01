import { Button } from "@/components/ui/button";
import { useColorsContext } from "../../ColorsContext/ColorsContext";
import { ColorSequence } from "@/api/types";

export const AddColorSequenceButton: React.FC = () => {
  const { colorSequences, setColorSequences } = useColorsContext();

  const addNewColorSequence = () => {
    setColorSequences([
      ...colorSequences,
      {
        color_amount: 0,
        description: "add a description",
        name: "New Color Sequence",
        selection: 1,
      } as ColorSequence,
    ]);
  };

  return (
    <Button onClick={addNewColorSequence} className="min-w-[200px]:w-full ">
      Add Color Sequence
    </Button>
  );
};
