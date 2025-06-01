import matplotlib.pyplot as plt

def draw_thinking_stickman(ax, origin=(0, 0), scale=1.0):
    x, y = origin

    # Head (tilted slightly to right)
    head = plt.Circle((x + 0.1 * scale, y + 1.5 * scale), 0.3 * scale, fill=False, lw=2)
    ax.add_patch(head)

    # Eyes (looking top-right)
    eye1 = (x + 0.1 * scale + 0.07 * scale, y + 1.5 * scale + 0.07 * scale)
    eye2 = (x + 0.1 * scale + 0.14 * scale, y + 1.5 * scale + 0.03 * scale)
    ax.plot(*eye1, 'ko', markersize=3)
    ax.plot(*eye2, 'ko', markersize=3)

    # Body
    ax.plot([x, x], [y + 1.2 * scale, y], color='black', lw=2)

    # Left arm
    ax.plot([x, x - 0.4 * scale], [y + 1.1 * scale, y + 0.8 * scale], color='black', lw=2)

    # Right arm touching head
    ax.plot([x, x + 0.3 * scale], [y + 1.1 * scale, y + 1.5 * scale], color='black', lw=2)

    # Legs
    ax.plot([x, x - 0.4 * scale], [y, y - 0.5 * scale], color='black', lw=2)
    ax.plot([x, x + 0.4 * scale], [y, y - 0.5 * scale], color='black', lw=2)

    # Text
    ax.text(x + 0.5 * scale, y + 1.8 * scale, "Hmm...", fontsize=10, style='italic')
    
    # Background explanation text (multi-line)
    message = (
        "Still in progress.\n"
        "The data are from Amazon bestsellers (1995–2024).\n"
        "Top 10 books each year were selected.\n"
        "Now I'm exploring how to visualize it\n"
        "using xkcd-style storytelling."
    )

    ax.text(x + 0.5 * scale, y + 1.4 * scale, message,
            fontsize=9, va='top', ha='left', linespacing=1.3)

    # Signature
    ax.text(x, y - 0.8 * scale, "Inspired by xkcd style", fontsize=8, alpha=0.6)

# 示例使用
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)

draw_thinking_stickman(ax, origin=(0.5, 0.5), scale=1.2)

plt.axis('off')
plt.tight_layout()
plt.savefig("bk_rep/output/stickman_intro.svg", format="svg")
plt.show()
