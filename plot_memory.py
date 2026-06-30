import csv
import matplotlib.pyplot as plt

cache_sizes = []
hit_rates = []

with open("memory.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cache_sizes.append(int(row["cache_size"]))
        hit_rates.append(float(row["hit_rate"]))

plt.figure()
plt.plot(cache_sizes, hit_rates, marker="o")
plt.xlabel("Cache size")
plt.ylabel("Hit rate (%)")
plt.title("Cache Size vs Hit Rate")
plt.tight_layout()
plt.savefig("memory.svg")

print("Wrote memory.svg")
