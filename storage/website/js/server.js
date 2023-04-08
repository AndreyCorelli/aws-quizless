class Server {
    constructor() {
        this.baseUrl = 'http://localhost:8055/api/';
    }

    async checkStatus(response) {
        if (response.status >= 200 && response.status < 300)
            return await response.json()
        throw await response.json()
    }

    processErrorInResponse(error) {
        if (error.detail)
            alert(error.detail);
        else {
            console.log('Generic error occurred, please check the log');
            console.error(error);
        }
    }

    getQuizTopics(onCompleted) {
        const url = this.baseUrl + 'quiz-topics'
        fetch(url)
            .then(this.checkStatus)
            .then(data => {
                onCompleted(data);
            })
            .catch(error => {
                this.processErrorInResponse(error);
            });
    }

    startQuiz(quizId, userName, intervalSeconds, onCompleted) {
        const url = this.baseUrl + 'quiz-start'
        fetch(url, {
                method: 'POST',
                body: JSON.stringify(
                    {"topic_id": quizId, "user_name": userName, "question_seconds": intervalSeconds}),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then(this.checkStatus)
            .then(data => {
                onCompleted(data);
            })
            .catch(error => {
                this.processErrorInResponse(error);
            });
    }

    scheduleQuiz(quizCode, userToken, delaySeconds, onCompleted) {
        const url = this.baseUrl + 'quiz-schedule'
        fetch(url, {
                method: 'POST',
                body: JSON.stringify(
                    {"quiz_code": quizCode, "user_token": userToken, "delay_seconds": delaySeconds}
                ),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then(this.checkStatus)
            .then(data => {
                onCompleted(data);
            })
            .catch(error => {
                this.processErrorInResponse(error);
            });
    }

    joinQuiz(quizCode, userName, onCompleted) {
        const url = this.baseUrl + 'quiz-join';
        fetch(url, {
                method: 'POST',
                body: JSON.stringify({"quiz_code": parseInt(quizCode), "user_name": userName}),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then(this.checkStatus)
            .then(data => {
                onCompleted(data);
            })
            .catch(error => {
                this.processErrorInResponse(error);
            });
    }

    postAnswer(quizCode, userToken, questionIndex, answer, onCompleted) {
        const url = this.baseUrl + 'quiz-answer'
        fetch(url, {
                method: 'POST',
                body: JSON.stringify(
                    {"quiz_code": quizCode, "user_token": userToken,
                     "question_index": questionIndex, "answer": answer}
                ),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then(this.checkStatus)
            .then(data => {
                onCompleted(data);
            })
            .catch(error => {
                this.processErrorInResponse(error);
            });
    }

    getQuizResults(quizCode, onCompleted) {
        const url = this.baseUrl + `quiz-results/${quizCode}`
        fetch(url)
            .then(this.checkStatus)
            .then(data => {
                onCompleted(data);
            })
            .catch(error => {
                this.processErrorInResponse(error);
            });
    }

    checkQuizStatus(quizCode, userToken, onCompleted) {
        const url = this.baseUrl + 'quiz-check-status'
        fetch(url, {
                method: 'POST',
                body: JSON.stringify(
                    {"quiz_code": quizCode, "user_token": userToken}
                ),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then(this.checkStatus)
            .then(data => {
                onCompleted(data);
            })
            .catch(error => {
                this.processErrorInResponse(error);
            });
    }
}
