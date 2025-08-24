import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyjokes

# TTS setup
engine = pyttsx3.init()
voices = engine.getProperty("voices")
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break
engine.setProperty("rate", 200)

def speak(text):
    print("Sam:", text)
    engine.say(text)
    engine.runAndWait()

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
        return query.lower()
    except:
        return "none"

# Track current context
current_context = {"website": None}

# Open desktop apps
def open_app(app_name):
    app_name = app_name.lower()
    try:
        if "notepad" in app_name:
            os.system("notepad")
        elif "calculator" in app_name:
            os.system("calc")
        elif "paint" in app_name:
            os.system("mspaint")
        elif "word" in app_name:
            os.system("start winword")
        elif "excel" in app_name:
            os.system("start excel")
        elif "vscode" in app_name or "code" in app_name:
            os.system("code")
        else:
            return False
        speak(f"Opening {app_name}")
        return True
    except:
        return False

# Open websites
def open_website(site_name):
    site_name = site_name.lower()
    if "youtube" in site_name:
        webbrowser.open("https://youtube.com")
        current_context["website"] = "youtube"
    elif "google" in site_name:
        webbrowser.open("https://google.com")
        current_context["website"] = "google"
    elif "amazon" in site_name:
        webbrowser.open("https://www.amazon.com")
        current_context["website"] = "amazon"
    elif "zomato" in site_name:
        webbrowser.open("https://www.zomato.com")
        current_context["website"] = "zomato"
    elif "swiggy" in site_name:
        webbrowser.open("https://www.swiggy.com")
        current_context["website"] = "swiggy"
    elif "instagram" in site_name:
        webbrowser.open("https://www.instagram.com")
        current_context["website"] = "instagram"
    else:
        webbrowser.open(f"https://www.google.com/search?q={site_name}")
        current_context["website"] = "google"
    speak(f"Opening {site_name}")

# Handle searches inside websites
def handle_search(query):
    site = current_context["website"]
    if site == "amazon":
        webbrowser.open(f"https://www.amazon.com/s?k={query}")
        speak(f"Searching {query} on Amazon")
    elif site == "google":
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching {query} on Google")
    elif site == "youtube":
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        speak(f"Searching {query} on YouTube")
    elif site == "zomato":
        webbrowser.open(f"https://www.zomato.com/search?query={query}")
        speak(f"Finding {query} on Zomato")
    elif site == "swiggy":
        webbrowser.open(f"https://www.swiggy.com/search?query={query}")
        speak(f"Ordering {query} on Swiggy")
    else:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching {query} online")

# Main logic
if __name__ == "__main__":
    speak("Hello, I am Sam, your personal assistant. How can I help you?")

    while True:
        cmd = listen_command()
        if cmd == "none":
            continue

        # Exit
        if "exit" in cmd or "quit" in cmd:
            speak("Goodbye! Have a nice day.")
            break

        # Time & Date
        elif "time" in cmd:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif "date" in cmd:
            today = datetime.date.today().strftime("%B %d, %Y")
            speak(f"Today's date is {today}")

        # Joke
        elif "joke" in cmd:
            joke = pyjokes.get_joke()
            speak(joke)

        # Order food
        elif "order" in cmd and "zomato" in cmd:
            food_item = cmd.replace("order", "").replace("from zomato", "").strip()
            if food_item:
                webbrowser.open(f"https://www.zomato.com/search?query={food_item}")
                speak(f"Ordering {food_item} from Zomato")
            else:
                open_website("zomato")

        elif "order" in cmd and "swiggy" in cmd:
            food_item = cmd.replace("order", "").replace("from swiggy", "").strip()
            if food_item:
                webbrowser.open(f"https://www.swiggy.com/search?query={food_item}")
                speak(f"Ordering {food_item} from Swiggy")
            else:
                open_website("swiggy")

        # Handle "open" commands
        elif "open" in cmd:
            parts = cmd.split(" then ")
            for part in parts:
                part = part.replace("open", "").strip()
                if not open_app(part):
                    open_website(part)

        # Handle generic search
        elif "search" in cmd or "find" in cmd:
            query = cmd.replace("search", "").replace("find", "").strip()
            handle_search(query)

        else:
            # If in context (like already in Zomato)
            if current_context["website"]:
                handle_search(cmd)
            else:
                speak("Sorry, I did not get that. Please try again.")
