# Távola Redonda IA — V12 (Grounded Debate)

Projeto local e gratuito para debater decisões empresariais com **Qwen3 1.7B + Ollama + Streamlit**.

## Fluxo (exatamente 7 chamadas)

1. Strategy AI, Technology AI e Ethical AI apresentam opiniões iniciais (3 chamadas).
2. Cada agente lê os argumentos dos outros e responde com base nos documentos (3 chamadas).
3. O moderador recebe o debate e **excertos originais relevantes dos anexos** (1 chamada).

## O que mudou em relação à V11

- Prompts mais curtos e orientados para **factos, hipóteses e incertezas**.
- Os agentes têm de fundamentar os argumentos e corrigir afirmações sem suporte na segunda ronda.
- O moderador recebe excertos selecionados do texto original, não apenas as respostas dos agentes.
- `evidence_checks.py` valida aritmeticamente **equações explícitas**, como `178.000 € = 1.200 × (850 € − 310 €) − 470.000 €`, através de Python, sem LLM extra.
- Mantém `.docx`, `.xlsx` (todas as folhas), Qwen3 1.7B e sete chamadas. Sem APIs pagas.

**Limites:** o Python não constrói modelos financeiros automaticamente a partir de prosa livre, não recalcula fórmulas do Excel e não verifica todos os factos. Os excertos fornecidos ao moderador podem omitir detalhes de documentos grandes; os três agentes recebem o conteúdo integral que cabe no limite de upload já definido. Mesmo com estas alterações, o LLM pode continuar a cometer erros. Para análises críticas, valida os cálculos e as recomendações.

## Instalação (Windows / VS Code)

Instala o [Ollama](https://ollama.com/download) e executa uma vez:

```powershell
ollama pull qwen3:1.7b
```

Na pasta do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Para quem já tem a V11 instalada, basta substituir `roundtable.py` e adicionar `evidence_checks.py`, sem reinstalar bibliotecas. Os restantes ficheiros permanecem iguais.

## Testes

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

O teste automático substitui o modelo por respostas simuladas; **não** mede a qualidade das respostas geradas no teu computador.

## Próximo teste recomendado

Carrega `Caso_Atelier_Norte_AI_Roundtable.docx` (o ficheiro de caso que já tens) e pergunta:

> Compara A, B e C usando os valores financeiros do documento. Explica quais dependem de vendas ainda não confirmadas e se a opção B é recomendável já ou apenas de forma faseada. Não inventes reduções na taxa de defeitos.

Compara a V11 e a V12 com a **mesma pergunta e o mesmo documento**. Observa se há mais valores reais, menos afirmações inventadas e uma comparação mais equilibrada das alternativas.

## Git

Recomenda-se experimentar numa branch própria antes de fazer merge na `main`.

```powershell
git switch -c feature/grounded-debate
git add -A
git commit -m "Improve evidence-based agent debate"
git push -u origin feature/grounded-debate
```
