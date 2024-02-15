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

export const ColorSequenceBuilder: React.FC = () => {
  const [colors, setColors] = useState(
    [
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
      {
        id: 1245,
        blue: 50,
        color_sequence_id: "",
        green: 100,
        position: 2,
        red: 150,
      },
      {
        id: 1246,
        blue: 200,
        color_sequence_id: "",
        green: 50,
        position: 3,
        red: 100,
      },
      {
        id: 1247,
        blue: 100,
        color_sequence_id: "",
        green: 200,
        position: 4,
        red: 50,
      },
    ].sort((a, b) => a.position - b.position)
  );
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
