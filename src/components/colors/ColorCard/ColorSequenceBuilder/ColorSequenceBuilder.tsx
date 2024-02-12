import {
  DndContext,
  useSensor,
  useSensors,
  MouseSensor,
  TouchSensor,
  closestCenter,
  Active,
  PointerSensor,
  KeyboardSensor,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import ColorItem from "./ColorItem";
import { useMemo, useState } from "react";
import SortableColorItem from "./SortableColorItem";
import SortableColorItemOverlay from "./SortableColorItemOverlay";

export const ColorSequenceBuilder: React.FC = () => {
  const [colors, setColors] = useState([
    {
      id: 123,
      blue: 250,
      color_sequence_id: "",
      green: 150,
      position: 0,
      red: 200,
    },
    {
      id: 1244,
      blue: 120,
      color_sequence_id: "",
      green: 150,
      position: 1,
      red: 200,
    },
    // Weitere Farben hier...
  ]);
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

  return (
    <DndContext
      sensors={sensors}
      onDragStart={({ active }) => {
        setActive(active);
      }}
      onDragEnd={({ active, over }) => {
        if (over && active.id !== over?.id) {
          const activeIndex = colors.findIndex(({ id }) => id === active.id);
          const overIndex = colors.findIndex(({ id }) => id === over.id);

          colors[activeIndex].position = overIndex;
          colors[overIndex].position = activeIndex;

          setColors(colors.sort((a, b) => a.position - b.position));
        }
        setActive(null);
      }}
      onDragCancel={() => {
        setActive(null);
      }}
    >
      <SortableContext items={colors}>
        <div className="grid gap-2 grid-cols-5">
          {colors.map((color, index) => (
            <SortableColorItem color={color} />
          ))}
        </div>
      </SortableContext>
      <SortableColorItemOverlay>
        {activeItem && <ColorItem color={activeItem} />}
      </SortableColorItemOverlay>
    </DndContext>
  );
};
