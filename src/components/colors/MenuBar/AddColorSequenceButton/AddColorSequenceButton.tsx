import { Button } from "@/components/ui/button";
import { useColorsContext } from "../../ColorsContext/ColorsContext";
import { ColorSequence } from "@/api/types";
import { addColorSequence, getColorSequences } from "@/api/api-calls";

export const AddColorSequenceButton: React.FC = () => {
  const { setColorSequences } = useColorsContext();

  const addNewColorSequence = async () => {
    const newColorSequence: ColorSequence = {
      color_amount: 0,
      description: "add a description",
      name: "New Color Sequence",
      selection: 1,
    } as ColorSequence;

    const response = await addColorSequence(newColorSequence);
    if (response.success) {
      const sequences_data = await getColorSequences();
      if (sequences_data.color_sequences) {
        setColorSequences(sequences_data.color_sequences as ColorSequence[]);
      }
    }
  };

  return (
    <Button
      onClick={() => {
        addNewColorSequence();
      }}
      className="min-w-[200px]:w-full "
    >
      Add Color Sequence
    </Button>
  );
};
