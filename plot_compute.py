import csv
import matplotlib.pyplot as plt

data = {}

with open("compute.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        gil = row["gil"]
        threads = int(row["threads"])
        seconds = float(row["seconds"])

        if gil not in data:
            data[gil] = {"threads": [], "seconds": []}

        data[gil]["threads"].append(threads)
        data[gil]["seconds"].append(seconds)

plt.figure()

for gil in sorted(data):
    label = f"GIL={gil}"
    plt.plot(data[gil]["threads"], data[gil]["seconds"], marker="o", label=label)

plt.xlabel("Threads")
plt.ylabel("Seconds")
plt.title("GIL Mode and Thread Count Performance")
plt.legend()
plt.tight_layout()
plt.savefig("compute.svg")

print("Wrote compute.svg")
