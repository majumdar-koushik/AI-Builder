
from flask import Flask, request
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_KEY")
)

@app.route("/")
def home():

    return """
    <h2>My AI Assistant</h2>

    <form action="/ask">

        <input name="q" style="width:400px">

        <button type="submit">Ask</button>

    </form>
    """


@app.route("/ask")
def ask():

    question = request.args.get("q")

    try:
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question
    )
        return response.text

    except Exception as e:
        return "Error: " + str(e)




app.run()