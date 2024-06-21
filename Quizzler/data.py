import requests as reqs

db_url = "https://opentdb.com/api.php"

paramter = {
    "amount": 10,
    "type": "boolean",
    "category": 18,
    "difficulty": "easy"
}

response = reqs.get(url=db_url, params=paramter)
response.raise_for_status()

question_data = response.json()["results"]
