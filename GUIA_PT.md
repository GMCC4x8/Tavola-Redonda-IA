# Guia — AI Roundtable totalmente gratuita (Windows + VS Code)

## O que é isto?

Uma aplicação que executa **um modelo de IA no teu PC** via Ollama. O mesmo modelo faz os papéis de estratega, perito tecnológico, crítico e moderador. A app é feita em Python e Streamlit. Opcionalmente, uma tabela CSV é analisada com Pandas antes de ser fornecida à IA.

## 1. Instalar as ferramentas (uma única vez)

1. **Python**: descarrega Python 3.12 ou 3.13 em https://www.python.org/downloads/ . No Windows, se o instalador oferecer a opção, ativa "Add Python to PATH". Verifica no PowerShell: `py --version`.
2. **VS Code**: instala através de https://code.visualstudio.com/ . Adiciona a extensão **Python** da Microsoft.
3. **Ollama**: instala através de https://ollama.com/download . No Windows, a aplicação inicia normalmente o servidor local automaticamente. Fecha e volta a abrir o terminal depois da instalação.

## 2. Descarregar a IA (sem chave, sem conta, sem pagamentos)

Abre o terminal do VS Code: **Terminal > New Terminal**.

```powershell
ollama --version
ollama pull qwen3:4b-instruct
ollama list
```

O modelo `qwen3:4b-instruct` ocupa cerca de 2,5 GB em disco. Confirma que aparece em `ollama list`.

## 3. Abrir o projeto no VS Code

Descompacta o ZIP numa pasta, por exemplo `Documentos\ai-roundtable`. No VS Code: **File > Open Folder...** e escolhe essa pasta. O terminal deve estar na mesma pasta que `app.py`.

## 4. Criar o ambiente Python e instalar dependências

No terminal PowerShell do VS Code:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

O ambiente `.venv` isola os pacotes do projeto e é ignorado pelo Git. Utilizar o Python diretamente de `.venv` evita problemas de políticas de execução do PowerShell.

## 5. Executar a aplicação

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Abre o endereço apresentado no terminal (normalmente **http://localhost:8501**). Mantém o Ollama aberto e o terminal da aplicação em execução.

Se aparecer "connection refused", confirma que o Ollama está aberto no Windows. Se necessário, abre-o no menu Iniciar. Em casos em que não esteja a correr, pode-se iniciar com `ollama serve` num outro terminal, mas não o faças se já estiver a correr (a porta ficaria ocupada).

## 6. Experimentar o debate

Uma pergunta inicial sugerida:

> Como pode uma pequena consultora melhorar a margem operacional sem comprometer a qualidade?

Clica em **Iniciar a mesa-redonda**. A aplicação faz 7 chamadas ao modelo **sequencialmente**:

1. Strategy AI: primeira análise independente
2. Technology AI: primeira análise independente
3. Critical AI: primeira análise independente
4. Strategy AI: revê argumentos dos outros
5. Technology AI: revê argumentos dos outros
6. Critical AI: revê argumentos dos outros
7. Moderator AI: síntese final

A execução pode ser lenta se não tiveres GPU compatível. As duas rondas não garantem que a conclusão está correta.

## 7. Usar dados para um projeto mais interessante

Carrega o ficheiro **`dados/exemplo_vendas.csv`** na aplicação. É um dataset **fictício** com receitas, custos, gastos de marketing e número de clientes.

Pergunta, por exemplo:

> Com base nos dados do CSV, quais os sinais de deterioração das margens e que análises deveríamos fazer antes de decidir uma estratégia?

O Pandas calcula médias, mínimos, máximos, ausentes e algumas linhas de exemplo. A IA recebe esse **resumo dos dados**, não todos os registos. Não uses dados confidenciais no GitHub.

## 8. Ler e modificar o código

1. Abre **`app.py`**: é a interface, com o campo da pergunta, CSV, gráficos e botões.
2. Abre **`roundtable.py`**: a variável `AGENTS` define o papel de cada agente.
3. Em `ask_local()` vês como o Python chama `ollama.chat()`.
4. Em `run_roundtable()`, vê os dois ciclos `for`: são a ronda inicial e a discussão.
5. Em **`data_utils.py`**, vê como os dados do CSV são resumidos.

Um bom primeiro exercício é mudares o agente `Technology AI` para `Financial AI` e adaptares o texto do papel.

## 9. Executar testes (sem usar IA)

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes usam respostas falsas para verificar que existem sete chamadas e que é criado um relatório.

## 10. Publicar no GitHub

Cria um repositório **vazio** chamado `ai-roundtable` no GitHub (sem README nem .gitignore adicionais). No terminal, na pasta do projeto:

```powershell
git init
git add .
git commit -m "Initial free local AI Roundtable MVP"
git branch -M main
git remote add origin https://github.com/TEU_UTILIZADOR/ai-roundtable.git
git push -u origin main
```

Substitui `TEU_UTILIZADOR` pelo teu username. Instala o Git se ainda não o tiveres (https://git-scm.com/downloads). Poderás ter de autenticar-te no GitHub.

Antes do upload, confirma `git status` e certifica-te de que **`.venv/` e ficheiros privados** não estão a ser enviados.

## 11. Problemas comuns

- **`py` não existe:** instala Python ou testa `python --version` / `python -m venv .venv`.
- **`ollama` não é reconhecido:** reinicia o VS Code após instalar Ollama e confirma a instalação.
- **Modelo não encontrado:** usa `ollama pull qwen3:4b-instruct` e confirma `ollama list`.
- **Lento / falta de memória:** instala `ollama pull qwen2.5:1.5b-instruct`, seleciona esse modelo na barra lateral e volta a executar; a qualidade será inferior.
- **O endereço http://localhost:8501 não abre:** confirma que o comando do Streamlit continua ativo no terminal.
- **Queres parar a aplicação:** no terminal, carrega `Ctrl+C`.

## 12. Próximos desenvolvimentos para o portefólio

Implementa uma terceira ronda opcional, diferentes modelos, avaliação de respostas com casos de teste rotulados, gráficos comparativos e uma interface em inglês. Adiciona capturas de ecrã e um pequeno vídeo de demonstração ao README.
