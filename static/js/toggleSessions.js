let ul = document.querySelector("#events").children;

for (let i = 0; i < ul.length; i++) {
	ul[i].addEventListener("click", (e) => {
        try{
            if (e.target.nextElementSibling.tagName === "UL") {
                e.target.parentElement.children[1].classList.toggle("hidden");
            }
        }
        catch{}
	});
}
