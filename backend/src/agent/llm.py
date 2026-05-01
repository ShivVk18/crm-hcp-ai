import os
from groq import Groq

# Client is created lazily so it only fails at call-time, not at import.
_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client


def call_llm(
    prompt: str,
    model: str = "llama-3.1-8b-instant",
    as_json: bool = False,
) -> str:
    """
    Call the Groq LLM.

    Args:
        prompt:   The user message / instruction.
        model:    Groq model ID.
                  Defaults to llama-3.1-8b-instant — the official Groq replacement
                  for the decommissioned gemma2-9b-it (same speed/price profile).
                  Pass "llama-3.3-70b-versatile" for richer context/summarization tasks.
        as_json:  If True, request a JSON-mode response (supported by llama models).

    Returns:
        The model's text response.
    """
    client = _get_client()

    kwargs = dict(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    # JSON mode is only reliably supported by llama models on Groq
    if as_json and "llama" in model:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content