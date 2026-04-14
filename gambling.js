const rollButton = document.getElementById("roll-button");
rollButton.addEventListener("pointerdown", () => {
	fetch("http://127.0.0.1:8000/spin")
		.then(response => response.json())
		.then(data => {
			console.log(data.roll);
			console.log(data.value);
		});
});
