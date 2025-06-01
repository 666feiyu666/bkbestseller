import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import textwrap

plt.rcParams['font.family'] = 'Arial Unicode MS'  
plt.rcParams['axes.unicode_minus'] = False

def wrap_labels(labels, width):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]

def plot_repeated_titles(csv_path):
    df = pd.read_csv(csv_path)
    title_counts = df['title'].value_counts()
    repeated_titles = title_counts[title_counts > 2].sort_values()

    wrapped_labels = wrap_labels(repeated_titles.index.tolist(), 35)

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(
        wrapped_labels,
        repeated_titles.values,
        color="#4a90e2",
        height=0.6   # 💡 添加此行调整柱宽，默认是1，改为0.6更疏朗
    )

    ax.set_title("Books Appearing Multiple Times", fontsize=16)
    ax.set_xlabel("Number of Appearances", fontsize=12)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))  
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig("bk_rep/output/repeated_titles.svg", format='svg')
    plt.close()
    print("✅ Saved plot to: bk_rep/output/repeated_titles.svg")
