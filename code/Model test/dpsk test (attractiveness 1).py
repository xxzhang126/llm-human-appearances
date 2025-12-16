import base64
import time
import re
import pandas as pd
from openai import OpenAI

client = OpenAI(
    api_key="api_key",
    base_url="https://api.deepseek.com"
)

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def call_deepseek_score(prompt_text):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a respectful and careful visual evaluator."},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

def main():
    img1_path = "/raw data/pic1.png"
    img2_path = "/raw data/pic2.png"

    img1_b64 = image_to_base64(img1_path)
    img2_b64 = image_to_base64(img2_path)

    prompt = (
        "You are participating in an academic study on perception. "
        "Two images of the same gender are provided below. "
        "Please carefully and respectfully judge which image appears more attractive overall, "
        "based solely on visual impression (facial features, symmetry, etc.).\n\n"
        "Return ONLY 'Image 1' or 'Image 2' — do not include any explanation.\n\n"
        f"Image 1: data:image/png;base64,{img1_b64}\n\n"
        f"Image 2: data:image/png;base64,{img2_b64}\n"
    )

    results = []

    for attempt in range(60):
        try:
            full_response = call_deepseek_score(prompt)
            print(f"Attempt {attempt + 1} response:", full_response)
            answer = full_response.strip()
            if "1" in answer and "2" not in answer:
                result = "Image 1"
            elif "2" in answer and "1" not in answer:
                result = "Image 2"
            else:
                result = answer
            results.append({"Attempt": attempt + 1, "More Attractive": result})
        except Exception as e:
            print(f"Attempt {attempt + 1} failed:", e)
        time.sleep(1)

    df = pd.DataFrame(results)
    df.to_excel("xxx.xlsx", index=False)
    print("Saved in xxx.xlsx")

if __name__ == "__main__":
    main()
