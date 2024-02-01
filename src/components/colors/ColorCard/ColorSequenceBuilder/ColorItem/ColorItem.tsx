import { Color } from "@/api/types";

export const ColorItem: React.FC<{ color: Color }> = ({ color }) => {
  return (
    <div className="h-10 w-10 border p-2">
      <div
        className={`w-5 h-5 rounded-full bg-[rgb(${color.red},${color.green},${color.blue})]`}
      ></div>
    </div>
  );
};
