interface Animation {
  name: string;
  description: string;
  variation: number;
  direction: number;
  color_sequence: string;
}

interface Section {
  name: string;
  start_led: number;
  end_led: number;
}

interface Color {
  color_sequence: string;
  position: number;
  red: number;
  green: number;
  blue: number;
}

interface ColorSequence {
  name: string;
  description: string;
  selection: 0 | 1 | 2;
  color_amount: number;
}

export type { Animation, Section, Color, ColorSequence };
