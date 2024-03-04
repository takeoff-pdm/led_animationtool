import ColorCard from "../ColorCard";
import { useColorsContext } from "../ColorsContext/ColorsContext";
import MenuBar from "../MenuBar";

export const ColorCardsWrapper: React.FC<{}> = ({}) => {
  const { colorSequences } = useColorsContext();
  return (
    <div className="sm:px-14 px-4">
      <MenuBar />
      <div className="w-full grid gap-5 md:grid-cols-2 xl:grid-cols-3 3xl:grid-cols-4">
        {colorSequences.map((a) => (
          <ColorCard colorSequence={a} />
        ))}
      </div>
    </div>
  );
};
