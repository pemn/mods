var ShipBeep = {
	active: true,
	n: 0,
	ac: new AudioContext(),
	beep: function() {
		var oscillator = this.ac.createOscillator();
		oscillator.type = "sine";
		oscillator.frequency.value = 800;
		oscillator.connect(this.ac.destination);
		oscillator.start(); 
		setTimeout(() => oscillator.stop(), 100);
	},
	loop: function() {
		n = document.querySelectorAll("div > span:nth-of-type(3) > span:only-of-type").length
		if (n > this.n) {
			this.beep();
			console.log(n);
		}
		this.n = n;
		if (this.active) {
			setTimeout(this.loop.bind(this), 10000);
		}
	}
}
ShipBeep.loop()
