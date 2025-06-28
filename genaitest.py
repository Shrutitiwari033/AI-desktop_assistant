import google.generativeai as genai
from config import api_key

# Configure the API key
genai.configure(api_key=api_key)

# Initialize the Generative Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate content
response = model.generate_content("Write an email to my boss for resignation?")

# Print the generated text
print(response.text)