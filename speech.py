# import streamlit as st
# import sounddevice as sd
# import numpy as np
# import io
# import wavio
# import speech_recognition as sr

# def record_sound(duration=5, samplerate=44100):
#     print("Recording...")
#     recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16')
#     sd.wait()
#     print("Recording complete.")
#     return recording

# def speech_to_text(audio_data):
#     recognizer = sr.Recognizer()
#     audio_data = np.array(audio_data)
#     with io.BytesIO() as wav_file:
#         wavio.write(wav_file, audio_data, rate=44100, sampwidth=2)
#         wav_file.seek(0)
#         with sr.AudioFile(wav_file) as source:
#             audio = recognizer.record(source)
#             try:
#                 text = recognizer.recognize_google(audio)
#                 return text
#             except sr.UnknownValueError:
#                 return "Unable to transcribe the audio"
#             except sr.RequestError as e:
#                 return f"Error: {e}"

# def main():
#     st.title("Real-time Speech to Text")

#     duration = st.slider("Recording Duration (seconds)", 1, 10, 5)

#     if st.button("Start Recording"):
#         audio_data = record_sound(duration=duration)
#         st.write("Recording complete.")
#         st.audio(audio_data, format='audio/ogg')
        
#         st.subheader("Transcribed Text:")
#         text = speech_to_text(audio_data)
#         st.write(text)

# if __name__ == "__main__":
#     main()

# import streamlit as st
# import sounddevice as sd
# import soundfile as sf
# import numpy as np
# import io
# import speech_recognition as sr

# def record_sound(duration=5, samplerate=44100):
#     print("Recording...")
#     recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
#     sd.wait()
#     print("Recording complete.")
#     return recording

# def speech_to_text(audio_data, samplerate):
#     recognizer = sr.Recognizer()
#     with io.BytesIO() as wav_file:
#         sf.write(wav_file, audio_data, samplerate, 'PCM_24')
#         wav_file.seek(0)
#         with sr.AudioFile(wav_file) as source:
#             audio = recognizer.record(source)
#             try:
#                 text = recognizer.recognize_google(audio)
#                 return text
#             except sr.UnknownValueError:
#                 return "Unable to transcribe the audio"
#             except sr.RequestError as e:
#                 return f"Error: {e}"

# def main():
#     st.title("Real-time Speech to Text")

#     duration = st.slider("Recording Duration (seconds)", 1, 10, 5)

#     if st.button("Start Recording"):
#         audio_data = record_sound(duration=duration, samplerate=44100)
#         st.write("Recording complete.")

#         st.subheader("Transcribed Text:")
#         text = speech_to_text(audio_data, samplerate=44100)
#         st.write(text)

# if __name__ == "__main__":
#     main()



import streamlit as st
import sounddevice as sd
import soundfile as sf
import tempfile
import numpy as np
import io
import speech_recognition as sr

def record_sound(duration=5, samplerate=44100):
    print("Recording...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete.")
    return recording

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Unable to transcribe the audio"
        except sr.RequestError as e:
            return f"Error: {e}"

def main():
    st.title("Real-time Speech to Text")

    duration = st.slider("Recording Duration (seconds)", 1, 10, 5)

    if st.button("Start Recording"):
        audio_data = record_sound(duration=duration, samplerate=44100)
        st.write("Recording complete.")

        # Save audio data to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            sf.write(temp_audio_file.name, audio_data, 44100, 'PCM_24')

        st.subheader("Transcribed Text:")
        text = speech_to_text(temp_audio_file.name)
        st.write(text)

if __name__ == "__main__":
    main()
