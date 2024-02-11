import fetch from "node-fetch";

let url = "http://192.168.178.178:8000"

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

// Animation
function startAnimation(data) {    
    fetch(url + "/api/animate/start", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        return res.json();
    }).then(json => console.log("Request complete! response:", json));
}

// Section
// addSection({name: "Sektion 1", start_led: 60, end_led: 119})
// updateSection({id: 0, name: "Banana", start_led: 2, end_led: 112})
// removeSection({id: 0})

// Color Sequence
// addColorSequence({name: "WeißRotWeiß", description: "Viel weiß wenig rot", selection: 0, color_amount: 1})
// updateColorSequence({id: 0, name: "RotWeißRot", description: "Viel rot wenig weiß", selection: 2, color_amount: 2})
// removeColorSequence({id: 1})

// Animation
// startAnimation({color_sequence_id: 0, animation_id: 0, section_id: 0})
// startAnimation({color_sequence_id: 0, animation_id: 0, section_id: 2})
