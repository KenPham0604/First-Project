from google import genai
from dotenv import load_dotenv
import os

# Loading API keys__________________________________________________________________________________________________
load_dotenv("C:\personalstuff\My Work\Code\Project\API\openai.env")

client = genai.Client(api_key=os.getenv("MY_KEY"))
prompt = """
Write a short 3-sentence fantasy story based on this idea: a lantern that grants wishes.

Then provide a short visual description (max 20 words) of the story's key scene, 
suitable for an image generation prompt.

Respond ONLY in this exact JSON format, no other text:
{
  "story": "...",
  "image_prompt": "..."
}
"""
response = client.models.generate_content(
    model = "gemini-3.5-flash" ,
    contents=prompt
)


# Out put clean up_____________________________________________________________________________________
import json

raw_text = response.text.strip()

# Strip markdown code fences if present
if raw_text.startswith("```"):
    raw_text = raw_text.split("```")[1]
    if raw_text.startswith("json"):
        raw_text = raw_text[4:]

data = json.loads(raw_text)

story = data["story"]
image_prompt = data["image_prompt"]

print("STORY:", story)
print("IMAGE PROMPT:", image_prompt)
