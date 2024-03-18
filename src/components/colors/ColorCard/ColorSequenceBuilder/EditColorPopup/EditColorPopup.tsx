import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Pencil2Icon, TrashIcon } from "@radix-ui/react-icons";
import { Colorful } from "@uiw/react-color";
import { useState } from "react";

export const EditColorPopup: React.FC<{
  hex: string;
  setHex: (hex: string) => void;
  children: any;
  onDelete: () => void
}> = ({ hex, setHex, children, onDelete }) => {

  const [open, setOpen] = useState(false);
  const [color, setColor] = useState(hex);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <div className="relative group">
          {children}
          <Button
            variant={"secondary"}
            size={"icon"}
            className={`w-6 h-6 opacity-100 shrink-0 group-hover:opacity-100 z-10 absolute -top-1 right-1 `}
          >
            <Pencil2Icon className="w-3.5 h-3.5 " />
          </Button>
        </div>
      </PopoverTrigger>
      <PopoverContent className="w-60 h-72">
        <Colorful
          className="w-32 overflow-hidden"
          color={color}
          onChange={(c) => setColor(c.hex)}
        />
        <div className="w-full pt-5 h-12 items-center flex justify-between">
          <Button
            onClick={() => {
              onDelete();
              setOpen(false);
            }}
            size={"icon"}
            variant={"destructive"}
          >
            <TrashIcon />
          </Button>
          <div className="flex items-center space-x-1">
            <Button
              onClick={() => {
                setColor(hex);
                setOpen(false);
              }}
              size={"default"}
              variant={"ghost"}
            >
              Close
            </Button>
            <Button
              size={"default"}
              onClick={() => {
                setHex(color);
                setOpen(false);
              }}
            >
              Save
            </Button>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
};
