interface Section {
  id: number;
  name: string;
  start_led: number;
  end_led: number;
  isActive?: boolean;
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

interface Settings {
  brightness: number;
  led_count: number;
  element_length: number;
  pin: number;
  frequency: number;
  dma: number;
  led_invert: boolean;
  channel: number;
  bpm: number;
}

export type { Animation, Section, Color, ColorSequence, Settings };
