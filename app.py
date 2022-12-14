from flask import Flask, request
import json
import bleach

app = Flask(__name__)

users = {}

def load_api_data(
    users_file="users.tsv",
    experience_file="experience.tsv",
    separator="\t", # Allows us to handle files with any separator
    primary_key="id" # Allows us to specify which column is the primary key
):
    parse_user_file(users_file, separator, primary_key)
    parse_experience_file(experience_file, separator, primary_key)

@app.route("/candidates", methods=["GET"])
def get_candidates():
    results = []

    for user in users:
        results.append({
            "bio": users[user]["bio"],
            "id": user,
            "name": users[user]["name"],
            "picture": users[user]["picture"]
        })

    output = json.dumps({
        "results": results
    })

    return output

@app.route("/candidate/<string:candidate_id>", methods=["GET"])
def get_candidate(candidate_id):
    if candidate_id not in users:
        raise ValueError("Unknown candidate ID")

    output = json.dumps({
        "results": {
            "bio": users[candidate_id]["bio"],
            "experience": format_experience(users[candidate_id]["experience"]),
            "name": users[candidate_id]["name"],
            "picture": users[candidate_id]["picture"]
        }
    })

    return output

@app.route("/candidate/<string:candidate_id>", methods=["PUT"])
def update_candidate(candidate_id):
    if candidate_id not in users:
        raise ValueError("Unknown candidate ID")

    if "experience" not in request.get_json():
        raise ValueError("Request is missing experience data")

    users[candidate_id]["experience"] = format_experience(request.get_json()["experience"])

    output = json.dumps({
        "results": "ok"
    })

    return output

def parse_user_file(file_path, separator, primary_key):
    try:
        with open(file_path, "r") as users_file:
            headers = parse_row(users_file.readline(), separator)
            primary_key_index = get_primary_key_index(primary_key, headers)

            for line in users_file.readlines():
                data = parse_row(line=line, separator=separator)
                if len(data) != len(headers):
                    raise ValueError("The user file is missing a data point")

                user = data[primary_key_index].strip()
                users[user] = { key: value for (key, value) in zip(headers, data)}
                users[user]["experience"] = []
    except FileNotFoundError:
        raise FileNotFoundError("The user file is missing")

def parse_experience_file(file_path, separator, primary_key):
    try:
        with open(file_path, "r") as experience_file:
            headers = parse_row(experience_file.readline(), separator)
            primary_key_index = get_primary_key_index(primary_key, headers)

            for line in experience_file.readlines():
                data = parse_row(line=line, separator=separator)
                if len(data) != len(headers):
                    raise ValueError("The experience file is missing a data point")

                user = data[primary_key_index].strip()
                users[user]["experience"].append({ key: value for (key, value) in zip(headers, data) if key != primary_key})
    except FileNotFoundError:
        raise FileNotFoundError("The experience file is missing")

def parse_row(line, separator):
    return [chunk.replace("\n", "") for chunk in line.split(separator)] # Remove the newline character at the end of the line

def get_primary_key_index(primary_key, headers):
    if headers.count(primary_key) != 1:
        raise ValueError("Invalid primary key was specified")

    return headers.index(primary_key)

def format_experience(experiences):
    output = []

    for experience in experiences:
        output.append({
            # Sanitize all user input
            "company": bleach.clean(experience["company"]),
            "dates": bleach.clean(experience["dates"]),
            "description": bleach.clean(experience["description"]),
            "title": bleach.clean(experience["title"])
        })

    return output


api_loaded = False
if not api_loaded:
    print("Loading API data...")
    load_api_data()
    api_loaded = True
