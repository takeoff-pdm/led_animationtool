import {
  DndContext,
  useSensor,
  useSensors,
  Active,
  PointerSensor,
  KeyboardSensor,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
} from "@dnd-kit/sortable";
import ColorItem from "./ColorItem";
import { useMemo, useState } from "react";
import SortableColorItem from "./SortableColorItem";
import SortableColorItemOverlay from "./SortableColorItemOverlay";
import AddColorButton from "../../AddColorButton";
import { Color, ColorSequence } from "@/api/types";
import { addColor } from "@/api/api-calls";

export const ColorSequenceBuilder: React.FC<{
  sequence: ColorSequence;
  colors: Color[];
  setColors: (colors: Color[]) => void;
}> = ({ sequence, colors, setColors }) => {
  const [active, setActive] = useState<Active | null>(null);
  const activeItem = useMemo(
    () => colors.find((item) => item.id === active?.id),
    [active, colors]
  );
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: any) => {
    const { active, over } = event;
    if (over && active.id !== over?.id) {
      const activeIndex = colors.findIndex(({ id }) => id === active.id);
      const overIndex = colors.findIndex(({ id }) => id === over.id);
      setColors(arrayMove(colors, activeIndex, overIndex));
    }
  };

  return (
    <DndContext
      sensors={sensors}
      onDragStart={({ active }) => {
        setActive(active);
      }}
      onDragEnd={handleDragEnd}
      onDragCancel={() => {
        setActive(null);
      }}
    >
      <SortableContext items={colors}>
        <div className="grid gap-2 grid-cols-5">
          {colors.map((color, index) => (
            <SortableColorItem key={color.id} color={color} />
          ))}
          <AddColorButton
            addColor={async () => {
              const lastColor = colors[colors.length - 1];
              const newColor = {
                id: Math.trunc(Math.random() * 1000000),
                color_sequence_id: JSON.stringify(sequence.id),
                position: lastColor.position + 1,
                red: Math.trunc(Math.random() * 255),
                green: Math.trunc(Math.random() * 255),
                blue: Math.trunc(Math.random() * 255),
              };
              const resp = await addColor(newColor);
              if (resp.success) {
                setColors([...colors, newColor]);
              }
            }}
          />
        </div>
      </SortableContext>
      <SortableColorItemOverlay>
        {activeItem && <ColorItem color={activeItem} />}
      </SortableColorItemOverlay>
    </DndContext>
  );
};
