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
