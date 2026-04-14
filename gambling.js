const rollButton = document.getElementById("roll-button");
const valueText = document.getElementById("value");
const symbols = [];
for (let i = 1; i < 16; i++) {
	symbols.push(document.getElementById(`symbol${i}`));
}
rollButton.addEventListener("pointerdown", () => {
	fetch("http://127.0.0.1:8000/spin")
		.then(response => response.json())
		.then(data => {
			console.log(data.roll);
			console.log(data.value);

			for (let symbolIndex = 0; symbolIndex < data.roll.length; symbolIndex++) {
				symbols[symbolIndex].src = "./assets/" + data.roll[symbolIndex];
			}

			valueText.textContent = data.value;
		});
});
