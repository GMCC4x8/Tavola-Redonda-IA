"""Minimal Streamlit UI: question, Word/Excel attachments, seven-call debate."""
import streamlit as st

from attachments import build_evidence
from roundtable import MODEL, run_debate

st.set_page_config(page_title="Távola Redonda IA", page_icon="💬", layout="centered")
st.title("💬 Távola Redonda IA")
st.caption("Três perspetivas · duas rondas de debate · uma conclusão · IA local gratuita")

with st.form("debate"):
    question = st.text_area("Pergunta para debate", placeholder="Qual é a decisão que queres analisar?", height=130)
    uploaded = st.file_uploader(
        "Anexos (opcionais): Word e Excel",
        type=["docx", "xlsx"],
        accept_multiple_files=True,
        help="Word (.docx) e Excel (.xlsx). Todas as folhas Excel são lidas.",
    )
    submitted = st.form_submit_button("Iniciar debate", type="primary", use_container_width=True)

if submitted:
    if not question.strip():
        st.error("Escreve uma pergunta.")
    else:
        try:
            files = [(file.name, file.getvalue()) for file in uploaded]
            evidence = build_evidence(files)
            progress = st.progress(0, text="A preparar o debate…")
            stage = st.empty()
            results = st.container()

            def update(step, phase, agent, answer):
                progress.progress(step / 7, text=f"{step}/7 chamadas concluídas")
                stage.caption(f"Última resposta: {phase} — {agent}")
                if phase != "Síntese final":
                    with results:
                        with st.expander(f"{phase} — {agent}", expanded=False):
                            st.markdown(answer)

            with st.spinner(f"A executar o debate com {MODEL}…"):
                result = run_debate(question, evidence=evidence, on_progress=update)

            progress.empty()
            stage.empty()
            with results:
                st.subheader("Conclusão do moderador")
                st.markdown(result["final"])

        except Exception as exc:
            st.error(str(exc))
