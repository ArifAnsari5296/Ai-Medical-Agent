# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

# VoiceBot UI with Gradio
import os
import gradio as gr

from brain_of_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# Load API keys globally to avoid fetching them in every function call
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Ensure API keys exist
if not GROQ_API_KEY:
    raise ValueError("❌ ERROR: GROQ_API_KEY is missing! Please set it in the .env file.")

if not ELEVENLABS_API_KEY:
    raise ValueError("❌ ERROR: ELEVENLABS_API_KEY is missing! Please set it in the .env file.")

# AI System Prompt for Doctor Analysis
system_prompt = """
You have to act as a professional doctor. Analyze the image and determine if anything is medically wrong. 
If needed, suggest remedies concisely in 1-2 sentences. Do not mention that you are an AI, and answer as if talking to a real patient.
Avoid preambles like 'In the image, I see'. Instead, respond directly.
"""


def process_inputs(audio_filepath, image_filepath):
    """Processes the audio and image input, then returns the doctor's response."""
    
    # ✅ Step 1: Validate the Audio File
    if not audio_filepath or not os.path.exists(audio_filepath):
        return "Error: No valid audio file provided.", "Error in transcription", None

    print(f"✅ Processing audio file: {audio_filepath}")

    # ✅ Step 2: Convert Speech to Text
    try:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=GROQ_API_KEY, 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

        print(f"🔍 Speech-to-Text Output: {speech_to_text_output}")

        # Handle empty transcription
        if not speech_to_text_output or speech_to_text_output.strip() == "":
            speech_to_text_output = "User input was not recognized."

    except Exception as e:
        return f"Speech-to-text error: {e}", "Error in transcription", None

    # ✅ Step 3: Process Image (if provided)
    if image_filepath:
        try:
            encoded_image = encode_image(image_filepath)
            query_text = system_prompt + " " + str(speech_to_text_output)
            
            doctor_response = analyze_image_with_query(
                query=query_text,
                encoded_image=encoded_image,
                model="meta-llama/llama-4-maverick-17b-128e-instruct"
            )
        except Exception as e:
            doctor_response = f"Image analysis error: {e}"
    else:
        doctor_response = "No image provided for analysis."

    # ✅ Step 4: Convert Doctor's Response to Speech
    try:
        output_audio_file = "doctor_response.mp3"
        text_to_speech_with_elevenlabs(
            input_text=doctor_response,
            output_filepath=output_audio_file
        )
    except Exception as e:
        return speech_to_text_output, doctor_response, f"Text-to-speech error: {e}"

    return speech_to_text_output, doctor_response, output_audio_file

# Create the Gradio Interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Record Your Voice"),
        gr.Image(type="filepath", label="Upload Medical Image (Optional)")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text Output"),
        gr.Textbox(label="Doctor_Ai's Response"),
        gr.Audio(label="Doctor_Ai's Voice Response")
    ],
    title="AI Doctor",
    description="Speak your symptoms and optionally upload an image. The AI will analyze and respond."
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch(debug=True)

#Access at: http://127.0.0.1:7860
