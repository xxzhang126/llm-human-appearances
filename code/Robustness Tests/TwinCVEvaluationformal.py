import os
import time
import base64
import fitz  # PyMuPDF
import pandas as pd
from openai import OpenAI

# ============================
# CONFIG
# ============================
API_KEY = "***" 
MODEL_NAME = "gpt-4o"
TEMPERATURE = 0.7

DEMO_EXCEL_PATH = "twindata.xlsx" 
DEMO_SHEET_NAME = None             

PDF_DIR = "."

OUTPUT_XLSX = "twinresults.xlsx"
SLEEP_SECONDS = 1.0 

client = OpenAI(api_key=API_KEY)


JOB_DESC_B = (
    "某公司正在招聘以下职位：作为该运营团队的财务分析师，候选人将在优化成本效率和支持公司战略决策中发挥关键作用。候选人将每天监控和管理交付、运输和物流过程中的成本，确保资源的合理分配。同时，候选人还将分析财务和运营数据，以评估盈利能力和绩效，提供洞见以塑造战略方向。此外，候选人将根据需要为跨职能团队提供财务数据支持。这是一个以数据驱动、以影响为导向的角色，需要较强的分析思维和跨部门协调能力。"
)

JOB_DESC_C = (
    "某公司正在招聘以下职位：作为该客户服务团队的一员，候选人将成为我们客户及其所寻求的专家知识之间的纽带。日常工作中，候选人将参与多个项目，这些项目来自顶尖客户机构的投资人、战略家与交易商，他们需要专家洞见为其决策提供依据。这是一个需要不断沟通的前线职位，要求候选人在多个工作流之间同时进行切换。 "
)

JOB_DESC_G = (
    "某公司正在招聘以下职位：作为该职位职员，候选人需要具备常见的职场能力，例如沟通、团队合作和解决问题的能力。不要求特定的技术背景，候选人可以来自不同的专业领域。"
)


def choose_job_desc(case_value: str) -> str:
    if case_value is None:
        return JOB_DESC_G

    s = str(case_value).strip().upper()
    if "B" in s:
        return JOB_DESC_B
    if "C" in s:
        return JOB_DESC_C
    if "G" in s:
        return JOB_DESC_G

    return JOB_DESC_G


def case_to_pdf_key(case_value: str) -> str:
    if case_value is None:
        raise ValueError("Case is missing (None). Cannot choose PDF.")

    s = str(case_value).strip().upper()
    matches = []

    if "FA" in s:
        matches.append("FA")
    if "FP" in s:
        matches.append("FP")
    if "MA" in s:
        matches.append("MA")
    if "MP" in s:
        matches.append("MP")

    if len(matches) != 1:
        raise ValueError(
            f"Case '{case_value}' must contain exactly one of FA/FP/MA/MP for PDF selection; got matches={matches}."
        )

    return matches[0]


