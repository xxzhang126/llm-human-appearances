import numpy as np
import pandas as pd
from scipy.stats import ks_2samp


delta = 0.5
power_levels = [0.8]
sample_sizes = range(4, 152, 2)
iterations = 10000
sigma = 1
c_alpha = 1.07


results = []

for power_target in power_levels:
    found_sample_size = None
    for n2 in sample_sizes:
        n1 = n2 + 1
        rejections = 0
        for _ in range(iterations):
            x1 = np.random.normal(loc=0, scale=sigma, size=n1)
            x2 = np.random.normal(loc=delta, scale=sigma, size=n2)
            d_stat, _ = ks_2samp(x1, x2, alternative='two-sided', mode='asymp')
            critical_value = c_alpha * np.sqrt((n1 + n2) / (n1 * n2))
            if d_stat > critical_value:
                rejections += 1
        power = rejections / iterations
        print(f"δ={delta}, Power Target={power_target}, n2={n2}, Power={power:.3f}")
        if power >= power_target:
            found_sample_size = n2
            break
    results.append(found_sample_size)

# 输出为 Excel
df = pd.DataFrame({"δ=0.5": results}, index=[int(p * 100) for p in power_levels])
df.index.name = "Power (P)"
df.to_excel("ks_simulation_table4_delta_0.5.xlsx")
print("\n 已保存为 ks_simulation_table4_delta_0.5.xlsx")
