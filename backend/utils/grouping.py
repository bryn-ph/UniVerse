# utils/grouping.py
import re

STOPWORDS = {
    "introduction","intro","advanced","fundamentals","to","and","of","for","the",
    "ii","i","iii","iv","unit","course","study"
}
UNI_NOISE = {"rmit","monash","unsw","unimelb","uq","usyd","anu","uts","uwa"}

TOKEN_RE = re.compile(r"[a-z0-9]+")

def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall((text or "").lower())

def normalize_tokens(name: str, tags: list[str]) -> list[str]:
    name_tokens = [t for t in _tokenize(name) if t not in STOPWORDS and t not in UNI_NOISE]
    tag_tokens = []
    for tag in tags or []:
        tag_tokens += [t for t in _tokenize(tag) if t not in STOPWORDS]
    return sorted(set(name_tokens + tag_tokens))

def make_signature(name: str, tags: list[str]) -> str:
    toks = normalize_tokens(name, tags)
    return "-".join(toks[:6]) or "general"

def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)
