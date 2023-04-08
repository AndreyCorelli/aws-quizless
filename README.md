For getting help with Terraform check [this page](readme-terraform.md). 

# 1 Groundwork

Setup virtual environment for the specific Python version (3.10):
```shell
pyenv local 3.10
virtualenv venv -p python3.10
source venv/bin/activate
```

Install the dependencies:
```shell
pip install fastapi
pip install redis
pip install uvicorn
pip freeze > requirements.txt
```

Test the API:
```shell
curl -iX 'GET' 'http://localhost:8055/api/quiz-topics'
```

Setup Git repository in the current project folder:
```shell
git init .
git remote add origin git@github.com:<username>/quizless.git
```

# 2 Quiz Backend
Test starting the quiz:
```shell
curl -iX 'POST' 'http://localhost:8055/api/quiz-start' \
  -H "Content-Type: application/json" \
  -d '{"topic_id": "d729af45-5ed3-42d0-ac57-d4485b64b067", "user_name": "Alph"}'
```
Test joining the quiz (quiz_code is taken from the previous command output):
```shell
curl -iX 'POST' 'http://localhost:8055/api/quiz-join' \
  -H "Content-Type: application/json" \
  -d '{"quiz_code": 68571, "user_name": "Bart"}'
```
Test getting the quiz status:
- both quiz_code and user_token are taken either from /quiz-start or /quiz-join response.
```shell
curl -iX 'POST' 'http://localhost:8055/api/quiz-check-status' \
  -H "Content-Type: application/json" \
  -d '{"quiz_code": 68571, "user_token": "07d76bbd-51f6-4b7f-9d7a-59a6287c0a36"}'
```