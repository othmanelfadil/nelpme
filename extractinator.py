import json
import os
import asyncio
import random
from dotenv import load_dotenv
from groq import AsyncGroq


load_dotenv()

data = [json.loads(line) for line in open('etymology_sorted.jsonl', 'r', encoding='utf-8')]

#print(data[0])
#print(len(data)) it's 52126

entry = data[random.randrange(len(data))]
print(entry)
word = entry.get("word")
etymology = entry.get("etymology", "")



prompt = f"""
You are a historical linguist. For the word '{word}', analyze this etymology description:

'{etymology}'

Return a JSON object with these rules:

1. "word": the original word.
2. "history": a list of dictionaries, each representing **one distinct historical stage** in the word's history. Each dictionary must include:
   - "date_text": textual description of the date (e.g., "Middle English", "17th century"), or null if unknown.
   - "date_start": earliest possible year for this stage (integer), or null if unknown.
   - "date_end": latest possible year for this stage (integer), or null if unknown.
   - "place": the place of origin, or null if unknown.
   - "lat": latitude of the place in decimal, or null if unknown.
   - "lon": longitude of the place in decimal, or null if unknown.
   - "word": the historical form.
3. **Do not merge multiple stages into one dictionary.** Each stage must be a separate entry in "history".
4. If the etymology is just a prefix, suffix, or single word, "history" can be empty.
5. Only return valid JSON — no extra text or explanation.
"""

client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"),)

async def main() -> None:
    chat_completion = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-20b",
        )

    content = chat_completion.choices[0].message.content

    try:
        structured = json.loads(content)
    except json.JSONDecodeError:
        structured = {"word": word, "history": []} 

    print(json.dumps(structured, indent=2, ensure_ascii=False))

asyncio.run(main())


'''
client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"),)

async def main() -> None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of low latency LLMs",
            }
        ],
        model="openai/gpt-oss-20b",
    )
    print(chat_completion.choices[0].message.content)


asyncio.run(main())
'''
