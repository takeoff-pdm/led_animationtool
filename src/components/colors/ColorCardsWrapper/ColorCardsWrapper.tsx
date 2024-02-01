import ColorCard from "../ColorCard";
import { useColorsContext } from "../ColorsContext/ColorsContext";
import MenuBar from "../MenuBar";

export const ColorCardsWrapper: React.FC<{}> = ({}) => {
  const { colorSequences } = useColorsContext();
  return (
    <div className="sm:px-14 px-4">
      <MenuBar />
      <div className="gap-2 flex w-screen h-screen transition-all flex-col md:flex-row py-0 sm:py-2">
        {colorSequences.map((a) => (
          <ColorCard colorSequence={a} />
        ))}
      </div>
    </div>
  );
};
