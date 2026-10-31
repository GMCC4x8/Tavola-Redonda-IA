"""Lightweight, deterministic evidence helpers. No AI/API calls.

These checks do NOT infer financial models from prose or Excel formulas.
They can only validate arithmetic expressions written explicitly as
"number = arithmetic expression" and select original evidence lines.
"""
from __future__ import annotations

import ast
from decimal import Decimal, InvalidOperation
import operator
import re
import unicodedata

_NUMBER = r"\d+(?:\.\d{3})*(?:,\d+)?"
_ALLOWED_EXPR = re.compile(r"^[\d\s,.€()+*/×xX−–-]+$")
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_STOPWORDS = {"para", "como", "com", "uma", "que", "qual", "das", "dos", "por", "sobre", "nos", "nas", "seus", "sua", "se", "ser", "este", "esta", "mais", "menos", "tres", "todas", "todos", "anexa", "anexado", "documento"}


def _normalize_num(match: re.Match[str]) -> str:
    """Convert European 1.200 and 1.200,50 into Python-friendly numerals."""
    return match.group(0).replace(".", "").replace(",", ".")


def _safe_math(expression: str) -> Decimal:
    clean = expression.replace("€", "").replace("×", "*").replace("x", "*").replace("X", "*")
    clean = clean.replace("−", "-").replace("–", "-").strip()
    if not _ALLOWED_EXPR.fullmatch(expression):
        raise ValueError("Operador inválido")
    clean = re.sub(_NUMBER, _normalize_num, clean)
    node = ast.parse(clean, mode="eval")

    def calculate(n: ast.AST, depth: int = 0) -> Decimal:
        if depth > 12:
            raise ValueError("Expressão demasiado complexa")
        if isinstance(n, ast.Expression):
            return calculate(n.body, depth + 1)
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            return Decimal(str(n.value))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            value = calculate(n.operand, depth + 1)
            return -value if isinstance(n.op, ast.USub) else value
        if isinstance(n, ast.BinOp) and type(n.op) in _OPERATORS:
            left, right = calculate(n.left, depth + 1), calculate(n.right, depth + 1)
            if isinstance(n.op, ast.Div) and right == 0:
                raise ValueError("Divisão por zero")
            return _OPERATORS[type(n.op)](left, right)
        raise ValueError("Expressão inválida")

    result = calculate(node)
    if not result.is_finite() or abs(result) > 10**15:
        raise ValueError("Resultado fora de limites")
    return result


def verify_explicit_equations(evidence: str, max_checks: int = 5) -> str:
    """Check only explicit arithmetic with a stated expected number.

    For example: '178.000 € = 1.200 × (850 € − 310 €) − 470.000 €'.
    Does not evaluate Excel cell formulas or model unstructured business data.
    """
    verified = []
    for line in evidence.splitlines():
        if "=" not in line or len(line) > 400:
            continue
        lhs, rhs = line.rsplit("=", 1)
        value_match = re.search(rf"(?<![\w])({_NUMBER})\s*€?\s*$", lhs)
        if value_match is None:
            continue
        try:
            expected = Decimal(value_match.group(1).replace(".", "").replace(",", "."))
            result = _safe_math(rhs)
        except (ValueError, SyntaxError, InvalidOperation, OverflowError, ZeroDivisionError):
            continue
        status = "CONFERE" if abs(expected - result) <= Decimal("0.01") else "NÃO CONFERE"
        verified.append(f"[{status}] Valor indicado: {expected}; cálculo: {result}; expressão: {rhs.strip()}")
        if len(verified) >= max_checks:
            break
    if not verified:
        return ""
    return ("CONTAS EXPLÍCITAS VERIFICADAS PELO PYTHON (não substitui análise financeira):\n"
            + "\n".join(verified))


def _normalize_words(value: str) -> set[str]:
    value = unicodedata.normalize("NFKD", value.lower())
    value = "".join(c for c in value if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z]{4,}", value) if w not in _STOPWORDS}


def select_relevant_evidence(evidence: str, question: str, max_chars: int = 2500) -> str:
    """Choose unmodified evidence lines for the moderator's limited context.

    The first six calls receive the full extracted content. Moderator gets
    relevant source excerpts as a cross-check, not a claim of full re-reading.
    """
    if not evidence.strip():
        return ""
    if len(evidence) <= max_chars:
        return evidence.strip()
    keywords = _normalize_words(question)
    rows = [(idx, line.strip()) for idx, line in enumerate(evidence.splitlines()) if line.strip()]
    ranking = []
    for idx, line in rows:
        words = _normalize_words(line)
        score = 3 * len(words & keywords)
        score += 2 if any(c.isdigit() for c in line) else 0
        score += 2 if "€" in line else 0
        score += 2 if any(s in line.lower() for s in ("opção", "opcao", "option", "resultado", "lucro", "investimento", "preço", "custos")) else 0
        score += 9 if re.match(r"^(opção|opcao|option)\s+[a-z]", line, re.IGNORECASE) else 0
        ranking.append((score, idx, line))
    # Avoid cutting lines halfway: only include whole lines that fit.
    ranking.sort(key=lambda x: (-x[0], x[1]))
    selected = []
    used = 0
    for _score, idx, line in ranking:
        if used + len(line) + 1 <= max_chars:
            selected.append((idx, line))
            used += len(line) + 1
    selected.sort()
    output = "\n".join(line for _idx, line in selected)
    if len(selected) < len(rows):
        output = "EXCERTOS RELEVANTES DOS ANEXOS (não incluem todas as linhas):\n" + output
    return output
