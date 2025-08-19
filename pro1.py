from gtts import gTTS
import os
from langdetect import detect

# Ask user for input
text = input("👉 Enter the text you want to convert to speech: ")

# Detect language automatically
lang = detect(text)
print(f"🌍 Detected language: {lang}")

# Convert to speech
speech = gTTS(text=text, lang=lang, slow=False)

# Save file
speech.save("output.mp3")
print("✅ Audio file saved as output.mp3")

# Play file
os.system("start output.mp3")
print("▶️ Playing audio...")
