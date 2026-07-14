import re

_FENCE_RE = re.compile(r"^```(?:json)?\s*\n?(.*?)\n?```$", re.DOTALL)


def strip_json_fence(raw: str) -> str:
    """Strips a surrounding ```json ... ``` (or ``` ... ```) code fence.

    Real AIProvider implementations (e.g. AnthropicProvider) often wrap a
    JSON reply in a markdown code fence even when told not to; MockAIProvider
    and a schema-constrained response never need this.
    """
    stripped = raw.strip()
    match = _FENCE_RE.match(stripped)
    return match.group(1).strip() if match else stripped
