"use client";
import ColorCardsWrapper from "@/components/colors/ColorCardsWrapper";
import ColorsContext from "@/components/colors/ColorsContext";

const ColorsPage: React.FC = () => {
  return (
    <ColorsContext>
      <ColorCardsWrapper />
    </ColorsContext>
  );
};

export default ColorsPage;
