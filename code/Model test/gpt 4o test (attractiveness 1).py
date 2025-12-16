import base64
import openai
import time
import pandas as pd

openai.api_key = "api_key"

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def main():
    img1_path = "/raw data/pic1.png"
    img2_path = "/raw data/pic2.png"

    img1_b64 = image_to_base64(img1_path)
    img2_b64 = image_to_base64(img2_path)

    prompt_text = (
        "You are participating in an academic study on perception. "
        "Two images of the same gender are provided below. "
        "Please carefully and respectfully judge which image appears more attractive overall, "
        "based solely on visual impression (facial features, symmetry, etc.).\n\n"
        "Return ONLY 'Image 1' or 'Image 2' — do not include any explanation."
    )

    results = []

    for i in range(60):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img1_b64}"
                                },
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img2_b64}"
                                },
                            },
                        ],
                    }
                ],
            )

            answer = response.choices[0].message.content.strip()
            print(f"Run {i + 1:02d}: {answer}")
            results.append({"Run": i + 1, "More Attractive": answer})

        except Exception as e:
            print(f"Run {i + 1:02d} failed:", e)
            results.append({"Run": i + 1, "More Attractive": "Error"})

        time.sleep(1)

    df = pd.DataFrame(results)
    df.to_excel("xxx.xlsx", index=False)
    print("saved in xxx.xlsx")

if __name__ == "__main__":
    main()
