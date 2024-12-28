import pyttsx3
import speech_recognition as sr
import openai
import wikipedia
import webbrowser
import os

# Initialize OpenAI API Key
openai.api_key = "your_openai_api_key"  # Replace with your OpenAI API key

# Text-to-Speech Function with Adjustments
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    # Set voice to female (try Indian accent if available)
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():  # "Zira" is Microsoft's female voice
            engine.setProperty("voice", voice.id)
            break

    # Adjust the speech rate
    engine.setProperty("rate", 140)  # Default is 200. Reduce for slower speech.
    engine.say(text)
    engine.runAndWait()

# Speech Recognition Function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm listening...")
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            speak("There seems to be a problem with the service.")
        return None

# AI Chat Function using ChatCompletion
def chat_with_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "I'm having trouble connecting to the AI."

# Wikipedia Search Function
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("Here is what I found:")
        speak(result)
    except wikipedia.DisambiguationError as e:
        speak("The term is ambiguous, try to be more specific.")
    except Exception:
        speak("I couldn't find information on that topic.")

# Open Website Function
def open_website(command):
    if "google" in command:
        webbrowser.open("https://www.google.com")
    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
    else:
        speak("I don't know that website yet.")

# System Control Function
def control_system(command):
    if "notepad" in command:
        os.system("notepad")
    elif "calculator" in command:
        os.system("calc")
    else:
        speak("I can't perform that action.")

# Main Function to Handle Commands
def main():
    speak("Hello! I am MJ, your AI assistant.")
    while True:
        command = listen()
        if command:
            if "wikipedia" in command:
                speak("What should I search on Wikipedia?")
                query = listen()
                if query:
                    search_wikipedia(query)
            elif "open" in command:
                open_website(command)
            elif "run" in command:
                control_system(command)
            elif "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
            else:
                response = chat_with_ai(command)
                speak(response)

# Run the Assistant
if __name__ == "__main__":
    main()
