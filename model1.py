import google.generativeai as genai
import time
import logging
import grpc

# Configure the Gemini API (replace with your actual key)
genai.configure(api_key="api-key")

# Logging setup
logging.basicConfig(level=logging.INFO)

# Model configuration
generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 8192,
}

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Initialize the Gemini model
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    logging.info("✅ Gemini 1.5 Pro model initialized successfully.")
except Exception as e:
    logging.error("❌ Error initializing Gemini model: %s", e)
    raise SystemExit(e)
