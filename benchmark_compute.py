import csv
import subprocess
import time

ROWS = 10000      # 最后改成1000000
CACHE = 50000

THREADS = [1, 2, 4, 8]
GILS = [1, 0]

with open("compute.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["gil", "threads", "seconds"])

    for gil in GILS:
        for threads in THREADS:
            print(f"gil={gil}, threads={threads}")

            cmd = [
                "docker",
                "exec",
                "p3-client-1",
                "python3.13-nogil",
                "-X",
                f"gil={gil}",
                "client.py",
                "/data/2021_public_lar.parquet",
                "--rows",
                str(ROWS),
                "--cache",
                str(CACHE),
                "--threads",
                str(threads),
            ]

            start = time.perf_counter()

            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            elapsed = time.perf_counter() - start

            writer.writerow([gil, threads, elapsed])
            f.flush()

print("Wrote compute.csv")
