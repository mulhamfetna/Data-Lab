"""Serialization & compression: same data, far smaller and faster in the right format."""
import gzip
import io
import time

import pandas as pd


def sizes(df: pd.DataFrame) -> dict[str, int]:
    csv = df.to_csv(index=False).encode()
    csv_gz = gzip.compress(csv)
    pb = io.BytesIO()
    df.to_parquet(pb, index=False)
    return {"CSV": len(csv), "CSV.gz": len(csv_gz), "Parquet": len(pb.getvalue())}


def read_speed_ms(df: pd.DataFrame) -> dict[str, float]:
    csv = df.to_csv(index=False).encode()
    t0 = time.time(); pd.read_csv(io.BytesIO(csv)); t_csv = (time.time() - t0) * 1000
    pb = io.BytesIO(); df.to_parquet(pb, index=False); parq = pb.getvalue()
    t0 = time.time(); pd.read_parquet(io.BytesIO(parq)); t_parq = (time.time() - t0) * 1000
    return {"CSV": round(t_csv, 1), "Parquet": round(t_parq, 1)}
