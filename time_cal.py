import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
matplotlib.use('TkAgg')

class PeriodicityAnalyzer:
    def __init__(self, signal, time):
        self.signal = signal
        self.time = time
        self.start_time = None
        self.interval = None
        self.clicks = []

        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.line, = self.ax.plot(time, signal)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_title('Click to set start time and interval')
        self.ax.grid(True)

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        self.reset_button_ax = plt.axes([0.8, 0.05, 0.1, 0.04])
        self.reset_button = Button(self.reset_button_ax, 'Reset')
        self.reset_button.on_clicked(self.reset)

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        self.clicks.append(event.xdata)
        if len(self.clicks) == 1:
            self.start_time = self.clicks[0]
            self.ax.axvline(x=self.start_time, color='r', linestyle='--')
            self.ax.set_title('Click to set interval')
        elif len(self.clicks) == 2:
            self.interval = abs(self.clicks[1] - self.clicks[0])
            self.analyze_periodicity()

        self.fig.canvas.draw()

    def reset(self, event):
        self.start_time = None
        self.interval = None
        self.clicks = []
        self.ax.clear()
        self.line, = self.ax.plot(self.time, self.signal)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_title('Click to set start time and interval')
        self.ax.grid(True)
        self.fig.canvas.draw()

    def analyze_periodicity(self):
        self.ax.clear()
        self.ax.plot(self.time, self.signal)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_title('Time Domain Signal with Periodicity Analysis')
        self.ax.grid(True)

        collected_y_values = []
        max_time = max(self.time)
        current_time = self.start_time

        while current_time <= max_time:
            self.ax.axvline(x=current_time, color='r', linestyle='--', alpha=0.5)

            idx = np.argmin(np.abs(self.time - current_time))
            y_value = self.signal[idx]
            collected_y_values.append((current_time, y_value))

            current_time += self.interval

        current_time = self.start_time
        while current_time >= 0:
            self.ax.axvline(x=current_time, color='r', linestyle='--', alpha=0.5)

            idx = np.argmin(np.abs(self.time - current_time))
            y_value = self.signal[idx]
            collected_y_values.append((current_time, y_value))

            current_time -= self.interval

        self.fig.canvas.draw()

        print("수집된 y축 값:")
        for t, y in collected_y_values:
            print(f"시간: {t:.2f}s, 진폭: {y:.4f}")

        if len(collected_y_values) > 1:
            y_values = [y for _, y in collected_y_values]
            mean_y = np.mean(y_values)
            std_y = np.std(y_values)
            print(f"\n수집된 y축 값의 평균: {mean_y:.4f}")
            print(f"수집된 y축 값의 표준편차: {std_y:.4f}")
            print(f"변동 계수 (CV): {std_y / mean_y:.4f}")

            if std_y / mean_y < 0.1:
                print("신호가 강한 주기성을 보입니다.")
            elif std_y / mean_y < 0.3:
                print("신호가 중간 정도의 주기성을 보입니다.")
            else:
                print("신호가 약한 주기성을 보이거나 주기성이 없습니다.")
        else:
            print("주기성 평가를 위한 충분한 데이터가 수집되지 않았습니다.")


# 예제 신호 생성
duration = 10  # 신호 지속 시간 (초)
sample_rate = 1000  # 샘플링 레이트 (Hz)
time = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)

# 여러 주파수 성분을 가진 복합 신호 생성
f1, f2, f3 = 1, 2.5, 5  # 주파수 (Hz)
signal = (np.sin(2 * np.pi * f1 * time) +
          0.5 * np.sin(2 * np.pi * f2 * time) +
          0.3 * np.sin(2 * np.pi * f3 * time))

# 노이즈 추가
noise = np.random.normal(0, 0.1, len(time))
signal += noise

# PeriodicityAnalyzer 인스턴스 생성 및 실행
analyzer = PeriodicityAnalyzer(signal, time)
plt.show()