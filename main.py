import streamlit as st
import gradio as gr
from paddleocr import PaddleOCR
from langchain.llms import CTransformers
import streamlit as st
import sounddevice as sd
import soundfile as sf
import tempfile
import numpy as np
import io
import speech_recognition as sr


from requests import post

# Function to send data to CRM API
def send_to_crm(data):
    # Replace these values with actual CRM API endpoint and credentials
    api_endpoint = "https://example.com/api/contacts"
    api_key = "your_api_key"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = post(api_endpoint, json=data, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()  # Return JSON response from CRM API
    except Exception as e:
        st.error(f"Error sending data to CRM: {e}")

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

# Define OCR function using PaddleOCR
def ocr_with_paddle(img):
    finaltext = ''
    ocr = PaddleOCR(lang='en', use_angle_cls=True)
    result = ocr.ocr(img)
    for i in range(len(result[0])):
        text = result[0][i][1][0]
        finaltext += ' '+ text
    return finaltext

# Define function for processing text using LLM
def process_text_with_llm(text):
    llm = CTransformers(
        model="llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        max_new_tokens=1096,
        temperature=0.2,
        repetition_penalty=1.13
    )
    return llm(f"""read the text....{text}...carefully and give names,email,phone number,address and other important information in json format present the text.There are some inconsistency in the text you have to only return name,emai,address,phone number....use your inteligence and correctly identify it \
          """)

def transcribe_text_with_llm(trans_text,voice):
    llm2 = CTransformers(
        model="llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        max_new_tokens=1096,
        temperature=0.2,
        repetition_penalty=1.13
    )
    return llm2(f"""this is the final result {trans_text} and this is the required changes {voice}...do these changes on final result with required changes and return the final output""")

# Streamlit UI
# def main():
#     st.title("Image Text Extraction and Processing")

#     # File uploader for image
#     uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

#     if uploaded_file is not None:
#         # Display uploaded image
#         st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

#         # Convert uploaded file to bytes
#         file_bytes = uploaded_file.read()

#         # Perform OCR on the uploaded image
#         ocr_result = ocr_with_paddle(file_bytes)

#         # Display OCR result
#         st.subheader("OCR Result:")
#         st.text(ocr_result)

#         # Process OCR result using LLM
#         st.subheader("Processed Text:")
#         processed_result = process_text_with_llm(ocr_result)
#         st.write(processed_result)

#         st.title("Real-time Speech to Text")

#         duration = st.slider("Recording Duration (seconds)", 1, 10, 5)

#         if st.button("Start Recording"):
#             audio_data = record_sound(duration=duration, samplerate=44100)
#             st.write("Recording complete.")

#             # Save audio data to a temporary WAV file
#             with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
#                 sf.write(temp_audio_file.name, audio_data, 44100, 'PCM_24')

#             st.subheader("Transcribed Text:")
#             transcribed_text = speech_to_text(temp_audio_file.name)
#             st.write(transcribed_text)
#         st.subheader("final output")

#         final_output=transcribe_text_with_llm(processed_result,transcribed_text)
#         st.write(final_output)

#         st.subheader("Send to CRM:")
#         if st.button("Send to CRM"):
#             response = send_to_crm(processed_result)
#             st.write("Response from CRM API:")
#             st.json(response)

# if __name__ == "__main__":
#     main()

def main():
    st.title("Image Text Extraction and Processing")

    # File uploader for image
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Display uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Convert uploaded file to bytes
        file_bytes = uploaded_file.read()

        # Perform OCR on the uploaded image
        ocr_result = ocr_with_paddle(file_bytes)

        # Display OCR result
        st.subheader("OCR Result:")
        st.text(ocr_result)

        # Process OCR result using LLM
        st.subheader("Processed Text:")
        processed_result = process_text_with_llm(ocr_result)
        st.write(processed_result)

        st.title("Real-time Speech to Text")

        duration = st.slider("Recording Duration (seconds)", 1, 10, 5)

        transcribed_text = ""  # Initialize transcribed_text variable

        if st.button("Start Recording"):
            audio_data = record_sound(duration=duration, samplerate=44100)
            st.write("Recording complete.")

            # Save audio data to a temporary WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                sf.write(temp_audio_file.name, audio_data, 44100, 'PCM_24')

            st.subheader("Transcribed Text:")
            transcribed_text = speech_to_text(temp_audio_file.name)
            st.write(transcribed_text)

            st.subheader("final output")

            final_output=transcribe_text_with_llm(processed_result, transcribed_text)
            st.write(final_output)

        st.subheader("Send to CRM:")
        if st.button("Send to CRM"):
            response = send_to_crm(processed_result)
            st.write("Response from CRM API:")
            st.json(response)

if __name__ == "__main__":
    main()
