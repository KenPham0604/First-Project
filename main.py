from google import genai
from dotenv import load_dotenv
import os
import json
import time
# Note: Create a multiple models solution with retry and wait time feature

# Loading API keys__________________________________________________________________________________________________
load_dotenv(r"C:\personalstuff\My Work\Code\Project\API\openai.env")

client = genai.Client(api_key=os.getenv("GENAI_KEY"))
prompt = """
Write 3 famous sentences from famous books, games, or media in the world about carefulness.

Then provide a short visual description (max 20 words) of that media's key scene, 
suitable for an image generation prompt.

Respond ONLY in this exact JSON format, no other text:
{
  "story": "...",
  "image_prompt": "..."
}
"""
def retry_generation(prompt, max_try = 3):
    model = ["gemini-3.5-flash","gemini-3.5-flash-lite"]
    last_error = None
    for model_name in model:
        for attempt in range(max_try):
            try:
                response = client.models.generate_content(
                model = model_name ,
                contents=prompt
            )
                return response
            except Exception as e:
                last_error = e
                print(f'Attempt {attempt}')
                print(f'{model_name} failing by {e}')
                if attempt < max_try - 1:
                    wait_time = 2**attempt
                    print(f'Retrying in {wait_time}...')
                    time.sleep(wait_time)
    raise RuntimeError(f"Every model failed by {last_error}")

response =  retry_generation(prompt)


# Out put clean up_____________________________________________________________________________________


raw_text = response.text.strip()

# Pull the JSON object out regardless of surrounding text/fences.
# Prefer a fenced ```json ... ``` block if present, otherwise fall back
# to the first {...} object found anywhere in the response.
import re

fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
if fence_match:
    json_str = fence_match.group(1)
else:
    brace_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if not brace_match:
        raise ValueError(f"No JSON object found in model response:\n{raw_text}")
    json_str = brace_match.group(0)

try:
    data = json.loads(json_str)
except json.JSONDecodeError as e:
    raise ValueError(f"Failed to parse JSON from model response: {e}\nExtracted text:\n{json_str}")

story = data["story"]
image_prompt = data["image_prompt"]

print("STORY:", story)
print("IMAGE PROMPT:", image_prompt)