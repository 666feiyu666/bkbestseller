import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Arial Unicode MS'  # macOS推荐字体
plt.rcParams['axes.unicode_minus'] = False

# 价格趋势
def avg_price_by_year(csv_path):
    df = pd.read_csv(csv_path)
    df = df[df['price'] != "N/A"].copy()
    df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)


    avg_price = df.groupby('year')['price'].mean()

    plt.figure(figsize=(10, 5))
    avg_price.plot(marker='o')
    plt.title("平均畅销书价格（1995–2024）")
    plt.ylabel("平均价格（美元）")
    plt.xlabel("年份")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/avg_price_by_year.png")
    plt.close()
    print("✅ 保存图表：output/avg_price_by_year.png")

# 评分趋势
def plot_avg_rating_trend(csv_path):
    df = pd.read_csv(csv_path)

    # 清洗评分字段
    df = df[df['rating'] != "N/A"].copy()
    df['rating'] = df['rating'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)

    # 按年份取平均
    avg_rating = df.groupby('year')['rating'].mean()

    # 绘图
    plt.figure(figsize=(10, 5))
    avg_rating.plot(marker='o', color='green')
    plt.title("畅销书平均评分变化趋势（2000–2024）")
    plt.xlabel("年份")
    plt.ylabel("平均评分（5分制）")
    plt.ylim(4.0, 5.1)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("output/avg_rating_trend.png")
    plt.close()
    print("✅ 保存图表：output/avg_rating_trend.png")

# 受欢迎的作者
def plot_repeated_authors(csv_path):
    df = pd.read_csv(csv_path)
    author_counts = df['author'].value_counts()
    repeated_authors = author_counts[author_counts > 2]

    plt.figure(figsize=(10, 6))
    repeated_authors.sort_values().plot(kind='barh')
    plt.title("多次上榜的作者")
    plt.xlabel("上榜次数")
    plt.tight_layout()
    plt.savefig("output/repeated_authors.png")
    plt.close()
    print("✅ 保存图表：output/repeated_authors.png")

def plot_author_repetition_donut(csv_path):
    import matplotlib.cm as cm
    df = pd.read_csv(csv_path)
    author_counts = df['author'].value_counts()
    repetition_dist = author_counts.value_counts().sort_index()  # 出现次数 → 作者数

    labels = [f"{k}次" for k in repetition_dist.index]
    values = repetition_dist.values
    colors = cm.tab20.colors[:len(values)]

    plt.figure(figsize=(6, 6))
    wedges, _ = plt.pie(
        values,
        startangle=90,
        wedgeprops=dict(width=0.4),
        colors=colors
    )
    plt.legend(wedges, labels, title="上榜次数", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.title("作者上榜次数分布（含1次）")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("output/author_repetition_donut.png")
    plt.close()
    print("✅ 保存图表：output/author_repetition_donut.png")



# 受欢迎的书目
def plot_repeated_titles(csv_path):
    df = pd.read_csv(csv_path)
    title_counts = df['title'].value_counts()
    repeated_titles = title_counts[title_counts > 2]

    plt.figure(figsize=(10, 6))
    repeated_titles.sort_values().plot(kind='barh')
    plt.title("多次上榜的书名")
    plt.xlabel("上榜次数")
    plt.tight_layout()
    plt.savefig("output/repeated_titles.png")
    plt.close()
    print("✅ 保存图表：output/repeated_titles.png")

def plot_title_repetition_donut(csv_path):
    import matplotlib.cm as cm
    df = pd.read_csv(csv_path)
    title_counts = df['title'].value_counts()
    repetition_dist = title_counts.value_counts().sort_index()  # 出现次数 → 书名数

    labels = [f"{k}次" for k in repetition_dist.index]
    values = repetition_dist.values
    colors = cm.tab20.colors[:len(values)]

    plt.figure(figsize=(6, 6))
    wedges, _ = plt.pie(
        values,
        startangle=90,
        wedgeprops=dict(width=0.4),
        colors=colors
    )
    plt.legend(wedges, labels, title="上榜次数", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.title("书名上榜次数分布（含1次）")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("output/title_repetition_donut.png")
    plt.close()
    print("✅ 保存图表：output/title_repetition_donut.png")

# 平装还是精装？
def plot_format_pie(csv_path):
    df = pd.read_csv(csv_path)

    # 标准化格式名称
    df = df[df['format'] != "N/A"].copy()
    df['format'] = df['format'].str.lower().str.strip()
    df['format'] = df['format'].replace({
        'hardcover': 'Hardcover',
        'paperback': 'Paperback',
        'mass market paperback': 'Paperback',
        'audio cd': 'Other',
        'spiral-bound': 'Other',
        'board book': 'Other',
        'kindle edition': 'Other',
        'kindle': 'Other',
        'cards': 'Other',
        'other': 'Other',
    })
    df['format'] = df['format'].apply(lambda x: x.capitalize() if x in ['Hardcover', 'Paperback'] else 'Other')

    format_counts = df['format'].value_counts()

    # 饼状图绘制
    plt.figure(figsize=(6, 6))
    plt.pie(format_counts, labels=format_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title("畅销书装帧形式分布")
    plt.axis('equal')  # 保持圆形
    plt.tight_layout()
    plt.savefig("output/book_format_pie.png")
    plt.close()
    print("✅ 保存图表：output/book_format_pie.png")