import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL_NAME="llama-3.3-70b-versatile"
GROQ_KEY = os.environ.get("GROQ_API")
client = Groq(api_key=GROQ_KEY)


def generate_response_with_context(prompt, context):
    # Construct the final prompt for the LLaMA model
    final_prompt = (
        f"Context: {context}\n\n"
        f"Question: {prompt}\n"
        "Answer:"
    )

    # Send the prompt to the Groq API
    chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": final_prompt},
                {"role": "user", "content": prompt},
            ],
            model=LLM_MODEL_NAME,
        )

    assistant_response = chat_completion.choices[0].message.content

    # Extract the response text
    return assistant_response

