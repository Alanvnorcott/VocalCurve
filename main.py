import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech recorded from `microphone`."""
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.RequestError:
        print("ERROR: API unavailable")
    except sr.UnknownValueError:
        print("Unable to recognize speech")

    return None


def count_word(target_word):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    count = 0

    print(f"I'm now listening for the word '{target_word}'. Speak clearly into the microphone.")
    print("Say 'stop' to end the session.")

    while True:
        print("\nListening...")
        transcription = recognize_speech_from_mic(recognizer, microphone)

        if transcription:
            print(f"You said: {transcription}")

            if transcription.lower() == 'stop':
                break

            words = transcription.lower().split()
            word_count = words.count(target_word.lower())
            count += word_count

            if word_count > 0:
                print(f"'{target_word}' was said {word_count} time(s) in this phrase.")

            print(f"Total count of '{target_word}': {count}")

    print(f"\nSession ended. '{target_word}' was said a total of {count} time(s).")


if __name__ == "__main__":
    target_word = input("Enter the word you want to keep track of: ")
    count_word(target_word)