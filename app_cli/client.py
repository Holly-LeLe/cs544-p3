import argparse
import threading
import zipfile
import requests

import pyarrow as pa
import pyarrow.csv as pv
import pyarrow.parquet as pq

import cache


def read_table(path):
    columns = ["state_code", "census_tract", "income"]

    if path.endswith(".parquet"):
        return pq.read_table(path, columns=columns)

    convert_options = pv.ConvertOptions(
        include_columns=columns,
        column_types={
            "state_code": pa.string(),
            "census_tract": pa.string(),
            "income": pa.float64(),
        },
    )

    if path.endswith(".zip"):
        with zipfile.ZipFile(path) as zf:
            name = zf.namelist()[0]
            with zf.open(name) as f:
                return pv.read_csv(f, convert_options=convert_options)

    return pv.read_csv(path, convert_options=convert_options)
def worker(table, start, stop, results, idx):
    session = requests.Session()

    states = table.column("state_code")
    tracts = table.column("census_tract")
    incomes = table.column("income")

    under = {}
    total = {}
    hits = 0
    lookups = 0

    for i in range(start, stop):
        try:
            state = states[i].as_py()
            tract = tracts[i].as_py()
            income = incomes[i].as_py()

            if state is None or tract is None or income is None:
                continue

            tract = str(tract).strip()
            if tract == "" or len(tract) != 11 or not tract.isdigit():
                continue

            income = float(income)
            if income <= 0:
                continue

            url = f"http://server:8001/{tract}"
            content, hit = cache.http_get(url, session)

            lookups += 1
            if hit:
                hits += 1

            if content is None:
                continue

            median = float(content)

            total[state] = total.get(state, 0) + 1

            if income < median:
                under[state] = under.get(state, 0) + 1

        except Exception:
            continue

    results[idx] = (under, total, hits, lookups)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--rows", type=int, default=-1)
    parser.add_argument("--cache", type=int, default=2000)
    parser.add_argument("--threads", type=int, default=8)
    args = parser.parse_args()

    table = read_table(args.path)

    if args.rows != -1:
        table = table.slice(0, args.rows)

    cache.init_cache(args.cache)

    n = table.num_rows
    results = [None] * args.threads
    threads = []

    for t in range(args.threads):
        start = t * n // args.threads
        stop = (t + 1) * n // args.threads

        th = threading.Thread(
            target=worker,
            args=(table, start, stop, results, t),
        )
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    final_under = {}
    final_total = {}
    final_hits = 0
    final_lookups = 0

    for result in results:
        if result is None:
            continue

        under, total, hits, lookups = result
        final_hits += hits
        final_lookups += lookups

        for state, count in total.items():
            final_total[state] = final_total.get(state, 0) + count

        for state, count in under.items():
            final_under[state] = final_under.get(state, 0) + count

    for state in sorted(final_total):
        total = final_total[state]
        under = final_under.get(state, 0)
        percent = int(under / total * 100)
        print(f"{state}: {percent}% of {total}")

    if final_lookups == 0:
        hit_rate = 0
    else:
        hit_rate = int(final_hits / final_lookups * 100)

    print(f"hit rate: {hit_rate}%")


if __name__ == "__main__":
    main()
