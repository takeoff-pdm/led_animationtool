let RECEIVER_HOST: string = process.env.RECEIVER_HOST || "";

interface RequestData {
  [key: string]: any;
}

async function sendRequest(
  endpoint: string,
  method: "GET" | "POST",
  data?: RequestData
): Promise<void> {
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
  console.log("Request complete! response:", json);
}

// Section
const addSection = (data: RequestData) =>
  sendRequest("add/section", "POST", data);
const updateSection = (data: RequestData) =>
  sendRequest("update/section", "POST", data);
const removeSection = (data: RequestData) =>
  sendRequest("remove/section", "POST", data);

// ColorSequence
const addColorSequence = (data: RequestData) =>
  sendRequest("add/color_sequence", "POST", data);
const updateColorSequence = (data: RequestData) =>
  sendRequest("update/color_sequence", "POST", data);
const removeColorSequence = (data: RequestData) =>
  sendRequest("remove/color_sequence", "POST", data);

// Color
const getColor = (data: RequestData) => sendRequest("get/color", "GET", data);
const getColorsFromSequence = (data: RequestData) =>
  sendRequest("get/colors_from_sequence", "GET", data);
const addColor = (data: RequestData) => sendRequest("add/color", "POST", data);
const updateColor = (data: RequestData) =>
  sendRequest("update/color", "POST", data);
const removeColor = (data: RequestData) =>
  sendRequest("remove/color", "POST", data);

// Animation
const updateAnimation = (data: RequestData) =>
  sendRequest("update/animation", "POST", data);
const startAnimation = (data: RequestData) =>
  sendRequest("start/animate", "POST", data);
const stopAnimation = (data: RequestData) =>
  sendRequest("stop/animate", "POST", data);

// Settings
const getSettings = () => sendRequest("get/settings", "GET");
const updateBrightness = (data: RequestData) =>
  sendRequest("update/brightness", "POST", data);
const updateLedCount = (data: RequestData) =>
  sendRequest("update/led-count", "POST", data);
const updateBpm = (data: RequestData) =>
  sendRequest("update/bpm", "POST", data);

export {
  addSection,
  updateSection,
  removeSection,
  addColorSequence,
  updateColorSequence,
  removeColorSequence,
  getColor,
  getColorsFromSequence,
  addColor,
  updateColor,
  removeColor,
  updateAnimation,
  startAnimation,
  stopAnimation,
  getSettings,
  updateBrightness,
  updateLedCount,
  updateBpm,
};
