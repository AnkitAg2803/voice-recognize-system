import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import tempfile
from pydub import AudioSegment
from pydub.playback import play
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd  # Add this line to import pandas

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Function to perform task based on user input
def perform_task(text):
    # Placeholder for task execution based on the recognized text
    print("Performing task based on recognized text:", text)

# Function to listen to user input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Processing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        process_input(text)
        play_recognized_voice(audio)
    except sr.UnknownValueError:
        print("Sorry, I could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Function to perform natural language processing
def process_input(text):
    # Dummy function for now; you can add NLP processing here in the future
    tokens = word_tokenize(text)
    # Remove stopwords (not necessary for this example)
    filtered_tokens = [word for word in tokens if word.lower() not in stopwords.words('english')]
    # Join the tokens back into a single string
    processed_text = ' '.join(filtered_tokens)
    # Perform task based on processed text
    perform_task(processed_text)
    # Visualize word frequency
    visualize_word_frequency(tokens)

# Function to visualize word frequency
def visualize_word_frequency(tokens):
    # Create a frequency distribution of words
    word_freq = {}
    for word in tokens:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Convert word frequency dictionary to DataFrame for visualization
    word_freq_df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
    
    # Plot word frequency using Seaborn
    sns.barplot(x='Frequency', y='Word', data=word_freq_df)
    plt.title('Word Frequency')
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    plt.show()

# Function to play the recognized voice as background sound
def play_recognized_voice(audio):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_audio:
        tmp_audio.write(audio.get_wav_data())
        tmp_audio_path = tmp_audio.name

    sound = AudioSegment.from_file(tmp_audio_path, format="wav")
    play(sound)

    os.unlink(tmp_audio_path)  # Clean up temporary file

# Main function to listen continuously
def main():
    while True:
        listen()

if __name__ == "__main__":
    main()
