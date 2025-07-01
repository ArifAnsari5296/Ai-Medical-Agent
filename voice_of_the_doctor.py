import os
import platform
import subprocess
from pydub import AudioSegment
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import gTTS for Google TTS
from gtts import gTTS

# Import ElevenLabs TTS
from elevenlabs.client import ElevenLabs
from elevenlabs import save, play

# Get API Key from .env file
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("ERROR: ElevenLabs API key not found! Please set it in the .env file.")

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def text_to_speech_with_gtts(input_text, output_filepath):
    """ Convert text to speech using Google TTS (gTTS) and play it. """
    language = "en"

    # Convert text to speech
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    # Convert MP3 to WAV
    wav_filepath = convert_mp3_to_wav(output_filepath)
    play_audio(wav_filepath)


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """ Convert text to speech using ElevenLabs API and play it. """
    try:
        audio = client.text_to_speech.convert(
            text=input_text,
            voice_id="21m00Tcm4TlvDq8ikWAM"
        )

        # Save as MP3
        save(audio, output_filepath)
        print(f"Audio saved to {output_filepath}")

        # Convert MP3 to WAV
        wav_filepath = convert_mp3_to_wav(output_filepath)
        play_audio(wav_filepath)

    except Exception as e:
        print(f"❌ Error: {e}")


def convert_mp3_to_wav(mp3_filepath):
    """ Convert an MP3 file to WAV format for compatibility with Windows SoundPlayer. """
    wav_filepath = mp3_filepath.replace(".mp3", ".wav")
    
    try:
        audio = AudioSegment.from_mp3(mp3_filepath)
        audio.export(wav_filepath, format="wav")
        return wav_filepath
    except Exception as e:
        print(f"⚠️ Error converting MP3 to WAV: {e}")
        return mp3_filepath  # Fall back to MP3 if conversion fails


def play_audio(output_filepath):
    """ Play an audio file based on the OS. """
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"⚠️ Error playing audio: {e}")


# 🔹 Test Google gTTS
gtts_text = "Hi, this is an Puchu"
gtts_output = "gtts_test.mp3"
#text_to_speech_with_gtts(gtts_text, gtts_output)

# 🔹 Test ElevenLabs TTS
elevenlabs_text = "Hi"
elevenlabs_output = "elevenlabs_test.mp3"
#text_to_speech_with_elevenlabs(elevenlabs_text, elevenlabs_output)
