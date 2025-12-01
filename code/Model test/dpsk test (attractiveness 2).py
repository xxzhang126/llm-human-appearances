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
        "You are participating in an academic perception study. "
        "Two facial images are shown below. For each image, identify key **observable visual traits** "
        "without making any attractiveness judgment or comparison. Focus only on descriptive facial features.\n\n"
        "For each image, list traits such as (examples):\n"
        "- hair length (long/medium/short)\n"
        "- hair style (straight/wavy/curly/tied up)\n"
        "- eye size (small/medium/large)\n"
        "- eyelid type (single/double)\n"
        "- eyebrow thickness (thin/medium/thick)\n"
        "- face shape (round/oval/heart/square)\n"
        "- nose size (small/medium/prominent)\n"
        "- mouth shape (thin lips/full lips)\n"
        "- skin condition (smooth/visible texture/etc.)\n\n"
        "Output STRICTLY in this JSON format:\n"
        "{\n"
        "  \"Image1\": [\"trait1\", \"trait2\", \"trait3\", ...],\n"
        "  \"Image2\": [\"trait1\", \"trait2\", \"trait3\", ...]\n"
        "}\n\n"
        "Do not compare the two images. Do not include any judgment words (e.g., attractive/pretty). "
        "Just list observable traits.\n\n"
        f"Image1: data:image/png;base64,{img1_b64}\n\n"
        f"Image2: data:image/png;base64,{img2_b64}\n"
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
    df.to_excel("attractiveness_results.xlsx", index=False)
    print("\n结果已保存到 attractiveness_results.xlsx")

if __name__ == "__main__":
    main()
