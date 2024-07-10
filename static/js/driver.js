const driver = document.getElementById("driver-list");
const placeholder = document.querySelector(".nothing-selected");
const hidden = document.querySelector(".chart");
let chart;
const getDrivers = async () => {
	const result = await fetch("/getdriver");
	const data = await result.json();
	for (let i = 0; i < data.length; i++) {
		let div = document.createElement("div");
		div.classList.add("inline");
		let checkbox = document.createElement("input");
		checkbox.setAttribute("type", "checkbox");
		checkbox.setAttribute("value", data[i][0]);
		checkbox.setAttribute("id", data[i][0]);
		let label = document.createElement("label");
		label.innerText = data[i][2] + " " + data[i][3] + " " + data[i][4];
		label.setAttribute("value", data[i][0]);
		label.setAttribute("for", data[i][0]);
		div.append(checkbox);
		div.append(label);
		driver.append(div);
		driver.addEventListener("click", (e) => {});
	}
};
getDrivers();
let compareList = [];
driver.addEventListener("click", (e) => {
	if (e.target.tagName !== "LABEL") {
		if (compareList.indexOf(e.target.value) == -1) {
			compareList.push(e.target.value);
		} else {
			compareList.splice(compareList.indexOf(e.target.value), 1);
		}
	}
	fetchResults(compareList);
	if(compareList.length === 0){
		hidden.classList.add("hidden");
		placeholder.classList.remove("hidden");
	}
	else{
		hidden.classList.remove("hidden");
		placeholder.classList.add("hidden");
	}
});

counter = 0;
const drawChart = (input) => {
	let data = [];
	let labels = [1];
	for (let driver of input) {
		let pointsArray = [];
		for (let i = 1; i < driver.length; i++) {
			if (i > 1) {
				if (labels.length < driver.length - 1) {
					labels.push(i);
				}
				pointsArray.push(driver[i] + pointsArray[i - 2]);
			} else {
				pointsArray.push(driver[i]);
			}
		}
		let item = {
			label: driver[0],
			data: pointsArray,
			borderWidth: 2,
		};
		data.push(item);
	}
	// data.datasets[0].data = [];
	if (counter > 0) {
		chart.destroy();
	}
	counter++;

	const ctx = document.getElementById("myChart");

	chart = new Chart(ctx, {
		type: "line",
		data: {
			labels: labels,
			datasets: data,
		},
		options: {
			scales: {
				y: {
					beginAtZero: true,
				},
			},
		},
	});
	labels = [1];
	
};
const fetchResults = async (driverArray) => {
	let data = [];
	for (let driver_id of driverArray) {
		response = await fetch(`/getresult?driver_id=${driver_id}`);
		result = await response.json();
		let driver = [`${result[0][17]} ${result[0][18]}`];
		for (let res of result) {
			driver.push(res[7] == "" ? 0 : res[7]);
		}
		data.push(driver);
	}
	drawChart(data);
};
