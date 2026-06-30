import csv
import matplotlib.pyplot as plt

formats = []
seconds = []

with open("storage.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        formats.append(row["format"])
        seconds.append(float(row["seconds"]))

plt.figure()
plt.bar(formats, seconds)
plt.xlabel("Storage format")
plt.ylabel("Seconds")
plt.title("Storage Format Load Time")
plt.tight_layout()
plt.savefig("storage.svg")
print("Wrote storage.svg")
