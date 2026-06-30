import csv
import subprocess
import time
def run_and_time(cmd):
    start = time.perf_counter()

    subprocess.run(
        cmd,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return time.perf_counter() - start
PARQUET_CMD = [
    "docker", "exec", "p3-client-1",
    "python3.13-nogil",
    "client.py",
    "/data/2021_public_lar.parquet",
    "--rows", "0",
    "--cache", "2000",
    "--threads", "8",
]

CSV_CMD = [
    "docker", "exec", "p3-client-1",
    "python3.13-nogil",
    "client.py",
    "/data/2021_public_lar_csv.zip",
    "--rows", "0",
    "--cache", "2000",
    "--threads", "8",
]

results = [
    ("parquet", run_and_time(PARQUET_CMD)),
    ("csv_zip", run_and_time(CSV_CMD)),
]

with open("storage.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["format", "seconds"])
    writer.writerows(results)

print("Wrote storage.csv")
