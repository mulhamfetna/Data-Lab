"""An automated data-quality health check on any table."""
import pandas as pd


def profile(df: pd.DataFrame) -> dict:
    rows = []
    for c in df.columns:
        s = df[c]
        row = {"column": c, "dtype": str(s.dtype),
               "missing_%": round(100 * s.isna().mean(), 1),
               "unique": int(s.nunique(dropna=True))}
        if pd.api.types.is_numeric_dtype(s) and s.notna().any():
            row["min"] = round(float(s.min()), 2)
            row["max"] = round(float(s.max()), 2)
        rows.append(row)
    table = pd.DataFrame(rows)
    warnings = []
    for _, r in table.iterrows():
        if r["missing_%"] > 0:
            warnings.append(f"⚠️ **{r['column']}** — {r['missing_%']}% missing")
        if r["unique"] <= 1:
            warnings.append(f"⚠️ **{r['column']}** — constant column (no information)")
    if df.duplicated().any():
        warnings.append(f"⚠️ {int(df.duplicated().sum())} duplicate rows")
    return {"table": table, "warnings": warnings, "rows": len(df), "cols": len(df.columns)}
