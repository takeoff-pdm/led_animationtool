import { Animation, Color, ColorSequence, Section } from "./types";

let RECEIVER_HOST: string = process.env.RECEIVER_HOSTNAME || "";

interface RequestData {
  [key: string]: any;
}

interface SettingsValueData {
  value: number;
}

async function sendRequest(
  endpoint: string,
  method: "GET" | "POST",
  data?: RequestData
): Promise<any> {
  const url = `${RECEIVER_HOST}/api/${endpoint}`;
  const options: RequestInit = {
    method: method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  };
  if (method === "GET") {
    delete options.body;
  }
  const response = await fetch(url, options);
  const json = await response.json();
  return json;
}

// Section
const getSections = () => sendRequest("get/sections", "GET");
const addSection = (data: Section) => sendRequest("add/section", "POST", data);
const updateSection = (data: Section) =>
  sendRequest("update/section", "POST", data);
const removeSection = (data: Section) =>
  sendRequest("remove/section", "POST", data);

// ColorSequence
const getColorSequences = () => sendRequest("get/color_sequences", "GET");
const addColorSequence = (data: ColorSequence) =>
  sendRequest("add/color_sequence", "POST", data);
const updateColorSequence = (data: ColorSequence) =>
  sendRequest("update/color_sequence", "POST", data);
const removeColorSequence = (data: ColorSequence) =>
  sendRequest("remove/color_sequence", "POST", data);

// Color
const getColor = (data: Color) => sendRequest("get/color", "GET", data);
const getColorsFromSequence = (data: ColorSequence) =>
  sendRequest("get/colors_from_sequence", "GET", data);
const addColor = (data: Color) => sendRequest("add/color", "POST", data);
const updateColor = (data: Color) => sendRequest("update/color", "POST", data);
const removeColor = (data: Color) => sendRequest("remove/color", "POST", data);

// Animation
const getAnimations = () => sendRequest("get/animations", "GET");
const getAnimation = (data: { id: number }) =>
  sendRequest("get/animation", "POST", data);
const updateAnimation = (data: Animation) =>
  sendRequest("update/animation", "POST", data);
const startAnimation = (data: Animation) =>
  sendRequest("start/animate", "POST", data);
const stopAnimation = (data: Animation) =>
  sendRequest("stop/animate", "POST", data);

// Settings
const getSettings = () => sendRequest("get/settings", "GET");
// { value: 80 }
const updateBrightness = (data: SettingsValueData) =>
  sendRequest("update/brightness", "POST", data);
// { value: 80 }
const updateLedCount = (data: SettingsValueData) =>
  sendRequest("update/led-count", "POST", data);
// { value: 145 }
const updateBpm = (data: SettingsValueData) =>
  sendRequest("update/bpm", "POST", data);

export {
  getSections,
  addSection,
  updateSection,
  removeSection,
  getColorSequences,
  addColorSequence,
  updateColorSequence,
  removeColorSequence,
  getColor,
  getColorsFromSequence,
  addColor,
  updateColor,
  removeColor,
  getAnimations,
  getAnimation,
  updateAnimation,
  startAnimation,
  stopAnimation,
  getSettings,
  updateBrightness,
  updateLedCount,
  updateBpm,
};
