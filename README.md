# Távola Redonda IA

Uma aplicação **gratuita e local** que utiliza inteligência artificial para analisar questões e debater diferentes perspetivas. Desenvolvida com **Python, Streamlit, Ollama e Qwen3 1.7B**.

## Como funciona

1. O utilizador escreve uma pergunta e, se quiser, anexa ficheiros **Word (.docx)** ou **Excel (.xlsx)**.
2. Três agentes analisam o problema: **Strategy AI** (negócio), **Technology AI** (viabilidade) e **Ethical AI** (ética).
3. Os agentes apresentam as suas opiniões e, numa segunda ronda, respondem aos argumentos uns dos outros.
4. Um moderador reúne os principais pontos e apresenta uma conclusão.

O debate tem **7 chamadas ao modelo**: 3 análises iniciais, 3 respostas na segunda ronda e 1 síntese final.

## Instalação

É necessário ter **Python** e [Ollama](https://ollama.com/download) instalados.

Descarrega o modelo gratuito:

```powershell
ollama pull qwen3:1.7b
```

Na pasta do projeto, executa:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

A aplicação abre no browser. O modelo corre no teu computador, sem necessidade de API paga.

## Exemplo de utilização

Anexa um relatório empresarial e pergunta:

> Qual é a melhor estratégia para aumentar as vendas sem comprometer a qualidade? Analisa os dados fornecidos e identifica os principais riscos.

## Notas

- Os ficheiros Excel podem conter várias folhas.
- Documentos grandes estão sujeitos a limites de tamanho e contexto do modelo.
- As respostas da IA podem conter erros; confirma os dados e os cálculos antes de tomar decisões.

## Tecnologias

**Python · Streamlit · Ollama · Qwen3 1.7B**
