import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 20})

# 假设我们有5个不同的语音识别系统
systems = ['System1', 'System2', 'System3', 'System4', 'System5']

# 延迟数据（单位：秒）
delays = [0.5, 0.6, 0.7, 0.8, 0.9]

# 准确性数据（单位：百分比）
accuracies = [95, 90, 85, 80, 75]

x = np.arange(len(systems))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, delays, width, label='Delay')
rects2 = ax.bar(x + width/2, accuracies, width, label='Accuracy')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by system and metric')
ax.set_xticks(x)
ax.set_xticklabels(systems)
ax.legend()

# Function to add horizontal dashed lines at the top of the bars
def add_dashed_line(rects):
    for rect in rects:
        height = rect.get_height()
        ax.hlines(height, rect.get_x(), rect.get_x() + rect.get_width(), colors='k', linestyles='dashed')

add_dashed_line(rects1)
add_dashed_line(rects2)

fig.tight_layout()

# 保存图像为jpg格式
plt.savefig("output.jpg")

plt.show()