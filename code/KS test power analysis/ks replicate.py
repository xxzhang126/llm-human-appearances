import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

def simulate_power(n, delta, iterations=10000, alpha=0.2, seed=None):
    """
    Monte Carlo simulation for two-sample KS test power with normal distribution.
    - n: sample size per group
    - delta: mean difference / sigma (sigma=1)
    - iterations: number of simulations
    - alpha: significance level
    """
    rng = np.random.default_rng(seed)
    rejections = 0

    for _ in range(iterations):
        x1 = rng.normal(0, 1, n)          # sample 1, mean=0
        x2 = rng.normal(delta, 1, n)      # sample 2, mean=delta
        stat, pval = ks_2samp(x1, x2)
        if pval < alpha:
            rejections += 1

    return rejections / iterations  # estimated power


def find_min_sample(delta, target_power, max_n=150, step=2, iterations=10000):
    """
    Find the minimum sample size per group required to achieve given power.
    """
    for n in range(4, max_n+1, step):
        power = simulate_power(n, delta, iterations=iterations)
        if power >= target_power:
            return n
    return None


if __name__ == "__main__":
    deltas = [0.5, 0.7, 0.9]
    powers = [0.8, 0.9, 0.95, 0.99]

    results = { "Power": [] }
    for d in deltas:
        results[f"δ={d}"] = []

    for p in powers:
        results["Power"].append(f"{int(p*100)}%")
        for d in deltas:
            n_required = find_min_sample(d, p, iterations=10000)
            results[f"δ={d}"].append(n_required if n_required else "-")


    df = pd.DataFrame(results)


    output_file = "KS_Table.xlsx"
    df.to_excel(output_file, index=False)

    print(f"结果已保存到 {output_file}")
    print(df)