def pdf_path_from_key(pdf_key: str) -> str:
    filename = f"resume-{pdf_key}.pdf"
    path = os.path.join(PDF_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found: {path}")
    return path
    

def append_row_to_excel(row_dict, path):
    df_row = pd.DataFrame([row_dict])

    if not os.path.exists(path):
        df_row.to_excel(path, index=False)
    else:
        with pd.ExcelWriter(path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
            startrow = writer.sheets["Sheet1"].max_row
            df_row.to_excel(writer, index=False, header=False, startrow=startrow)


def pdf_to_images_base64(pdf_path: str):
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        images.append(base64.b64encode(img_bytes).decode("utf-8"))
    return images


def build_persona_prefix(row: pd.Series) -> str:

    def get(col_name: str):
        if col_name in row.index and pd.notna(row[col_name]) and str(row[col_name]).strip() != "":
            return str(row[col_name]).strip()
        return None

    age = get("Age")
    evaluatormale = get("EvaluatorMale")
    nationality = get("Nationality")
    marriage = get("marriage")
    birthplace = get("Birth")
    liveplace = get("Lived")
    education = get("Education")

    BASE_PERSONA = (
        "你是一位专业的人力资源管理者。"
    )

    parts = []
    if age:
        parts.append(f"年龄：{age}")
    if evaluatormale:
        parts.append(f"性别：{evaluatormale}")
    if nationality:
        parts.append(f"民族：{nationality}")
    if marriage:
        parts.append(f"婚姻状况：{marriage}")
    if birthplace:
        parts.append(f"出生地：{birthplace}")
    if liveplace:
        parts.append(f"现居住地：{liveplace}")
    if education:
        parts.append(f"已获得的最高学历：{education}")

    core = ", ".join(parts) if parts else ""


    if core:
        return f"{BASE_PERSONA} 你的人口统计学信息如下：{core}.".strip()
    return f"{BASE_PERSONA}".strip()


Q1_REST = (
    "\n\n"
    "请根据以上职位描述和简历对候选人进行评估，并对该候选人与该职位的匹配度打分。请在1到10分之间进行打分。1表示很不符合，10表示很符合。 "
    "仅返回数字，不要包含任何解释或文字。"
)

questions = {
    "Q2": {
        "prompt": "你认为该候选人在工作场所中的专业能力如何？请在1到7分之间进行打分。1表示完全不具备，7表示完全具备。",
        "column_name": "Answer_Q2",
    },
    "Q3": {
        "prompt": "你认为该候选人在工作场所中的自信水平如何？请在1到7分之间进行打分。1表示完全不具备，7表示完全具备。",
        "column_name": "Answer_Q3",
    },
    "Q4": {
        "prompt": "你认为该候选人在工作场所中的独立工作能力如何？请在1到7分之间进行打分。1表示完全不具备，7表示完全具备。",
        "column_name": "Answer_Q4",
    },
    "Q5": {
        "prompt": "你认为该候选人在工作场所中的竞争意识程度如何？请在1到7分之间进行打分。1表示完全不具备，7表示完全具备。",
        "column_name": "Answer_Q5",
    },
    "Q6": {
        "prompt": "你认为该候选人在工作场所中的认知能力如何？请在1到7分之间进行打分。1表示从不，7表示总是。",
        "column_name": "Answer_Q6",
    },
    "Q7": {
        "prompt": "你认为该候选人在工作场所中会多频繁地展现沟通能力？请在1到7分之间进行打分。1表示从不，7表示总是。",
        "column_name": "Answer_Q7",
    },
    "Q8": {
        "prompt": "你认为候选人在工作场所中会多频繁地展现人际交往能力？请在1到7分之间进行打分。1表示从不，7表示总是。",
        "column_name": "Answer_Q8",
    },
    "Q9": {
        "prompt": "你认为候选人在工作场所中会多频繁地展现领导能力？请在1到7分之间进行打分。1表示从不，7表示总是。",
        "column_name": "Answer_Q9",
    },
    "Q10": {
        "prompt": "你认为候选人在工作场所中会多频繁地展现说服能力？请在1到7分之间进行打分。1表示从不，7表示总是。",
        "column_name": "Answer_Q10",
    },
    "Q11": {
        "prompt": "你认为候选人在工作场所中会多频繁地展现谈判能力？请在1到7分之间进行打分。1表示从不，7表示总是。",
        "column_name": "Answer_Q11",
    },
}


def main():
    # 1) Read demographics Excel

    df_demo = pd.read_excel(DEMO_EXCEL_PATH, sheet_name="Sheet1")
    # df_demo = df_demo.iloc[START_ROW:]
    # df_demo = df_demo.head(1)

    if df_demo.empty:
        raise ValueError("Demographics Excel is empty.")
    if "Case" not in df_demo.columns:
        raise ValueError("Demographics Excel must contain a column named 'Case'.")

    # 2) Prepare PDF image cache (FA/FP/MA/MP)
    pdf_image_cache = {}
    for key in ("FA", "FP", "MA", "MP"):
        path = pdf_path_from_key(key)
        pdf_image_cache[key] = pdf_to_images_base64(path)

    results = []
    total_runs = len(df_demo)

    for idx, row in df_demo.iterrows():
        run_id = idx + 1
        case_val = row.get("Case", "")

        # 3) Choose PDF strictly by Case (FA/FP/MA/MP)
        pdf_key = case_to_pdf_key(case_val)
        images_base64 = pdf_image_cache[pdf_key]

        # 4) Choose job description by Case letter (B/C/G)
        job_desc = choose_job_desc(case_val)

        # 5) Build persona
        persona_prefix = build_persona_prefix(row)

        # 6) Build Q1 prompt (persona + jobdesc + rest)
        q1_prompt = f"{persona_prefix}\n\n{job_desc}{Q1_REST}"

        # 7) Prepare output row (include all original demographics columns)
        run_result = {
            "Run": run_id,
            "Case": case_val,
            "PDF_key": pdf_key,  
        }
        for col in df_demo.columns:
            if col not in run_result:
                run_result[col] = row[col]

        try:
            messages = []

            q1_content = [{"type": "text", "text": q1_prompt}]
            for img_b64 in images_base64:
                q1_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_b64}"}
                })

            messages.append({"role": "user", "content": q1_content})

            for q_key in ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11"]:
                print(f"[{run_id:04d}/{total_runs}] {q_key} | Case={case_val} | PDF={pdf_key}")

                if q_key != "Q1":
                    messages.append({"role": "user", "content": questions[q_key]["prompt"]})

                resp = client.chat.completions.create(
                    model=MODEL_NAME,
                    temperature=TEMPERATURE,
                    messages=messages,
                )

                answer = resp.choices[0].message.content.strip()

                if q_key == "Q1":
                    run_result["Score_Q1"] = answer
                else:
                    run_result[questions[q_key]["column_name"]] = answer

                messages.append({"role": "assistant", "content": answer})

            append_row_to_excel(run_result, OUTPUT_XLSX)

        except Exception as e:
            print(f"Run {run_id:04d} failed: {e}")
            run_result["Score_Q1"] = run_result.get("Score_Q1", "Error")
            for _, meta in questions.items():
                run_result[meta["column_name"]] = run_result.get(meta["column_name"], "Error")
            run_result["Error"] = str(e)
            results.append(run_result)

        time.sleep(SLEEP_SECONDS)

    print(f"Saved as {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
