import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(year):
    input_path = f"output/wordanalysis/{year}_keywords.csv"
    output_path = f"output/wordanalysis/{year}_wordcloud.png"

    df = pd.read_csv(input_path)
    word_freq = dict(zip(df['word'], df['frequency']))

    wc = WordCloud(width=1000, height=600, background_color='white')
    wc.generate_from_frequencies(word_freq)

    plt.figure(figsize=(12, 7))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"🌥️ {year} 词云图已保存至 {output_path}")

# 生成所有年份词云图
for year in range(1995, 2025):
    generate_wordcloud(year)
