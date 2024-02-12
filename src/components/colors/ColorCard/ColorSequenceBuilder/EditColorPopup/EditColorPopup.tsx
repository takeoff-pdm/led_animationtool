import { Button } from "@/components/ui/button";
import { Pencil1Icon, Pencil2Icon, PlusIcon } from "@radix-ui/react-icons";
import { Colorful } from "@uiw/react-color";
import { useState } from "react";

export const EditColorPopup: React.FC<{
  hex: string;
  setHex: (hex: string) => void;
  children: any;
}> = ({ hex, setHex, children }) => {
  // TODO: Save on change
  const [hidden, setHidden] = useState<boolean>(false);
  return (
    <div onClick={() => setHidden(!hidden)} className="relative group">
      {children}
      <Button
        variant={"secondary"}
        size={"icon"}
        className={`w-6 h-6 ${
          !hidden ? "opacity-50" : "opacity-100"
        } shrink-0 group-hover:opacity-100 z-10 absolute -top-1 right-1 `}
      >
        <Pencil2Icon className="w-3.5 h-3.5 " />
      </Button>
      <div className={`${!hidden && "hidden"}`}>
        <Colorful color={hex} onChange={(c) => setHex(c.hex)} />
      </div>
    </div>
  );
};
