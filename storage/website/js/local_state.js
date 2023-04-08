class LocalStateManager {
    constructor() {
        this._userName = null;
        this._lastAnswer = null;
    }

    get userName() {
        if (this._userName === null)
            this._userName = window.localStorage.getItem('quizz_username', '');
        return this._userName;
    }

    set userName(value) {
        if (this._userName == value)
            return;
        this._userName = value;
        window.localStorage.setItem('quizz_username', value);
    }

    get lastAnswer() {
        if (this._lastAnswer === null) {
            const lastAnswerJson = window.localStorage.getItem('quizz_last_answer', '');
            this._lastAnswer = lastAnswerJson ? JSON.parse(lastAnswerJson) : null;
        }
        return this._lastAnswer;
    }

    set lastAnswer(value) {
        this._lastAnswer = value;
        window.localStorage.setItem('quizz_last_answer', JSON.stringify(value));
    }

    storeQuizState(quizState) {
        let state = quizState;
        if (state)
            state = JSON.stringify(state);
        window.localStorage.setItem('quizz_state', state);
    }

    readQuizState() {
        const dataStr = window.localStorage.getItem('quizz_state', '');
        return JSON.parse(dataStr);
    }
}