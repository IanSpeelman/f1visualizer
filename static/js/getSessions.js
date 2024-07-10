const event = document.getElementById("event");
const session = document.getElementById("session");

event.addEventListener("change", async () => {
	const sessionList = await getSessions(event.value);
	makeOptions(sessionList);
});

const getSessions = async (event_id) => {
	let url = `/sessions?event=${event_id}`;
	const response = await fetch(url);
	const sessions = await response.json();
	return sessions;
};

const makeOptions = (sessions) => {
	while (session.firstChild) {
		session.removeChild(session.lastChild);
	}
	const option = document.createElement("option");
	option.innerText = " -- Select session -- ";
	option.setAttribute("disabled", "");
	option.setAttribute("selected", "");
	session.append(option);
	for (let i = 0; i < sessions.length; i++) {
		const option = document.createElement("option");
		option.innerText = sessions[i][2];
		option.value = sessions[i][0];
		session.append(option);
	}
};
