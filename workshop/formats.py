"""The same records in different file 'clothes' — compare size and prove round-trip."""
import io

import pandas as pd


def sizes(df: pd.DataFrame) -> dict[str, int]:
    """Bytes each format takes to store the same data."""
    csv = df.to_csv(index=False).encode()
    js = df.to_json(orient="records").encode()
    xb = io.BytesIO(); df.to_excel(xb, index=False, engine="openpyxl")
    pb = io.BytesIO(); df.to_parquet(pb, index=False)
    return {"CSV": len(csv), "JSON": len(js),
            "Excel": len(xb.getvalue()), "Parquet": len(pb.getvalue())}


def roundtrip_rows(df: pd.DataFrame) -> dict[str, int]:
    """Write then read each format; return rows recovered (must equal the input)."""
    out = {}
    out["CSV"] = len(pd.read_csv(io.StringIO(df.to_csv(index=False))))
    out["JSON"] = len(pd.read_json(io.StringIO(df.to_json(orient="records"))))
    pb = io.BytesIO(); df.to_parquet(pb, index=False); pb.seek(0)
    out["Parquet"] = len(pd.read_parquet(pb))
    return out


def parse_table(html: str) -> pd.DataFrame:
    """Extract a structured table out of a document (here HTML; PDFs use camelot/tabula)."""
    return pd.read_html(io.StringIO(html))[0]
