import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（SimHei）支持中文
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号

class CentralBankGame:
    def __init__(self, root):
        self.root = root
        self.root.title("货币风暴：央行行长的抉择")
        self.root.geometry("1100x650")
        self.root.configure(bg='#f9f9f9')

        self.day = 0
        self.gdp = 100
        self.inflation = 50
        self.unemployment = 50
        self.interest_rate = 5.0
        self.money_supply = 100

        self.history = []

        self.create_widgets()
        self.update_charts()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("微软雅黑", 10), background="#f9f9f9")
        style.configure("TButton", font=("微软雅黑", 10))
        style.configure("Title.TLabel", font=("微软雅黑", 12, "bold"), background="#f9f9f9")
        style.configure("Action.TButton", font=("微软雅黑", 10, "bold"), background="#5c85d6", foreground="white")

        # 主布局
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 左边：控制区域
        control_frame = ttk.LabelFrame(main_frame, text="政策调控区", padding=15)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # 利率设置
        ttk.Label(control_frame, text="利率 (%)", style="Title.TLabel").pack(anchor=tk.W, pady=(0,5))
        self.rate_entry = ttk.Entry(control_frame, width=10)
        self.rate_entry.pack(pady=5)
        self.rate_entry.insert(0, "5.0")

        # 货币供应设置
        ttk.Label(control_frame, text="货币供应 (指数)", style="Title.TLabel").pack(anchor=tk.W, pady=(15,5))
        self.money_entry = ttk.Entry(control_frame, width=10)
        self.money_entry.pack(pady=5)
        self.money_entry.insert(0, "100")

        # 执行按钮
        ttk.Button(control_frame, text="执行政策", command=self.apply_policy, style="Action.TButton").pack(pady=15)
        ttk.Button(control_frame, text="查看帮助", command=self.show_help).pack(pady=5)

        # 状态面板
        status_frame = ttk.LabelFrame(control_frame, text="当前经济状态", padding=10)
        status_frame.pack(pady=20, fill=tk.X)

        self.status_labels = {
            'day': ttk.Label(status_frame, text="📅 天数: 0"),
            'gdp': ttk.Label(status_frame, text="📈 GDP: 100"),
            'inflation': ttk.Label(status_frame, text="💹 通胀率: 50"),
            'unemployment': ttk.Label(status_frame, text="👷‍♂️ 失业率: 50")
        }
        for lbl in self.status_labels.values():
            lbl.pack(anchor=tk.W, pady=2)

        # 图表区域
        chart_frame = ttk.Frame(main_frame)
        chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def apply_policy(self):
        try:
            rate = float(self.rate_entry.get())
            money = float(self.money_entry.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效数字")
            return

        # 经济变量变化逻辑
        self.day += 1
        delta_gdp = (money - 100) * 0.5 - (rate - 5) * 0.3 + random.randint(-5, 5)
        delta_inflation = (money - 100) * 0.6 - rate * 0.4 + random.randint(-3, 3)
        delta_unemployment = -(money - 100) * 0.3 + rate * 0.5 + random.randint(-4, 4)

        self.gdp = max(0, self.gdp + delta_gdp)
        self.inflation = min(100, max(0, self.inflation + delta_inflation))
        self.unemployment = min(100, max(0, self.unemployment + delta_unemployment))
        self.interest_rate = rate
        self.money_supply = money

        self.history.append((self.day, self.gdp, self.inflation, self.unemployment))
        self.update_charts()
        self.update_status()

    def update_status(self):
        self.status_labels['day'].config(text=f"📅 天数: {self.day}")
        self.status_labels['gdp'].config(text=f"📈 GDP: {int(self.gdp)}")
        self.status_labels['inflation'].config(text=f"💹 通胀率: {int(self.inflation)}")
        self.status_labels['unemployment'].config(text=f"👷‍♂️ 失业率: {int(self.unemployment)}")

    def update_charts(self):
        self.ax.clear()
        days = [d[0] for d in self.history]
        gdps = [d[1] for d in self.history]
        inflations = [d[2] for d in self.history]
        unemployments = [d[3] for d in self.history]

        self.ax.plot(days, gdps, label='GDP', color='green', marker='o')
        self.ax.plot(days, inflations, label='通胀率', color='red', marker='s')
        self.ax.plot(days, unemployments, label='失业率', color='blue', marker='^')

        self.ax.set_title("经济指标变化图", fontsize=12)
        self.ax.set_xlabel("天数", fontsize=10)
        self.ax.set_ylabel("指标值", fontsize=10)
        self.ax.legend()
        self.ax.grid(True, linestyle='--', color='#cccccc')
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.tick_params(labelsize=9)

        self.canvas.draw()

    def show_help(self):
        messagebox.showinfo("帮助说明", "游戏帮助", """
【基本玩法】
您作为央行行长，通过调整利率和货币供应来影响经济。
每次点击"执行政策"后，经济指标会更新1天。

【经济指标】
📈 GDP：越高越好（0-100+）
💹 通胀：20-80较安全（过高或过低都危险）
👷 失业：越低越好（0-100）

【政策影响】
↑利率：抑制通胀，但会降低GDP、增加失业
↓利率：刺激经济，但可能推高通胀
↑货币：刺激GDP、降低失业，但推高通胀
↓货币：抑制通胀，但会减少GDP、增加失业

【新手建议】
1. 开始时保持利率5%、货币100
2. 观察3-5天后小幅调整
3. 避免单次调整幅度过大（利率±1%，货币±20）
4. 通胀>80时提高利率，<20时降低利率

【按键说明】
利率(%)：输入新利率（如4.5）
货币供应：输入新值（如120）
执行政策：应用当前设置
祝你好运！
    """)

if __name__ == "__main__":
    root = tk.Tk()
    app = CentralBankGame(root)
    root.mainloop()
