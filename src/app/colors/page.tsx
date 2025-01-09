"use client";
import ColorCardsWrapper from "@/components/colors/ColorCardsWrapper";
import ColorsContext from "@/components/colors/ColorsContext";
import FrequencyColorCard from "@/components/colors/FrequencyColor";

const ColorsPage: React.FC = () => {
  return (
    <>
      <FrequencyColorCard  />

      <ColorsContext>
        <ColorCardsWrapper />
      </ColorsContext>
    </>
  );
};

export default ColorsPage;
