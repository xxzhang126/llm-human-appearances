import re
import base64
import pandas as pd
import time
import openai

openai.api_key = "api_key"


def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

image_path = "/raw data/pic.png"
img_b64 = image_to_base64(image_path)

instruction = (
    "请评估该照片。\n\n"
    "1 = 画面整体观感较弱\n"
    "10 = 画面整体观感非常良好\n\n"
    "仅返回一个 1–10 的整数。"
)


results = []

for i in range(30):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=10,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": instruction},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                    ]
                }
            ]
        )

        full_response = response["choices"][0]["message"]["content"].strip()
        print(f"Run {i + 1:02d} full response:", full_response)

        match = re.search(r"\b([1-9]|10)\b", full_response)
        score = int(match.group(1)) if match else "No score"

        print(f"Run {i + 1:02d} → Score:", score)
        results.append({"Run": i + 1, "Score": score})

    except Exception as e:
        print(f"Run {i + 1:02d} failed:", e)
        results.append({"Run": i + 1, "Score": "Error"})


df = pd.DataFrame(results)
df.to_excel("xxx.xlsx", index=False)
print("Saved in xxx.xlsx")
