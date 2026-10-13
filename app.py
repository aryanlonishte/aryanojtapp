from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recognize", methods=["POST"])
def recognize():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"})

    audio_file = request.files["audio"]

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return jsonify({"text": text})

    except sr.UnknownValueError:
        return jsonify({"error": "Sorry, speech could not be understood."})

    except sr.RequestError:
        return jsonify({"error": "Speech recognition service is unavailable."})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)