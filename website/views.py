from flask import Blueprint, render_template, request, render_template_string
import requests
import markdown
import os

views = Blueprint("views", __name__)


# MAIN PAGE
@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        model = request.form.get("model")
        bot_response = generate_bot_response(user_input, model)
        markdown_response = markdown.markdown(bot_response, extensions=["fenced_code"])
        return render_template(
            "index.html", user_input=user_input, converted_markdown=markdown_response, model = model
        )
    return render_template("index.html")


def generate_bot_response(user_input, model):
    api_key = os.environ["OPENAI_API_KEY"]
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "model": model,  # "gpt-4-1106-preview",
        "messages": [
            {
                "role": "user",
                "content": user_input,
            },
        ],
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        message = response_json["choices"][0]["message"]["content"]
    else:
        message = f"Błąd połączenia z API OpenAI: {response.status_code}\nTreść odpowiedzi:{response.text}"

    return message
