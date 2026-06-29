
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from google import genai
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
db = SQLAlchemy(app)
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500))
    answer = db.Column(db.String(2000))
with app.app_context():
    db.create_all()

#print("KEY USED =", os.getenv("GEMINI_KEY")[:16])
#print("MODEL =", "gemini-2.0-flash")

client = genai.Client(
    api_key=os.getenv("GEMINI_KEY")
)


@app.route("/")
def home():
    chats = ChatHistory.query.all()
    return render_template("index.html", answer="", chats=chats)

@app.route("/ask")
def ask():

    question = request.args.get("q")

    try:
# """ """      """    response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=question
#         ) """ """ """
        class Fake:
            text = "TEST ANSWER"

        response = Fake()
        chat = ChatHistory(
            question=question,
            answer=response.text
        )

        db.session.add(chat)
        db.session.commit()


        return render_template(
            "index.html",
            answer=response.text
        )

    except Exception as e:

        return render_template(
            "index.html",
            answer="Error: " + str(e)
        )
with app.app_context():
    chats = ChatHistory.query.all()
    print("TOTAL RECORDS =", len(chats))

#app.run()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)