from pathlib import Path
from openai import OpenAI

# Read API key
api_key = (
    Path(__file__).parent /
    "api_key.txt"
).read_text().strip()

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-5",
    input="Hello world. Please say hello to the world."
)

print(response.output_text)
