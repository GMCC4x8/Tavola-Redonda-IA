"""Free, local Streamlit interface for the AI Roundtable."""

import json

import pandas as pd
import streamlit as st

from data_utils import csv_context
from roundtable import DEFAULT_MODEL, run_roundtable, to_markdown

st.set_page_config(page_title="AI Roundtable", page_icon="🧠", layout="wide")

st.title("🧠 AI Roundtable")
st.caption("Três perspectivas. Duas rondas. Uma síntese. IA local, sem APIs pagas.")

with st.sidebar:
    st.header("⚙️ Configuração")
    model = st.selectbox(
        "Modelo local (Ollama)",
        options=[DEFAULT_MODEL, "qwen2.5:1.5b-instruct"],
        help="O modelo selecionado tem de estar instalado com 'ollama pull'.",
    )
    st.info("Todas as chamadas à IA são feitas no teu computador via Ollama.")
    st.caption("Sete chamadas sequenciais: 3 opiniões + 3 críticas + 1 síntese.")

question = st.text_area(
    "Que problema queres discutir?",
    value="Como pode uma pequena consultora melhorar a margem operacional sem comprometer a qualidade?",
    height=110,
)

uploaded = st.file_uploader(
    "Opcional: carregar um CSV para fundamentar a discussão", type=["csv"]
)
context = ""
valid_csv = True

if uploaded is not None:
    if uploaded.size > 2_000_000:
        st.error("O CSV deve ter menos de 2 MB nesta primeira versão.")
        valid_csv = False
    else:
        try:
            df = pd.read_csv(uploaded)
            context = csv_context(df)
            c1, c2 = st.columns(2)
            c1.metric("Registos do CSV", f"{len(df):,}")
            c2.metric("Variáveis", len(df.columns))
            with st.expander("Pré-visualização e resumo dos dados"):
                st.dataframe(df.head(10), use_container_width=True)
                st.code(context, language="text")
            st.caption("A IA recebe um resumo estatístico e 5 linhas de exemplo, não o CSV completo.")
        except Exception as exc:
            st.error(f"Não foi possível ler o CSV: {exc}")
            valid_csv = False

if st.button("▶ Iniciar a mesa-redonda", type="primary", disabled=not question.strip() or not valid_csv):
    st.session_state.pop("roundtable_result", None)
    with st.status("A consultar o modelo local...", expanded=True) as status:
        progress_bar = st.progress(0)

        def on_progress(done, total, phase, agent):
            progress_bar.progress(done / total)
            status.write(f"{done}/{total} — {phase}: {agent} concluído")

        try:
            result = run_roundtable(
                question=question,
                data_context=context,
                model=model,
                progress=on_progress,
            )
            st.session_state["roundtable_result"] = result
            status.update(label="Mesa-redonda concluída", state="complete")
        except Exception as exc:
            status.update(label="Não foi possível concluir", state="error")
            st.error(
                "Verifica se o Ollama está aberto e se instalaste o modelo "
                f"'{model}' com 'ollama pull {model}'.\n\nDetalhe: {exc}"
            )

result = st.session_state.get("roundtable_result")
if result:
    st.divider()
    st.subheader("Resultados")
    t1, t2, t3, t4 = st.tabs(["Ronda 1", "Ronda 2", "Síntese", "Métricas"])

    with t1:
        for event in result["events"]:
            if event["phase"] == "Ronda 1":
                with st.expander(event["agent"], expanded=True):
                    st.markdown(event["text"])

    with t2:
        for event in result["events"]:
            if event["phase"] == "Ronda 2":
                with st.expander(event["agent"], expanded=True):
                    st.markdown(event["text"])

    with t3:
        st.markdown(result["final"])
        st.warning("Concordância entre agentes não comprova a exatidão das conclusões.")

    with t4:
        events = pd.DataFrame(result["events"])
        a, b, c = st.columns(3)
        a.metric("Chamadas ao modelo", len(events))
        b.metric("Duração total", f"{result['total_seconds']:.1f} s")
        c.metric("Tokens gerados", int(events["generated_tokens"].sum()))
        st.bar_chart(events.set_index("agent")["seconds"])
        st.dataframe(
            events[["phase", "agent", "seconds", "prompt_tokens", "generated_tokens"]],
            use_container_width=True,
        )
        st.caption("Os tokens são uma métrica de utilização, não de qualidade.")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇ Descarregar relatório Markdown",
            data=to_markdown(result),
            file_name="roundtable_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col2:
        st.download_button(
            "⬇ Descarregar resultados JSON",
            data=json.dumps(result, ensure_ascii=False, indent=2),
            file_name="roundtable_result.json",
            mime="application/json",
            use_container_width=True,
        )
