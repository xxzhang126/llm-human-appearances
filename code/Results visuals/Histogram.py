import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ========== 1. Read Excel ==========
file_path = "Alldata_temp=0.7_1208.xlsx"   
df = pd.read_excel(file_path)

# ========== 2. Filter ==========
filtered_df = df[df["AI"] == 0]
# filtered_df = df[(df["AI"] == 0) & (df["General"] == 1) & (df["CandidateMale"] == 1)]

# filtered_df = df.copy()


# ========== 3. Prepare for proportion ==========
score_range = range(1, 11) 

# Frequency for Attractive = 1 
count_attr_1 = filtered_df[filtered_df["Attractive"] == 1]["CVEvaluation"] \
    .value_counts().reindex(score_range, fill_value=0)

# Frequency for Attractive = 0 
count_attr_0 = filtered_df[filtered_df["Attractive"] == 0]["CVEvaluation"] \
    .value_counts().reindex(score_range, fill_value=0)

# Calculate the propotion
total_attr_1 = count_attr_1.sum()
total_attr_0 = count_attr_0.sum()

prop_attr_1 = count_attr_1 / total_attr_1 if total_attr_1 > 0 else count_attr_1
prop_attr_0 = count_attr_0 / total_attr_0 if total_attr_0 > 0 else count_attr_0


# ========== 4. Draw the figure ==========
x = np.arange(len(score_range))
width = 0.35  # width for each bar

plt.figure(figsize=(8, 6))

plt.bar(x - width/2, prop_attr_1, width, label='Attractive')
plt.bar(x + width/2, prop_attr_0, width, label='Plain')

plt.xticks(x, score_range)
plt.xlabel("CV Score")
plt.ylabel("Proportion")
plt.title("Distribution of CV Score-HR Professional")
plt.legend()

plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# ========== 5. Save the figure ==========
output_file = "Histogram_Humanfullsample.png"
plt.savefig(output_file, dpi=300)
plt.show()

print(f"Saved as: {output_file}")
