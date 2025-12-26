import pandas as pd
import numpy as np

# ========= 可改参数 =========
INPUT_PATH = "data.xlsx"
OUTPUT_PATH = "Bootstrapresult.xlsx"
N_ITER = 10000        
SAMPLE_N = 50          
# ===========================


def build_case(row: pd.Series) -> str:
    gender = "M" if int(row["CandidateMale"]) == 1 else "F"
    attr = "A" if int(row["Attractive"]) == 1 else "P"

    if int(row["Backoffice"]) == 1:
        role = "B"
    elif int(row["Client"]) == 1:
        role = "C"
    elif int(row["General"]) == 1:
        role = "G"
    else:
        role = "UNK"

    return f"{gender}{attr}{role}"


def role_from_case(case_label: str) -> str:
    return case_label[2]


def attr_from_case(case_label: str) -> int:
    return 1 if case_label[1] == "A" else 0


def male_from_case(case_label: str) -> int:
    return 1 if case_label[0] == "M" else 0


def main():
    df = pd.read_excel(INPUT_PATH)

    required_cols = [
        "AI", "CVEvaluation", "CandidateMale",
        "Backoffice", "Client", "General", "Attractive"
    ]
    for c in required_cols:
        if c not in df.columns:
            raise ValueError(f"Missed: {c}")

    for c in ["AI", "CandidateMale", "Backoffice", "Client", "General", "Attractive"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=required_cols).copy()

    for c in ["AI", "CandidateMale", "Backoffice", "Client", "General", "Attractive"]:
        df[c] = df[c].astype(int)

    role_sum = df["Backoffice"] + df["Client"] + df["General"]
    df = df[role_sum == 1].copy()

    df["Case"] = df.apply(build_case, axis=1)

    group_cols = ["AI", "Backoffice", "Client", "General", "CandidateMale", "Attractive"]

    size_check = df.groupby(group_cols).size().reset_index(name="n")
    if (size_check["n"] < SAMPLE_N).any():
        raise ValueError("samples are not enough in some Case groups.")

    rng = np.random.default_rng()

    records = []

    for it in range(1, N_ITER + 1):
        means = []

        for keys, g in df.groupby(group_cols, dropna=False):
            ai, *_ = keys
            case_label = g["Case"].mode().iloc[0]

            rs = int(rng.integers(0, 2**31 - 1))
            sample = g.sample(n=SAMPLE_N, replace=False, random_state=rs)
            mean_val = sample["CVEvaluation"].mean()

            means.append({
                "Iter": it,
                "AI": int(ai),
                "Case": case_label,
                "Mean": mean_val
            })

        means_df = pd.DataFrame(means)
        means_df["Role"] = means_df["Case"].apply(role_from_case)

        for ai in [0, 1]:
            sub_ai = means_df[means_df["AI"] == ai]

            for role in ["B", "C", "G"]:
                sub_role = sub_ai[sub_ai["Role"] == role].copy()
                sub_role["_random"] = rng.random(len(sub_role))
                sub_role = sub_role.sort_values(
                    by=["Mean", "_random"],
                    ascending=[False, False]
                ).reset_index(drop=True)

                for idx in range(len(sub_role)):
                    case_label = sub_role.loc[idx, "Case"]

                    records.append({
                        "Iter": it,
                        "AI": ai,
                        "Role": role,
                        "RankInRole": idx + 1,  
                        "Case": case_label,
                        "Mean": sub_role.loc[idx, "Mean"],
                        "Attractive": attr_from_case(case_label),
                        "Male": male_from_case(case_label),
                    })


    out_df = pd.DataFrame(records)

    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        out_df.to_excel(writer, index=False, sheet_name="Random50_AllRanks")

    print("Saved as:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
