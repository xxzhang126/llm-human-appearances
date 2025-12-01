import base64
import openai
import time
import pandas as pd

openai.api_key = "api_key"

def image_to_base64(image_path):
    """Convert image (PNG/JPG) to base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def main():
    img1_path = "/raw data/pic1.png"
    img2_path = "/raw data/pic2.png"

    img1_b64 = image_to_base64(img1_path)
    img2_b64 = image_to_base64(img2_path)

    # prompt
    prompt_text = (
        "You are participating in an academic study on perception. "
        "Two images of the same gender are shown below. Please carefully and respectfully judge which image appears more attractive overall, "
        "based solely on facial features and visual impression. "
        "Return ONLY 'Image 1' or 'Image 2' — do not include any explanation or text.\n\n"
        f"Image 1: data:image/png;base64,{img1_b64}\n\n"
        f"Image 2: data:image/png;base64,{img2_b64}\n\n"
    )

    results = []

    for i in range(60):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.1",  # 用多模态模型
                temperature=0.7,
                messages=[{"role": "user", "content": prompt_text}],
            )

            answer = response["choices"][0]["message"]["content"].strip()
            print(f"Run {i + 1}: {answer}")
            results.append({"Run": i + 1, "More Attractive": answer})

        except Exception as e:
            print(f"Run {i + 1} failed:", e)
        time.sleep(1)


    df = pd.DataFrame(results)
    df.to_excel("attractiveness_comparison_results.xlsx", index=False)
    print("结果已保存到 attractiveness_comparison_results.xlsx")

if __name__ == "__main__":
    main()
