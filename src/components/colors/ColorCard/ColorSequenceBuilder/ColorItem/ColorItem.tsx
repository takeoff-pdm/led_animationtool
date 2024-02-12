import { Color } from "@/api/types";
import { SortableItemContext } from "../SortableColorItem/SortableColorItem";
import { useContext } from "react";

export const ColorItem: React.FC<{ color: Color }> = ({ color }) => {
  const backgroundColor = `rgb(${color.red}, ${color.green}, ${color.blue})`;
  const { attributes, listeners, ref } = useContext(SortableItemContext);

  return (
    <div
      {...attributes}
      {...listeners}
      ref={ref}
      className="h-12 rounded-sm shadow-sm w-12 border flex items-center justify-center"
    >
      <div className="w-8 h-8 rounded-full" style={{ backgroundColor }}></div>
    </div>
  );
};
