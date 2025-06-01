import matplotlib.pyplot as plt

# 每类书的数量（手动或根据统计得出）
sizes = [6, 3, 1, 1]  # 蓝、红、绿、紫

labels = [
    "Self-help / Growth (6 times)",
    "Fiction (3 times)",
    "Children (1 time)",
    "Business (1 times)"
]

colors = ["#4a90e2", "#f05a28", "#2ecc71", "#ba68c8"]

fig, ax = plt.subplots(figsize=(5, 5))
wedges, texts = ax.pie(
    sizes,
    colors=colors,
    startangle=90,
    wedgeprops=dict(width=0.4),
    labels=labels,
    labeldistance=1.3,
    textprops=dict(fontsize=9)
)

ax.set_title("Category Legend by Frequency", fontsize=12)
plt.tight_layout()
plt.savefig("bk_rep/output/category_legend_donut.svg", format="svg")
plt.close()
print("✅ Donut 图例已保存：bk_rep/output/category_legend_donut.svg")
