import os
from elevenlabs.client import ElevenLabs  # Correct import for ElevenLabs v1.50.7
from elevenlabs import save, play

# Get API key from environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("ERROR: ElevenLabs API key not found! Please set it in the .env file.")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using the ElevenLabs API (1.50.7).
    """
    try:
        # Use the correct voice_id for Rachel
        audio = client.text_to_speech.convert(
            text=input_text,
            voice_id="21m00Tcm4TlvDq8ikWAM"  # ✅ Rachel's correct voice ID
        )

        # Save and play the audio
        save(audio, output_filepath)
        play(audio)
        print(f"Audio saved as {output_filepath}")

    except Exception as e:
        print(f"Error: {e}")


# Example usage
text_to_speech_with_elevenlabs("Hello, this is ElevenLabs AI.", "elevenlabs_test.mp3")
import os
from elevenlabs.client import ElevenLabs  # Correct import for ElevenLabs v1.50.7
from elevenlabs import save, play

# Get API key from environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("ERROR: ElevenLabs API key not found! Please set it in the .env file.")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using the ElevenLabs API (1.50.7).
    """
    try:
        # Use the correct voice_id for Rachel
        audio = client.text_to_speech.convert(
            text=input_text,
            voice_id="21m00Tcm4TlvDq8ikWAM"  # ✅ Rachel's correct voice ID
        )

        # Save and play the audio
        save(audio, output_filepath)
        play(audio)
        print(f"Audio saved as {output_filepath}")

    except Exception as e:
        print(f"Error: {e}")


# Example usage
text_to_speech_with_elevenlabs("Hello, this is ElevenLabs AI.", "elevenlabs_test.mp3")
