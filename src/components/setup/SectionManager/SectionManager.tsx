import { addSection, getSections, removeSection } from "@/api/api-calls";
import { Section } from "@/api/types";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  EnterFullScreenIcon,
  PlusIcon,
  TrashIcon,
} from "@radix-ui/react-icons";
import { useState, useEffect } from "react";
import { useSetupContext } from "../SetupContext/SetupContext";
import { toast } from "sonner";

export const SectionManager: React.FC = () => {
  const [editedSections, setEditedSections] = useState<Section[]>([]);
  const [sections, setSections] = useState<Section[]>([]);

  useEffect(() => {
    const fetchSections = async () => {
      getSections().then((sections) => {
        setEditedSections(sections.sections);
      });
    };
    fetchSections();
  }, []);

  const addSectionOnClick = async () => {
    let id = Math.trunc(Math.random() * 1000000);
    let newSection = {
      id: id,
      name: "Section " + id,
      isActive: false,
      start_led: -1,
      end_led: -1,
    };

    addSection(newSection);

    setEditedSections([...editedSections, newSection]);
  };

  const onChange = (section: Section) => {
    setEditedSections(
      editedSections.map((s) => (s.id === section.id ? section : s))
    );
  };

  const onDelete = async (section: Section) => {
    // alert to confirm
    if (!confirm("Are you sure you want to delete this section?")) return;
    setEditedSections(editedSections.filter((s) => s.id !== section.id));
    const resp = await removeSection(section);
    if (resp.success) {
      setSections(sections.filter((s) => s.id !== section.id));
    } else {
      toast("Failed to remove section");
    }
  };

  const onUpdate = () => {
    setSections(editedSections);
  };

  const onCancel = () => {
    setEditedSections(sections);
  };

  return (
    <Card className="max-w-md min-h-72">
      <CardHeader>
        <CardTitle>Setup Sections</CardTitle>
        <CardDescription>Manage your sections.</CardDescription>
      </CardHeader>
      <CardContent>
        {editedSections.length === 0 ? (
          <PlaceHolder />
        ) : (
          <div className="space-y-2">
            {editedSections.map((section) => (
              <SectionItem
                onDelete={() => onDelete(section)}
                onChange={onChange}
                key={section.id}
                section={section}
              />
            ))}
          </div>
        )}
      </CardContent>
      <CardFooter className="w-full justify-center flex space-x-3">
        <Button onClick={onCancel} variant="ghost">
          Cancel
        </Button>
        <Button
          variant={"secondary"}
          onClick={addSectionOnClick}
          className="max-w-xs w-full"
        >
          <PlusIcon className="w-4 h-4 mr-2" />
          Add Section
        </Button>
        <Button onClick={onUpdate} variant={"default"}>
          Update
        </Button>
      </CardFooter>
    </Card>
  );
};

const PlaceHolder: React.FC = () => {
  return (
    <div className="w-full h-40 flex justify-center items-center flex-col">
      <EnterFullScreenIcon className="w-6 h-6" />
      <span className="ml-2 text-slate-600 mt-5">No sections found</span>
    </div>
  );
};

const SectionItem: React.FC<{
  section: Section;
  onChange: (section: Section) => void;
  onDelete: () => void;
}> = ({ section, onChange, onDelete }) => {
  const { settings } = useSetupContext();

  return (
    <div className="w-full h-12 rounded flex items-center  space-x-2 justify-between">
      <Input
        className="w-full"
        value={section.name}
        onChange={(e) =>
          onChange({
            ...section,
            name: e.currentTarget.value,
          })
        }
      />
      <div className="flex space-x-2">
        <Input
          min={0}
          className="w-20"
          value={section.start_led}
          type="number"
          onChange={(e) =>
            onChange({
              ...section,
              start_led: parseInt(e.currentTarget.value),
            })
          }
        />
        <Input
          max={settings.led_count}
          className="w-20"
          type="number"
          value={section.end_led}
          onChange={(e) =>
            onChange({
              ...section,
              end_led: parseInt(e.currentTarget.value),
            })
          }
        />
        <Button
          onClick={onDelete}
          className=""
          variant={"destructive"}
          size={"icon"}
        >
          <TrashIcon />
        </Button>
      </div>
    </div>
  );
};
