class QuizAnswerBlock {
    constructor(localState) {
        this.localState = localState;
        this.checkboxContainer = document.getElementById('round-question-questions-container');
        this.radioGroupSelector = 'input[name="answer"]';
    }

    readAnswerFromInputs(quizState) {
        let answer = getRadioGroupValue(this.radioGroupSelector);
        if (answer === undefined)
            answer = getSelectedCheckboxes(this.checkboxContainer);
        else
            answer = [answer];
        if (!answer)
            return null;
        // store answer in cache
        const questionIndex = quizState.state.cur_question_index[0];
        this.localState.lastAnswer = {
            "questionIndex": questionIndex,
            "quizCode": quizState.state.quiz_code,
            "answer": answer
        }
        return answer;
    }

    restoreLastAnswer(quizState) {
        const lastAnswer = this.localState.lastAnswer;
        if (!lastAnswer) return;
        if (quizState.state.cur_question_index[0] != lastAnswer.questionIndex)
            return;
        if (quizState.state.quiz_code != lastAnswer.quizCode)
            return;

        const questionType = quizState.state.cur_question.question_type;
        if (questionType == 'MULTI_CHOICE')
            this.restoreMultiChoice(quizState.state.cur_question, lastAnswer);
        else
            this.restoreSingleChoice(quizState.state.cur_question, lastAnswer);
    }

    restoreMultiChoice(question, answer) {
        const checkboxes = this.checkboxContainer.querySelectorAll("input[type='checkbox']");
        const selectedIndexes = [];
        for (let i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = answer.answer.includes(i);
        }
    }

    restoreSingleChoice(question, answer) {
        const radios = document.querySelectorAll(this.radioGroupSelector);
        if (radios.length > answer.answer[0])
            radios[answer.answer[0]].checked = true;
    }
}