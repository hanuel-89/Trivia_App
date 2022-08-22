# API Reference
## Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, while the React frontend is hosted at http://127.0.0.1:3000/
- Authentication: This version of the application does not require authentication or API keys.
## Error Handling
Errors are returned as JSON objects in the following format:
```bash
pip install -r requirements.txt
```
The API will return three error types when requests fail:
- 400: Bad request
- 404: Resource not found
- 422: Not processable

## Endpoints

### GET /questions
- General
 - Returns a list of question objects, success value, categories, current_category and total number of questions
 - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: ```curl http://127.0.0.1:5000/questions```
```bash
{
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"current_category": "History",
"questions": [
{
"answer": "Apollo 13",
"category": 5,
"difficulty": 4,
"id": 2,
"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
{
"answer": "Lake Victoria",
"category": 3,
"difficulty": 2,
"id": 13,
"question": "What is the largest lake in Africa?"
},
{
"answer": "The Palace of Versailles",
"category": 3,
"difficulty": 3,
"id": 14,
"question": "In which royal palace would you find the Hall of Mirrors?"
}
],
"success": true,
"total_questions": 22
}
```

### POST /questions
- General
 - **New Question**
 - Creates a new questions using the submitted question, answer, difficulty and category. Returns the id of the created questions, success value, total questions, and questions list based on current page number to update the frontend
 - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: ```curl http://127.0.0.1:3000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Who is the president of Nigeria?", "answer": "Buhari", "difficulty": 1, "category": 4}'```

```bash
{
    "posted": {
        "answer": "Buhari",
        "category": 4,
        "difficulty": 1,
        "id": 39,
        "question": "Who is the president of Nigeria?"
    },
    "posted_question_Id": 39,
    "success": true,
    "total_questions": 34
}
```
 - **Search**
 - Searches the database for questions that matches the search term
 - Returns the found questions, success value, and length of total questions found
- Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Tom"}'```

```bash
{
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

### DELETE /questions/{id}
- General
 - Deletes the questions of the given ID if it exists. Returns the id of the deleted questions, success value, and number of total questions.
- Sample: ```curl -X DELETE http://127.0.0.1:5000/questions/38```

```bash
{
    "deleted": 38,
    "success": true,
    "total_questions": 33
}
```
### GET /categories
- General
 - Returns a list of category objects, success value, and total number of categories
- Sample: ```curl http://127.0.0.1:5000/categories```
```bash
{
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"success": true,
"total_categories": 6
}
```
### GET /categories/{id}/questions
- General
 - Returns a list of questions in the selected category, the selected category, success values and the total questions in the category
- Sample: ```curl http://127.0.0.1:5000/categories/5/questions```
```bash
{
"current_category": 5,
"questions": [
{
"answer": "Apollo 13",
"category": 5,
"difficulty": 4,
"id": 2,
"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
{
"answer": "Tom Cruise",
"category": 5,
"difficulty": 4,
"id": 4,
"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
},
{
"answer": "Edward Scissorhands",
"category": 5,
"difficulty": 3,
"id": 6,
"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
}
],
"success": true,
"total_questions": 3
}
```
### POST /quizzes
- General
 - Shows the next question in the quiz based on the selected quiz category and the list of previous questions ID.
 - Returns the next question, success values, and total questions
- Sample: ```curl --location --request POST 'http://localhost:3000quizzes' --header 'Content-Type: application/json' --data-raw '{"previous_questions": [1, 4, 20, 15], "quiz_category": {"id": 3, "type": "Geography"}}'```
```bash
{
    "question": {
        "answer": "Ivan Hernandez",
        "category": 3,
        "difficulty": 3,
        "id": 26,
        "question": "Who is the president of Turkey?"
    },
    "success": true,
    "totalQuesitons": 24
}
```



