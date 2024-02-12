import { Color } from "@/api/types";

export const ColorItem: React.FC<{ color: Color }> = ({ color }) => {
  const backgroundColor = `rgb(${color.red}, ${color.green}, ${color.blue})`;

  return (
    <div className="h-12 rounded-sm shadow-sm w-12 border flex items-center justify-center">
      <div className="w-8 h-8 rounded-full" style={{ backgroundColor }}></div>
    </div>
  );
};
