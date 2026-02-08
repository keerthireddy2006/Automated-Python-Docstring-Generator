import requests
import re
import textwrap

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:3b"


def build_prompt(code: str, style: str) -> str:
    """
    Build a strong, clear prompt optimized for qwen2.5-coder:3b
    """
    style = style.lower()
    if style in ["rst", "restructuredtext"]:
        style = "reST"

    return f"""You are an expert Python docstring generator.

Generate EXACTLY ONE PEP 257 compliant docstring for the given function/method.

MANDATORY RULES - YOU MUST FOLLOW ALL:
- Output ONLY the docstring content (text that goes between triple quotes)
- Start with one short imperative summary sentence. End with a period.
- Then exactly one blank line.
- Then only needed sections: Args/Parameters, Returns, Raises, Yields
- Follow the selected style strictly: {style}
- Use exactly 4 spaces for indentation under sections
- Do NOT include ```python
- Do NOT repeat the function definition
- Do NOT add extra triple quotes around your output
- Do NOT add examples, notes, explanations, or any extra text
- Do NOT include the words "python" or "code" unless in type hints
- Return ONLY the pure docstring text — nothing before or after

Style reference:
- google: Args:, Returns:, Raises:
- numpy: Parameters\n----------, Returns\n-------, Raises\n------
- reST: :param name:, :returns:, :raises:

STRICT OUTPUT RULES - YOU MUST OBEY:
- Output ONLY the docstring content (the text INSIDE the triple quotes)
- Start directly with the summary sentence
- Then one blank line
- Then only needed sections
- Do NOT output triple quotes at all
- Do NOT repeat the function definition
- Do NOT include ```python or any fences
- Do NOT add extra text, examples, explanations or markup
- Return pure text only



Code:
{code}

Style: {style}

Respond with ONLY the docstring content. No other text.
"""


def clean_docstring(raw: str) -> str:
    """
    Clean LLM output and ensure it becomes a valid docstring.
    """
    raw = raw.strip()

    # Remove common LLM mistakes
    raw = re.sub(r"^```(?:python|py)?\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\s*```$", "", raw)
    raw = re.sub(r'^("""|\'\'\')+', "", raw)
    raw = re.sub(r'("""|\'\'\')+$', "", raw)

    # Split into lines and clean
    lines = [line.rstrip() for line in raw.splitlines()]

    # Remove leading/trailing empty lines
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return '"""\nNo description available.\n"""'

    # Force PEP 257 structure: summary + blank line
    summary = lines[0].strip()
    body = lines[1:]

    result = [summary, ""]  # summary + blank line

    for line in body:
        stripped = line.rstrip()
        if stripped:
            # Keep section headers clean, indent descriptions
            if re.match(r"^(Args|Parameters|Returns|Raises|Yields):", stripped.strip()):
                result.append(stripped)
            else:
                result.append("    " + stripped.lstrip())
        else:
            result.append("    ")

    # Add triple quotes
    result = ['"""'] + result + ['"""']

    return "\n".join(result)


def generate_docstring_llm(code: str, style: str = "Google") -> str:
    """
    Generate a PEP 257 compliant docstring using Ollama + qwen2.5-coder:3b

    Args:
        code: Function/method code as string
        style: "Google", "NumPy", "reST"

    Returns:
        Properly formatted docstring string (with triple quotes)
    """
    prompt = build_prompt(code, style)

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "num_predict": 512,  # enough for most docstrings
        },
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()

        raw = response.json().get("response", "").strip()

        if not raw:
            return '"""\nGenerated docstring.\n"""'

        cleaned = clean_docstring(raw)

        # Final safety: ensure triple quotes
        if not cleaned.startswith('"""'):
            cleaned = '"""\n' + cleaned.lstrip()
        if not cleaned.endswith('"""'):
            cleaned = cleaned.rstrip() + '\n"""'

        return cleaned

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ollama connection failed: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Docstring generation failed: {e}") from e


# ────────────────────────────────────────────────
# Optional test
# ────────────────────────────────────────────────
if __name__ == "__main__":
    sample = """
def add(a: int, b: int = 0) -> int:
    return a + b
"""

    try:
        doc = generate_docstring_llm(sample, style="Google")
        print("Generated docstring:\n")
        print(doc)
    except Exception as e:
        print(f"Error: {e}")
