// apex shipping contract watcher
var ASCW = {
	ac: new AudioContext(),	active: true, n: false, hash: [],
	beep: function(wait) {
		var oscillator = this.ac.createOscillator();
		oscillator.type = "sine";
		oscillator.frequency.value = 800;
		oscillator.connect(this.ac.destination);
		oscillator.start(); 
		if (wait === undefined) {
			wait = 100;
		}
		setTimeout(() => oscillator.stop(), wait);
	},
	talk: function(text) {
		speechSynthesis.speak(new SpeechSynthesisUtterance(text));
	},
    look: function(text) {
        if (! this.hash.includes(text)) {
            this.hash.push(text);
            console.log(text);
            if (this.n) {
                this.talk(text.match("@ \\d+")[0])
            }
            this.n = false;
        }
    },
	loop: function() {
		nl = document.querySelectorAll("div[title^='Rating'] + div");
		if (nl.length) {
            for (let i=0;i < nl.length; i++) {
                this.look(nl[i].innerText);
            }
		}
        this.n = true;
		if (this.active) {
			setTimeout(this.loop.bind(this), 10000);
		} else {
			this.beep(200);
		}
	},
    stop: function() {
        this.hash.length = 0;
        this.n = false;
        this.active = false;
    }
}
ASCW.loop();
