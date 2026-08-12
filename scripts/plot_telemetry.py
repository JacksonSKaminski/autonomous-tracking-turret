import glob
import os
import pandas as pd
import matplotlib.pyplot as plt

files = glob.glob('logs/*.csv')
latest = max(files, key=os.path.getmtime)

df = pd.read_csv(latest)
print(df)

fig, axes = plt.subplots(5, 1, figsize=(12, 15))

axes[0].plot(df["Latency (ms)"])
axes[0].set_title("Latency (ms)")

state_map = {"SEARCH": 0, "HOLD": 1, "TRACK": 2}
axes[1].plot(df["ROE State"].map(state_map))
axes[1].set_yticks([0, 1, 2])
axes[1].set_yticklabels(["SEARCH", "HOLD", "TRACK"])
axes[1].set_title("ROE State")

axes[2].plot(df["cx"], label="cx")
axes[2].plot(df["cy"], label="cy")
axes[2].legend()
axes[2].set_title("Centroid Position")

axes[3].plot(df["Angle X"], label="Pan Error")
axes[3].plot(df["Angle Y"], label="Tilt Error")
axes[3].legend()
axes[3].set_title("Pan and Tilt Error (degrees)")

axes[4].plot(df["Pan Output"], label="Pan PID Output")
axes[4].plot(df["Tilt Output"], label="Tilt PID Output")
axes[4].legend()
axes[4].set_title("PID Controller Outputs")

plt.tight_layout(pad=2.0)
plt.show()