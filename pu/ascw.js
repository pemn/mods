// apex shipping contract watcher
var ASCW = {
	active: true, n: false, hash: [],
	talk: function(text) {
		speechSynthesis.speak(new SpeechSynthesisUtterance(text));
	},
    look: function(text) {
        if (! this.hash.includes(text)) {
            this.hash.push(text);
            console.log(text);
            if (this.n) {
                let m = text.match("@ [^. ]+")
                if (m) this.talk(m[0]);
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
			setTimeout(this.loop.bind(this), 9999);
		} else {
			this.talk("beep");
            this.n = false;
            this.active = true;
            this.hash.length = 0;
		}
	},
    stop: function() {
        this.active = false;
    }
}
ASCW.loop();
