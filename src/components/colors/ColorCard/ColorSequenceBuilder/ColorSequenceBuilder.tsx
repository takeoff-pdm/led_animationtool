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
import { Color } from "@/api/types";

export const ColorSequenceBuilder: React.FC<{
  colors: Color[];
  setColors: (colors: Color[]) => void;
}> = ({
  colors, setColors
}) => {
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
            addColor={() => {
              setColors([
                ...colors,
                {
                  id: Math.random(),
                  blue: 0,
                  color_sequence_id: "",
                  green: 0,
                  position: colors.length,
                  red: 0,
                },
              ]);
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
