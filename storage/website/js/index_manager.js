class IndexPageManager {
    constructor() {
        this.server = new Server();
        this.localState = new LocalStateManager();
    }

    initialize() {
        this.setupTabs();
        document.getElementById('btn-start').addEventListener('click', (e) => {
            this.startQuiz();
        });
        document.getElementById('btn-join').addEventListener('click', (e) => {
            this.joinQuiz();
        });
        document.getElementById('user-name').value = this.localState.userName;
        // request topics to list on the "New quiz" page
        this.server.getQuizTopics((topics) => {
            this.renderTopics(topics);
        });
    }

    renderTopics(topics) {
        const parentDiv = document.getElementById('quiz-topics');
        createRadioGroup(topics, (t) => t.name, (t) => t.id, parentDiv, 'topics-radio-group', 'topic');
    }

    setupTabs() {
        const tabs = document.querySelectorAll('.tabs button');
        const tabNames = ['tab-join', 'tab-start']
        tabs.forEach((btn, i) => {
            btn.addEventListener('click', (e) => {
                this.openTab(e.currentTarget, tabNames[i]);
            })
        });
        this.openTab(tabs[tabs.length - 1], tabNames[tabs.length - 1]);
    }

    openTab(srcElement, tabName) {
        // Declare all variables
        let i, tabPanel, tabButton;

        // Get all elements with class="tab-panel" and hide them
        tabPanel = document.getElementsByClassName("tab-panel");
        for (i = 0; i < tabPanel.length; i++) {
            tabPanel[i].classList.remove("active");
        }

        // Get all elements with class="tab-button" and remove the class "active"
        tabButton = document.getElementsByClassName("tab-button");
        for (i = 0; i < tabButton.length; i++) {
            tabButton[i].classList.remove("active");
        }

        // Show the current tab, and add an "active" class to the button that opened the tab
        document.getElementById(tabName).classList.add("active");
        srcElement.classList.add("active");
    }

    startQuiz() {
        const selectedValue = getRadioGroupValue('input[name="topic"]');
        if (!selectedValue) return;
        const userName = document.getElementById('user-name').value;
        if (!userName) {
            alert('Select your user name before starting the quiz');
            return;
        }
        const intervalSeconds = document.getElementById('quiz-interval-seconds').value;
        this.localState.userName = userName;
        this.localState.storeQuizState(null);
        this.server.startQuiz(selectedValue, userName, parseInt(intervalSeconds),
            (quizState) => {
                this.localState.storeQuizState(quizState);
                // navigate to the quiz page
                window.location = 'quiz_round.html';
            });
    }

    joinQuiz() {
        const userName = document.getElementById('user-name').value;
        if (!userName) {
            alert('Select your user name before joining the quiz');
            return;
        }
        const quizCode = document.getElementById('quiz-code').value;
        if (!quizCode) {
            alert('Provide the quiz code in the correspondent input');
            return;
        }

        this.localState.userName = userName;
        this.localState.storeQuizState(null);
        this.server.joinQuiz(quizCode, userName, (quizState) => {
            this.localState.storeQuizState(quizState);
            // navigate to the quiz page
            window.location = 'quiz_round.html';
        });
    }
}