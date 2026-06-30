import csv
import subprocess
import re

ROWS = 1000000
CACHE_SIZES = range(10000, 100001, 10000)

with open("memory.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["cache_size", "hit_rate"])

    for cache_size in CACHE_SIZES:
        print(f"running cache={cache_size}")

        cmd = [
            "docker", "exec", "p3-client-1",
            "python3.13-nogil",
            "client.py",
            "/data/2021_public_lar.parquet",
            "--rows", str(ROWS),
            "--cache", str(cache_size),
            "--threads", "4",
        ]

        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )

        match = re.search(r"hit rate: (\d+)%", result.stdout)
        hit_rate = int(match.group(1))

        writer.writerow([cache_size, hit_rate])
        f.flush()

print("Wrote memory.csv")
