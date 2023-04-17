class Server {
    constructor() {
        this.baseUrl = "https://wi4tgcnh0j.execute-api.eu-central-1.amazonaws.com/prod/quiz/";
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

    queryServer(operation, payload, onCompleted) {
        const requestPayload = {
          "requested_operation": operation,
          "payload": payload
        };
        fetch(this.baseUrl, {
                method: 'POST',
                body: JSON.stringify(requestPayload),
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

    getQuizTopics(onCompleted) {
        this.queryServer("quiz-topics", {}, onCompleted);
    }

    startQuiz(quizId, userName, intervalSeconds, onCompleted) {
        this.queryServer("quiz-start", {
            "topic_id": quizId, "user_name": userName, "question_seconds": intervalSeconds},
            onCompleted);
    }

    scheduleQuiz(quizCode, userToken, delaySeconds, onCompleted) {
        this.queryServer("quiz-schedule", {
            "quiz_code": quizCode, "user_token": userToken, "delay_seconds": delaySeconds},
            onCompleted);
    }

    joinQuiz(quizCode, userName, onCompleted) {
        this.queryServer("quiz-join", {"quiz_code": parseInt(quizCode), "user_name": userName},
            onCompleted);
    }

    postAnswer(quizCode, userToken, questionIndex, answer, onCompleted) {
        this.queryServer("quiz-answer", {"quiz_code": quizCode, "user_token": userToken,
                     "question_index": questionIndex, "answer": answer},
            onCompleted);
    }

    getQuizResults(quizCode, onCompleted) {
        this.queryServer("quiz-results", {"quiz_code": quizCode}, onCompleted);
    }

    checkQuizStatus(quizCode, userToken, onCompleted) {
        this.queryServer("quiz-check-status", {"quiz_code": quizCode, "user_token": userToken}, onCompleted);
    }
}
