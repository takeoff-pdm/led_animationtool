"use client";
import AnimationPreview from "@/components/animations/AnimationPreview";
import { FlowAnimation } from "@/components/animations/AnimationPreview/FlowAnimation/FlowAnimation";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <AnimationPreview brightness={100} led_count={30}>
        <FlowAnimation
          colors={[
            {
              id: 1,
              blue: 0,
              green: 255,
              red: 0,
              color_sequence_id: 1,
              position: 0,
            },
            {
              id: 8,
              blue: 0,
              green: 0,
              red: 0,
              color_sequence_id: 1,
              position: 0,
            },
            {
              id: 2,
              blue: 143,
              green: 200,
              red: 0,
              color_sequence_id: 1,
              position: 0,
            },
            {
              id: 7,
              blue: 0,
              green: 0,
              red: 0,
              color_sequence_id: 1,
              position: 0,
            },
            {
              id: 3,
              blue: 0,
              green: 10,
              red: 155,
              color_sequence_id: 1,
              position: 0,
            },
            {
              id: 6,
              blue: 0,
              green: 0,
              red: 0,
              color_sequence_id: 1,
              position: 0,
            },
            {
              id: 4,
              blue: 52,
              green: 13,
              red: 100,
              color_sequence_id: 1,
              position: 0,
            },
            {
              id: 5,
              blue: 0,
              green: 0,
              red: 0,
              color_sequence_id: 1,
              position: 0,
            },
          ]}
          bpm={50}
        />
      </AnimationPreview>
    </main>
  );
}
