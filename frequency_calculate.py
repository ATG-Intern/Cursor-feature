import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

def plot_frequency_domain(signal, sample_rate):
    # FFT 수행
    fft_result = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1 / sample_rate)

    # 양의 주파수만 선택
    positive_freqs = freqs[:len(freqs) // 2]
    positive_fft = np.abs(fft_result[:len(fft_result) // 2])

    # 플롯 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(positive_freqs, positive_fft)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude')
    ax.set_title('Frequency Domain')
    ax.grid(True)

    vertical_lines = []  # 세로선을 저장할 리스트
    selected_point = None  # 선택된 점을 저장할 변수

    def on_click(event):
        nonlocal vertical_lines, selected_point
        if event.inaxes == ax:
            clicked_freq = event.xdata

            # 이전 세로선 제거
            for line in vertical_lines:
                line.remove()
            vertical_lines.clear()

            # 이전에 선택된 점 제거
            if selected_point:
                selected_point.remove()
                selected_point = None

            # 새로운 세로선 추가
            max_freq = max(positive_freqs)
            for i in range(1, int(max_freq // clicked_freq) + 1):
                freq = i * clicked_freq
                line = ax.axvline(x=freq, color='r', linestyle='--', alpha=0.5)
                vertical_lines.append(line)

            # 가장 가까운 주파수 찾기
            idx = np.argmin(np.abs(positive_freqs - clicked_freq))
            nearest_freq = positive_freqs[idx]
            nearest_amp = positive_fft[idx]

            # 결과 출력
            print(f"선택한 지점 - 주파수: {clicked_freq:.2f} Hz")
            print(f"가장 가까운 주파수 성분 - 주파수: {nearest_freq:.2f} Hz, 진폭: {nearest_amp:.2f}")

            # 선택한 지점 표시
            selected_point, = ax.plot(nearest_freq, nearest_amp, 'ro', markersize=10)
            plt.draw()

    # 클릭 이벤트 연결
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()

# 예제 신호 생성 (무작위 주파수 성분)
sample_rate = 1000  # 샘플링 레이트 (Hz)
duration = 1  # 신호 지속 시간 (초)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# 무작위 주파수 성분 생성
num_components = 10  # 주파수 성분의 수
np.random.seed(42)  # 재현성을 위한 시드 설정
frequencies = np.random.uniform(10, 200, num_components)  # 10Hz에서 200Hz 사이의 무작위 주파수
amplitudes = np.random.uniform(0.1, 1.0, num_components)  # 0.1에서 1.0 사이의 무작위 진폭

# 복합 신호 생성
signal = np.zeros_like(t)
for freq, amp in zip(frequencies, amplitudes):
    signal += amp * np.sin(2 * np.pi * freq * t)

# 주파수 도메인 플롯 생성
plot_frequency_domain(signal, sample_rate)

# 생성된 주파수 성분 출력
print("\n생성된 주파수 성분:")
print("---")
for i, (freq, amp) in enumerate(zip(frequencies, amplitudes), 1):
    print(f"{i}. 주파수: {freq:.2f} Hz, 진폭: {amp:.2f}")