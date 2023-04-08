class QuizTimer {
    constructor() {
        this.timerContainer = document.getElementById('timer-panel');
        this.timeLeft = -1;
        this.updatedAt = new Date();
    }

    setTimer(timeLeft) {
        this.timeLeft = timeLeft;
        this.updatedAt = new Date();
        this.displayTime(this.timeLeft);
        this.updateTimer();
    }

    updateTimer() {
        if (this.timeLeft <= 0) return;

        const timePassed = Math.round((new Date() - this.updatedAt) / 1000);
        let secondsLeft = this.timeLeft - timePassed;
        if (this.secondsLeft < 0)
            this.secondsLeft = -1;

        this.displayTime(secondsLeft);

        if (secondsLeft > 0)
            setTimeout(() => {
                this.updateTimer();
            }, 2000);
    }

    displayTime(timeLeft) {
        let s = '∞';
        if (timeLeft >= 0) {
            s = `${timeLeft}s`;
            if (timeLeft > 100) {
                // format minutes and seconds
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                s = `${minutes}m ${seconds}s`;
            }
        }
        this.timerContainer.innerText = s;
    }
}