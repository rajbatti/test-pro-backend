import os

from google import genai
from dotenv import load_dotenv

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
PROMPT_INSTRUCTIONS = """
You are an AI that extracts multiple-choice questions (MCQs) from HTML.

I will give you an HTML input that contains questions and their options.
Return **only** valid JSON (no explanation, no extra text). The JSON must be a list of objects.

Each object must have these keys:
- "question": string — the question HTML preserved exactly (including <sub>, <sup>, <img>, and MathJax <math> markup).
- "options": array of strings — each option as HTML preserved exactly.
- "correct_option": string — the **plain option label** (like "a", "b", "c", "d", or "1", "2", ...). **Do not** return HTML for correct_option.

IMPORTANT RULES (must follow exactly):
1. Preserve HTML markup for "question" and every entry in "options" exactly as they appear in the input. Do NOT convert to plain text.
2. The options may appear on separate lines or in one line, and can include extra spaces or inconsistent punctuation.Your task is to extract each option label and its corresponding html separately.
3. Preserve all math markup, fractions, and equations exactly.
4. Preserve images as <img src="..."> tags (do not alter the src).
5. `correct_option` must be ONLY the option label (e.g., "a"), lowercase if options were labeled alphabetically.
6. Output must be **valid JSON** only, with no surrounding text or commentary.
7. Check json correctly before sending response .
8. Don't leave any question give all.
9. Remove question number from question.

If you cannot find a correct option, set "correct_option" by solving yourself"".
"""

def call_gemini_extract_mcqs(html: str, system_prompt: str = PROMPT_INSTRUCTIONS):
    user_input = system_prompt + "\n\nHTML_INPUT_START\n" + html + "\nHTML_INPUT_END\n"

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=user_input
        )
        print(response.model_dump_json())
        return response.text
    except Exception as e:
        raise RuntimeError(f"API call failed: {e}")

