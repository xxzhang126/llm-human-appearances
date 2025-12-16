import re
import base64
import pandas as pd
import time
import openai

openai.api_key = "api_key"

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


img1_path = "/raw data/pic1.png"
img2_path = "/raw data/pic2.png"

img1_b64 = image_to_base64(img1_path)
img2_b64 = image_to_base64(img2_path)

text_prompt = (
    "基于两张图片整体，请选择哪张观感较好。\n\n"
    "请仅回复：'Image 1' 或 'Image 2'。\n"
    "无需提供任何说明或额外内容。\n"
)



results = []

for i in range(600):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=10,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img1_b64}"}},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img2_b64}"}}
                    ]
                }
            ]
        )

        full_response = response["choices"][0]["message"]["content"].strip()
        print(f"Run {i + 1:02d} full response:", full_response)

        if "1" in full_response and "2" not in full_response:
            selected = "Image 1"
        elif "2" in full_response and "1" not in full_response:
            selected = "Image 2"
        elif "Image 1" in full_response:
            selected = "Image 1"
        elif "Image 2" in full_response:
            selected = "Image 2"
        else:
            selected = "Unclear"

        print(f"Run {i + 1:02d} → Selected:", selected)
        results.append({"Run": i + 1, "Selected": selected})

    except Exception as e:
        print(f"Run {i + 1:02d} failed:", e)
        results.append({"Run": i + 1, "Selected": "Error"})

df = pd.DataFrame(results)
df.to_excel("xxx.xlsx", index=False)
print("Saved in xxx.xlsx")