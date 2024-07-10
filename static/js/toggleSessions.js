let events = document.querySelector("#events");

const getEvents = async () => {
	let response = await fetch("/getEvents");
	let results = await response.json();
	let eventNum = -1;
	sessionCount = 0;
	let ul = document.createElement("ul");
	let div = document.createElement("div");
	for (result of results) {
		let li = document.createElement("li");
		if (eventNum !== result[0]) {
			ul.classList.add("hidden");
			div.append(ul);
			events.append(div);
			div = document.createElement("div");
			ul = document.createElement("ul");
			li.innerText = result[1];
			div.append(li);
			eventNum = result[0];
		}

		let innerli = document.createElement("li");
		innerli.innerText = result[6];
		innerli.setAttribute("id", result[4]);
		ul.append(innerli);
	}
	ul.classList.add("hidden");
	div.append(ul);
	events.append(div);
	for (let i = 0; i < events.children.length; i++) {
		events.children[i].addEventListener("click", (e) => {
			if (!e.target.id == "") {
				getResults(e.target.id);
			}
			try {
				if (e.target.nextElementSibling.tagName === "UL") {
					e.target.parentElement.children[1].classList.toggle("hidden");
				}
			} catch {}
		});
	}
};
getEvents();

const getResults = async (session_id) => {
	const table = document.querySelector(".table-results");
	const placeholder = document.querySelector(".nothing-selected");
	console.log(`yep loading results for ${session_id}`);
	url = `/getsessionresults?session_id=${session_id}`;
	const response = await fetch(url);
	const results = await response.json();
	console.log(table.children[0].children.length);
	for (let i = table.children[0].children.length - 1; i > 0 ; i--) {
		table.children[0].children[i].remove();
	}
	for (let i = 0; i < results.length; i++) {
		let td = document.createElement("td");
		let tr = document.createElement("tr");
		td.innerText = results[i][4];
		tr.append(td);
		td = document.createElement("td");
		td.innerText = results[i][16];
		tr.append(td);
		td = document.createElement("td");
		td.innerText = `${results[i][17]} ${results[i][18]}`;
		tr.append(td);
		td = document.createElement("td");
		td.innerText = results[i][24];
		tr.append(td);
		td = document.createElement("td");
		td.innerText = results[i][5];
		tr.append(td);
		td = document.createElement("td");
		td.innerText = results[i][8];
		tr.append(td);
		td = document.createElement("td");
		td.innerText = results[i][10];
		tr.append(td);
		td = document.createElement("td");
		td.innerText = results[i][11];
		tr.append(td);
		td = document.createElement("td");
		td.innerText = results[i][7];
		tr.append(td);
		td = document.createElement("td");
		td.innerText = results[i][12];
		tr.append(td);
		td = document.createElement("td");
		table.children[0].append(tr);
	}
	table.classList.remove("hidden");
	placeholder.classList.add("hidden");
};
