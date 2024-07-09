const driver = document.getElementById("driver");
let chart;
const getDrivers = async () => {
	const result = await fetch("/getdriver");
	const data = await result.json();
	let option = document.createElement("option");
	option.innerText = " -- Select Driver -- ";
	option.setAttribute("selected", "");
	option.setAttribute("disabled", "");
	driver.append(option);
	for (let i = 0; i < data.length; i++) {
		let option = document.createElement("option");
		option.innerText = data[i][2] + " " + data[i][3] + " " + data[i][4];
		option.setAttribute("value", data[i][0]);
		driver.append(option);
	}
};
getDrivers();

driver.addEventListener("change", () => {
	fetchResults(driver.value);
});

const fetchResults = async (driver_id) => {
	response = await fetch(`/getresult?driver_id=${driver_id}`);
	result = await response.json();
	drawChart(result);
};

counter = 0;
const drawChart = (input) => {
	values = [];
	let data = {
		labels: [1, 2, 3, 4],
		datasets: [
			{
				label: "Driver 1",
				data: [],
				borderWidth: 2,
			},
		],
	};
	for (let i = 0; i < input.length; i++) {
		if (i > 0) {
			values[i] = (input[i][7] !== "" ? input[i][7] : 0) + values[i - 1];
		} else {
			values[i] = input[i][7];
		}
		console.log("changed");
	}
	console.log(input);
	console.log(values);
	data.datasets[0].data = values;
	if (counter > 0) {
		chart.destroy();
	}
	counter++;
	const ctx = document.getElementById("myChart");
	chart = new Chart(ctx, {
		type: "line",
		data: data,
		options: {
			scales: {
				y: {
					beginAtZero: true,
				},
			},
		},
	});
};
