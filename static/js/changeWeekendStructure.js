const sprint = document.getElementById("sprint");
const s2 = document.querySelectorAll(".session_2");
const s3 = document.querySelectorAll(".session_3");

sprint.addEventListener("click", () => {
	if (sprint.checked) {
        s2[0].innerText = "Sprint Shootout";
        s2[1].name = "sprint_shootout"
        s3[0].innerText = "Sprint Race";
        s3[1].name = "sprint_race"
	} else {
        s2[0].innerText = "Practice 2";
        s2[1].name = "practice_2"
        s3[0].innerText = "Practice 3";
        s3[1].name = "practice_3"
	}
});
