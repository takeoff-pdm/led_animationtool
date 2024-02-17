import fetch from "node-fetch";

let url = "http://0.0.0.0:8000"

// Section
function addSection(data) {
    fetch(url + "/api/add/section", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function updateSection(data) {
    fetch(url + "/api/update/section", {
    method: "POST",
    headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify(data)
    }).then(res => {
    return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function removeSection(data) {
    fetch(url + "/api/remove/section", {
    method: "POST",
    headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify(data)
    }).then(res => {
    return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

// ColorSequence
function addColorSequence(data) {    
    fetch(url + "/api/add/color_sequence", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function updateColorSequence(data) {
    fetch(url + "/api/update/color_sequence", {
    method: "POST",
    headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify(data)
    }).then(res => {
    return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function removeColorSequence(data) {
    fetch(url + "/api/remove/color_sequence", {
    method: "POST",
    headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify(data)
    }).then(res => {
    return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

// Color
function getColor(data) {    
    fetch(url + "/api/get/color", {
        method: "GET",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}
function getColorsFromSequence(data) {    
    fetch(url + "/api/get/colors_from_sequence", {
        method: "GET",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function addColor(data) {    
    fetch(url + "/api/add/color", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function updateColor(data) {
    fetch(url + "/api/update/color", {
    method: "POST",
    headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify(data)
    }).then(res => {
    return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function removeColor(data) {
    fetch(url + "/api/remove/color", {
    method: "POST",
    headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify(data)
    }).then(res => {
    return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

// Animation
function updateAnimation(data) {    
    fetch(url + "/api/update/animation", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function startAnimation(data) {    
    fetch(url + "/api/start/animate", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function stopAnimation(data) {    
    fetch(url + "/api/stop/animate", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

// Settings
function getSettings() {    
    fetch(url + "/api/get/settings", {
        method: "GET",
        headers: {'Content-Type': 'application/json'}
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function updateBrightness(data) {    
    fetch(url + "/api/update/brightness", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function updateLedCount(data) {    
    fetch(url + "/api/update/led-count", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

function updateBpm(data) {    
    fetch(url + "/api/update/bpm", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

// Section
// addSection({name: "Sektion 1", start_led: 0, end_led: 60})
// updateSection({id: 0, name: "Banana", start_led: 0, end_led: 59})
// removeSection({id: 0})

// Color Sequence
// addColorSequence({name: "Marlene", description: "halt Marlene", selection: 0, color_amount: 1})
// updateColorSequence({id: 2, name: "Random", description: "halt random", selection: 0, color_amount: 3})
// removeColorSequence({id: 1})

// Color
// addColor({ color_sequence_id: 2, red: 10, green: 120, blue: 255 })
// removeColor({ id: 16 })
// updateColor({ id: 1, color_sequence_id: 0, position: 1, red: 0, green: 0, blue: 255 })

// Animation
// updateAnimation({ id: 0, name: 'MonoColor', description: 'Monochromatic color switching (different sections possible)', variation: 1, direction: 0 })
// updateAnimation({ id: 1, name: 'Flow', description: 'Flow gliding through the pixels', variation: 0, direction: 0 })
// startAnimation({color_sequence_id: 2, animation_id: 1, section_id: 0})
// startAnimation({color_sequence_id: 0, animation_id: 0, section_id: 0})
// stopAnimation({ id: 0 }) // Id is section_id

// Settings
// getSettings()
// updateBrightness({ value: 80 })
// updateLedCount({ value: 100 })
// updateBpm({ value: 10 })
// getSettings()
