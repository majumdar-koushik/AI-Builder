from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from google import genai
from dotenv import load_dotenv
import os

load_dotenv() #Read secret variables from .env

app = Flask(__name__) #Create web application object.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"  #Database file = chat.db

db = SQLAlchemy(app)


# Database Model
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    answer = db.Column(db.String(2000))


# Create Database
with app.app_context():
    db.create_all()


# Gemini Provider
def ask_gemini(question):

    client = genai.Client(
        api_key=os.getenv("GEMINI_KEY")
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=question
    )

    return response.text


# Home Page
@app.route("/")
def home():

    chats = ChatHistory.query.all()

    return render_template(
        "index.html",
        answer="",
        chats=chats
    )


# Ask Route
@app.route("/ask")
def ask():

    question = request.args.get("q", "")

    try:
        answer = ask_gemini(question)

        chat = ChatHistory(
            question=question,
            answer=answer
        )

        db.session.add(chat)
        db.session.commit()

        return render_template(
            "index.html",
            answer=answer,
            chats=ChatHistory.query.all()
        )

    except Exception as e:

        return render_template(
            "index.html",
            answer="Error: " + str(e),
            chats=ChatHistory.query.all()
        )


# Run App
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)