import ColorItem from "./ColorItem";

export const ColorSequenceBuilder: React.FC = () => {
  return (
    <div className="h-32 w-full border rounded grid gap-2 p-1">
      <ColorItem
        color={{
          blue: 250,
          color_sequence: "",
          green: 150,
          position: 2,
          red: 200,
        }}
      />
    </div>
  );
};
