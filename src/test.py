
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from get_fm import *
from my_counter import *

counter = MyObjectCounter(
    model_path="yolov8n.pt",
    show=False
)

def test():
    frames = extract_frames("./vid/vid.mp4", )
    results = []

    for frame_id, frame in frames:
        count = counter.process_frame(frame, test=True)
        results.append((frame_id, count))
        
    expected = pd.read_csv("expected_counts.csv")
    actual_df = pd.DataFrame(results, columns=["frame_id", "actual_count"])
    merged = pd.merge(expected, actual_df, on="frame_id")

    merged["error"] = merged["actual_count"] - merged["expected_count"]
    merged["abs_error"] = merged["error"].abs()

    mae = merged["abs_error"].mean()
    mape = (merged["abs_error"] / merged["expected_count"]).mean() * 100
    accuracy = 100 - mape

    print(accuracy)

    fig, ax = plt.subplots()

    ax.plot(merged["frame_id"], merged["expected_count"], label="Ожидаемо", linewidth=2)
    ax.plot(merged["frame_id"], merged["actual_count"], label="Фактически", linewidth=2)

    # Подписи и сетка
    ax.set_title("Сравнение результатов подсчёта")
    ax.set_xlabel("ID кадра")
    ax.set_ylabel("Кол-во людей")
    ax.grid(True)
    ax.legend()

    # ❗ Обязательная строка для оси X в целых числах
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Сохранение (по желанию)
    # plt.savefig("test_results.png", dpi=300, bbox_inches='tight')

    plt.show()
    
test()