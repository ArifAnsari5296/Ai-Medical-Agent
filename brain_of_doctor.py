# Load environment variables (if using a .env file)
from dotenv import load_dotenv
load_dotenv()

import os
import base64
from groq import Groq

# Step 1: Setup GROQ API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validate API Key
if not GROQ_API_KEY:
    raise ValueError("❌ ERROR: GROQ_API_KEY is missing. Check your .env file.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Step 2: Convert Image to Required Format
def encode_image(image_path):   
    """Encodes an image to Base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Step 3: Setup Multimodal LLM
def analyze_image_with_query(query, encoded_image, model="llama-3.2-90b-vision-preview"):
    """Analyzes an image with a given query using Groq's multimodal model."""
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
            ],
        }
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ ERROR: Failed to analyze image. Details: {str(e)}"

# Example usage
if __name__ == "__main__":
    image_path = "acne.jpg"
    encoded_image = encode_image(image_path)
    query = "Is there something wrong with my face?"

    result = analyze_image_with_query(query, encoded_image)
    print("🩺 Doctor's Analysis:", result)
