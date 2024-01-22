import fetch from "node-fetch";

// // add
// let data = {name: "Sektion 1", start_led: 0, end_led: 119};

// fetch("http://192.168.178.178:8000/api/add/section", {
//   method: "POST",
//   headers: {'Content-Type': 'application/json'}, 
//   body: JSON.stringify(data)
// }).then(res => {
//   console.log("Request complete! response:", res);
// });

// // remove
// let data2 = {name: "Banana"};

// fetch("http://192.168.178.178:8000/api/remove/section", {
//   method: "POST",
//   headers: {'Content-Type': 'application/json'}, 
//   body: JSON.stringify(data2)
// }).then(res => {
//   console.log("Request complete! response:", res);
// });

// update
let data3 = {old_name: "Sektion 1", name: "Banana", start_led: 2, end_led: 112};

fetch("http://192.168.178.178:8000/api/update/section", {
  method: "POST",
  headers: {'Content-Type': 'application/json'}, 
  body: JSON.stringify(data3)
}).then(res => {
  console.log("Request complete! response:", res);
});
