interface Section {
  id: number;
  name: string;
  start_led: number;
  end_led: number;
}

interface ColorSequence {
  id: number;
  name: string;
  description: string;
  selection: number;
  color_amount: number;
}

interface Color {
  id: number;
  color_sequence_id: string;
  position: number;
  red: number;
  green: number;
  blue: number;
}

interface Animation {
  id: number;
  section_id: number | null;
  name: string;
  description: string;
  variation: number;
  direction: number;
  offset: number;
}


export type { Animation, Section, Color, ColorSequence };
