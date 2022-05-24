// apex shipping contract watcher
var ASCW = {
    t: false, n: false, d: [],
    talk: function(text) {
        speechSynthesis.speak(new SpeechSynthesisUtterance(text));
    },
    look: function(text) {
        if (! this.d.includes(text)) {
            this.d.push(text);
            console.log(text);
            if (this.n) {
                let m = text.match("@ ([^. ]+)[^\(]+.([^\)]+)")
                if (m) this.talk("+ " + m[2] + " = " + m[1]);
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
        this.t = setTimeout(this.loop.bind(this), 9999);
    },
    stop: function() {
        if (this.t) {
            clearTimeout(this.t);
            this.t = false;
            this.talk("*");
        }
        this.n = false;
        this.d.length = 0;
    }
}
ASCW.loop();
