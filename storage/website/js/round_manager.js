class RoundPageManager {
    constructor() {
        this.server = new Server();
        this.localState = new LocalStateManager();
        this.quizState = null;
        this.quizTimer = new QuizTimer();
        this.answerBlock = new QuizAnswerBlock(this.localState);
    }

    initialize() {
        document.getElementById('user-name').value = this.localState.userName;
        this.quizState = this.localState.readQuizState();
        this.renderQuizState();
        document.getElementById('btn-start-quiz').addEventListener('click', (e) => {
            this.scheduleQuiz();
        });
        document.getElementById('btn-post-answer').addEventListener('click', (e) => {
            this.postAnswer();
        });
        // request current quiz status
        this.server.checkQuizStatus(
            this.quizState.state.quiz_code, this.quizState.user.user_token,
            (data) => {this.updateAndRenderQuizData(data);});
    }

    scheduleQuiz() {
        this.server.scheduleQuiz(
            this.quizState.state.quiz_code,
            this.quizState.user.user_token,
            5,
            (data) => {this.updateAndRenderQuizData(data);}
        )
    }

    updateAndRenderQuizData(data) {
        if (!data || !data.state) {
            console.error('Received incorrect data (state) from the server');
            console.log(data);
            return;
        }
        this.localState.storeQuizState(data);
        this.quizState = data;
        this.renderQuizState();
    }

    postAnswer() {
        let answer = this.answerBlock.readAnswerFromInputs(this.quizState);
        if (!answer)
            return;
        answer = answer.map(x => parseInt(x));
        this.server.postAnswer(this.quizState.state.quiz_code,
            this.quizState.user.user_token, this.quizState.state.cur_question_index[0],
            answer, (data) => {
                this.updateAndRenderQuizData(data);
            });
    }

    renderQuizState() {
        // set the timer
        this.quizTimer.setTimer(this.quizState.state.updates_in_seconds);
        if (this.quizState.state.updates_in_seconds >= 0) {
            // schedule quiz status update
            setTimeout(() => {
                this.server.checkQuizStatus(
                    this.quizState.state.quiz_code, this.quizState.user.user_token,
                    (data) => {this.updateAndRenderQuizData(data);}
                );
            }, this.quizState.state.updates_in_seconds * 1000 + 10);
        }

        // update the user name
        this.localState.userName = this.quizState.user.name;
        let quizStatusText = `Quiz "${this.quizState.state.name}" (#` +
            `${this.quizState.state.quiz_code}) `;
        document.getElementById("start-quiz-panel").style.display = 'none';
        if (this.quizState.state.status == 'PENDING') {
            quizStatusText += 'is not started yet';
            if (this.quizState.user.user_role == 'COMMANDER') {
                quizStatusText += '. Share the link to the quiz with your friends ' +
                    'and then start the quiz.';
                // show the button to start the quiz
                document.getElementById("start-quiz-panel").style.display = 'block';
            }
        }
        else if (this.quizState.state.status == 'SCHEDULED')
            quizStatusText += `will start soon`;
        else if (this.quizState.state.status == 'STARTED')
            quizStatusText += 'is started';
        else if (this.quizState.state.status == 'FINISHED')
            quizStatusText += 'is finished';
        else if (this.quizState.state.status == 'EXPIRED')
            quizStatusText += 'is expired';
        document.getElementById("quiz-status-text").innerText = quizStatusText;

        this.renderPlayers();
        this.renderQuizQuestion();
        this.restoreLastAnswer();
        this.obtainAndRenderQuizResults();
    }

    restoreLastAnswer() {
        if (this.quizState.state.status != 'STARTED')
            return;
        this.answerBlock.restoreLastAnswer(this.quizState);
    }

    obtainAndRenderQuizResults() {
        if (this.quizState.state.status != 'FINISHED')
            return;
        this.server.getQuizResults(this.quizState.state.quiz_code, (data) => {
            this.renderQuizResults(data);
        });
    }

    renderQuizResults(data) {
        const container = document.getElementById('quiz-results');
        container.style.display = 'block';
        document.getElementById('quiz-results-title').innerText = `Quiz #${this.quizState.state.quiz_code} ("` +
            `${data.quiz_results.quiz_name}) is finished`;
        this.renderPlayersResults(data);
        this.renderPlayerAnswers(data);
    }

    renderPlayersResults(data) {
        const quizResults = data.quiz_results;
        const container = document.getElementById('quiz-results-players');
        deleteAllChildren(container);
        quizResults.players.forEach((player, index) => {
            const playerContainer = document.createElement('div');
            const text = `[${index + 1}] ${player.name} [${player.correct_answers} ` +
                `/ ${data.quiz_data.questions.length}]`;
            let markup = encodeHTML(text);
            if (player.name == this.quizState.user.name)
                markup = `<b>${markup}</b>`;
            playerContainer.innerHTML = markup;
            container.appendChild(playerContainer);
        });
    }

    renderPlayerAnswers(data) {
        const container = document.getElementById('quiz-results-answers');
        deleteAllChildren(container);

        const player = data.quiz_results.players.find((p) => p.name == this.quizState.user.name);
        const answers = player.answers;
        answers.forEach((playerAnswer, index) => {
            const childContainer = document.createElement('div');
            const questionContainer = document.createElement('div');
            childContainer.appendChild(questionContainer);

            const question = data.quiz_data.questions[index];
            const text = `[${index + 1}] ${question.text}`;
            questionContainer.innerHTML = encodeHTML(text);

            const answersContainer = document.createElement('div');
            childContainer.appendChild(answersContainer);

            let answerMarkup = '';
            question.answers.forEach((answerText, answerIndex) => {
                answerText = encodeHTML(answerText);
                const isCorrectAnsw = question.correct_answers.includes(answerIndex);
                const isPlayerChoice = playerAnswer.answer.includes(answerIndex);
                if (isCorrectAnsw)
                    answerText = `[correct] ${answerText}`;
                else
                    answerText = `[wrong] ${answerText}`;
                if (isPlayerChoice)
                    answerText += ' [chosen]';
                answerMarkup += answerText + '<br/>';
            });
            answersContainer.innerHTML = answerMarkup + '<hr/>';

            container.appendChild(childContainer);
        });
    }

    renderPlayers() {
        const parentDiv = document.getElementById('quiz-players');
        deleteAllChildren(parentDiv);
        // sort the user names: the current user would come first
        const ownUser = this.quizState.user.name;
        let names = this.quizState.all_user_names.filter(item => {
            return item == ownUser ? null : item;
        });
        names = [ownUser, ...names];

        names.forEach((u) => {
            const playerDiv = document.createElement('div');
            let markup = encodeHTML(u);
            if (u == ownUser)
                markup = `<b>${markup}</b>`;
            playerDiv.innerHTML = markup;
            parentDiv.appendChild(playerDiv);
        });
    }

    renderQuizQuestion() {
        const questionContainer = document.getElementById('round-question');
        if (!this.quizState.state.cur_question || this.quizState.state.status != 'STARTED') {
            questionContainer.style.display = 'none';
            return;
        }
        const numberContainer = document.getElementById('round-question-number');
        numberContainer.innerText = `Question ${this.quizState.state.cur_question_index[0] + 1} ` +
            `of ${this.quizState.state.cur_question_index[1]}`;
        // render image
        const imgContainer = document.getElementById('round-question-img-container');
        if (this.quizState.state.cur_question.image) {
            const img = document.querySelectorAll('#round-question-img-container img')[0];
            const imgUri = `img/${this.quizState.state.cur_question.image}`;
            img.src = imgUri;
            imgContainer.style.display = 'block';
        } else {
            imgContainer.style.display = 'none';
        }
        // render question text
        const txtContainer = document.getElementById('round-question-text-container');
        txtContainer.innerText = this.quizState.state.cur_question.text;
        // render answers
        const answerContainer = document.getElementById('round-question-questions-container');
        deleteAllChildren(answerContainer);
        const answers = this.quizState.state.cur_question.answers.map((e, i) => [e, i]);

        if (this.quizState.state.cur_question.question_type == 'SINGLE_CHOICE') {
            // add radiogroup
            createRadioGroup(answers, (t) => t[0], (t) => t[1], answerContainer, 'topics-radio-group', 'answer');
        } else {
            // add multiple choice
            createCheckboxes(answers, (t) => t[0], (t) => t[1], answerContainer, 'topics-radio-group');
        }

        questionContainer.style.display = 'block';
    }
}