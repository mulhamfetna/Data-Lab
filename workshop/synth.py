"""Tiny, honest tabular synthesizer: a Gaussian model over numeric columns.

Preserves means, spreads, and correlations (utility) without copying individuals
(privacy). This is the *principle* real tools (SDV, GANs, diffusion) scale up — the
demo says so explicitly. NOT a GAN.
"""
import numpy as np
import pandas as pd


def _numeric(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def generate(real: pd.DataFrame, n: int, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    cols = _numeric(real)
    X = real[cols].to_numpy(dtype=float)
    mean = X.mean(axis=0)
    cov = np.cov(X, rowvar=False)
    sample = rng.multivariate_normal(mean, cov, size=n)
    return pd.DataFrame(sample, columns=cols)


def utility_report(real: pd.DataFrame, synth: pd.DataFrame) -> dict:
    cols = _numeric(real)
    rep: dict = {}
    for c in cols:
        rep[c] = {
            "real_mean": float(real[c].mean()), "synth_mean": float(synth[c].mean()),
            "real_std": float(real[c].std()), "synth_std": float(synth[c].std()),
        }
    r_corr = real[cols].corr().to_numpy()
    s_corr = synth[cols].corr().to_numpy()
    rep["corr_abs_diff"] = float(np.nanmean(np.abs(r_corr - s_corr)))
    return rep


def privacy_report(real: pd.DataFrame, synth: pd.DataFrame) -> dict:
    cols = _numeric(real)
    R = real[cols].to_numpy(dtype=float)
    S = synth[cols].to_numpy(dtype=float)
    # standardize so no single column dominates the distance
    mu, sd = R.mean(axis=0), R.std(axis=0) + 1e-9
    Rn, Sn = (R - mu) / sd, (S - mu) / sd
    dists = []
    for s in Sn:
        dists.append(float(np.sqrt(((Rn - s) ** 2).sum(axis=1)).min()))
    dists = np.array(dists)
    return {
        "min_distance": float(dists.min()),
        "mean_distance": float(dists.mean()),
        "exact_match_frac": float((dists < 1e-9).mean()),
    }
