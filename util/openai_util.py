import time
import openai
from openai.error import RateLimitError

def completion_with_chatgpt(text: str, model: str = "gpt-4") -> str:
    max_retries = 5
    for i in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "user", "content": text},
                ],
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            wait_time = 2 ** i
            print(f"Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    raise Exception("Max retries exceeded.")