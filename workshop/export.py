"""Bundle the artifacts a participant generated into one downloadable zip."""
import io
import zipfile

from workshop import report, store_data as sd


def bundle() -> bytes:
    df = sd.clean_orders(sd.messy_orders())
    k = report.kpis(df)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("nour_store_report.txt", report.summary_text(k))
        z.writestr("nour_store_clean.csv", df.to_csv(index=False))
        z.writestr("README.txt",
                   "Data Lab session export\n"
                   "- nour_store_report.txt : the performance report\n"
                   "- nour_store_clean.csv  : the cleaned dataset\n")
    return buf.getvalue()
