"""Generate compact, deterministic numerical context from a local CSV."""

import pandas as pd


def csv_context(df: pd.DataFrame) -> str:
    if df.empty:
        return "O ficheiro CSV está vazio."

    lines = [f"Linhas: {len(df)}. Colunas: {len(df.columns)}."]
    lines.append("Colunas: " + ", ".join(map(str, df.columns[:12])))

    for col in df.columns[:10]:
        s = df[col]
        missing = int(s.isna().sum())
        if pd.api.types.is_numeric_dtype(s):
            valid = s.dropna()
            if not valid.empty:
                lines.append(
                    f"{col}: média={valid.mean():.2f}; mínimo={valid.min():.2f}; "
                    f"máximo={valid.max():.2f}; ausentes={missing}."
                )
            else:
                lines.append(f"{col}: todos os valores em falta.")
        else:
            top = s.astype("string").value_counts().head(3)
            items = ", ".join(f"{str(k)[:30]} ({int(v)})" for k, v in top.items())
            lines.append(f"{col}: valores mais frequentes: {items}; ausentes={missing}.")

    lines.append("Primeiras 5 linhas (amostra, NÃO a totalidade dos dados):")
    lines.append(df.iloc[:5, :10].to_csv(index=False))
    lines.append("Não inferir causalidade a partir de estatísticas descritivas.")
    return "\n".join(lines)[:4000]
