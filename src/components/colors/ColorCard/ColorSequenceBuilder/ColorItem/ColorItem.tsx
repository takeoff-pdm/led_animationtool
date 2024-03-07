import { Color } from "@/api/types";
import { SortableItemContext } from "../SortableColorItem/SortableColorItem";
import { useContext, useState } from "react";
import EditColorPopup from "../EditColorPopup";
import hexRgb from "hex-rgb";
import { rgbaToHex } from "@uiw/react-color";
import { updateColor } from "@/api/api-calls";

export const ColorItem: React.FC<{ color: Color }> = ({ color }) => {
  const [backgroundColor, setBackgroundColor] = useState<string>(
    `rgb(${color.red}, ${color.green}, ${color.blue})`
  );
  const { attributes, listeners, ref } = useContext(SortableItemContext);

  return (
    <EditColorPopup
      hex={rgbaToHex({
        r: color.red,
        g: color.green,
        b: color.blue,
        a: 1,
      })}
      setHex={(hex) => {
        const rgbCol = hexRgb(hex);
        setBackgroundColor(
          `rgb(${rgbCol.red}, ${rgbCol.green}, ${rgbCol.blue})`
        );
        updateColor({
          ...color,
          red: rgbCol.red,
          green: rgbCol.green,
          blue: rgbCol.blue,
        });
      }}
    >
      <div
        {...attributes}
        {...listeners}
        ref={ref}
        className="h-12 rounded-sm shadow-sm w-12 border flex items-center justify-center"
      >
        <div className="w-8 h-8 rounded-full" style={{ backgroundColor }}></div>
      </div>
    </EditColorPopup>
  );
};
