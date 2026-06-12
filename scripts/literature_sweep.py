import csv
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from typing import Iterable

import requests


OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
os.makedirs(OUT_DIR, exist_ok=True)

QUERIES = [
    "tactile contact detection robot manipulation",
    "unexpected contact robot tactile sensing",
    "tactile residual robot model error contact",
    "contact-rich manipulation tactile force sensing",
    "robot tactile world model contact prediction",
    "slip detection tactile manipulation robot",
    "in-hand manipulation tactile sensing contact",
    "force torque tactile residual estimation robot",
    "proprioception tactile contact anomaly robot",
    "tactile prediction error robot control",
    "contact event detection tactile robot",
    "haptic residuals contact detection manipulation",
    "tactile state estimation robot contact dynamics",
]

UA = "Mozilla/5.0 (compatible; codex-paper-batch/1.0; +https://openai.com)"


@dataclass
class Paper:
    title: str
    year: str
    venue: str
    doi: str
    url: str
    source: str
    query: str
    score: float


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def safe_get(url: str, params=None, headers=None, timeout=30):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    r = requests.get(url, params=params, headers=h, timeout=timeout)
    r.raise_for_status()
    return r


def crossref_search(query: str, rows: int = 100, offset: int = 0):
    params = {
        "query.bibliographic": query,
        "rows": rows,
        "offset": offset,
        "mailto": "codex@example.com",
        "select": "title,DOI,URL,container-title,issued,author,type",
    }
    try:
        data = safe_get("https://api.crossref.org/works", params=params).json()
        return data.get("message", {}).get("items", [])
    except Exception as e:
        return []


def arxiv_search(query: str, start: int = 0, max_results: int = 100):
    # arXiv API uses Atom; keep this as a fallback only.
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": query, "start": start, "max_results": max_results}
    try:
        txt = safe_get(url, params=params, timeout=30).text
    except Exception:
        return []
    items = []
    for m in re.finditer(r"<entry>(.*?)</entry>", txt, flags=re.S):
        chunk = m.group(1)
        title = re.search(r"<title>(.*?)</title>", chunk, re.S)
        year = re.search(r"<published>(\d{4})-", chunk)
        link = re.search(r'<link title="pdf" href="(.*?)"', chunk)
        items.append({
            "title": re.sub(r"\s+", " ", title.group(1)).strip() if title else "",
            "year": year.group(1) if year else "",
            "doi": "",
            "url": link.group(1) if link else "",
            "venue": "arXiv",
        })
    return items


def extract_year(issued):
    try:
        return str(issued["date-parts"][0][0])
    except Exception:
        return ""


def title_score(title: str, query: str) -> float:
    t = set(re.findall(r"[a-z0-9]+", norm(title)))
    q = set(re.findall(r"[a-z0-9]+", norm(query)))
    if not t or not q:
        return 0.0
    return len(t & q) / len(q)


def gather():
    seen = set()
    out = []
    for q in QUERIES:
        for offset in range(0, 300, 100):
            items = crossref_search(q, 100, offset)
            if not items:
                break
            for it in items:
                title = (it.get("title") or [""])[0]
                key = norm(title)
                if not title or key in seen:
                    continue
                seen.add(key)
                venue = (it.get("container-title") or [""])[0]
                out.append(Paper(
                    title=title,
                    year=extract_year(it.get("issued", {})),
                    venue=venue,
                    doi=it.get("DOI", ""),
                    url=it.get("URL", ""),
                    source="crossref",
                    query=q,
                    score=title_score(title, q),
                ))
            time.sleep(0.25)
        if len(out) < 800:
            for item in arxiv_search(q):
                key = norm(item["title"])
                if not item["title"] or key in seen:
                    continue
                seen.add(key)
                out.append(Paper(
                    title=item["title"],
                    year=item["year"],
                    venue=item["venue"],
                    doi=item["doi"],
                    url=item["url"],
                    source="arxiv",
                    query=q,
                    score=title_score(item["title"], q),
                ))
    out.sort(key=lambda p: (-p.score, p.year or "", p.title))
    return out


def write_csv(papers):
    path = os.path.join(OUT_DIR, "related_work_matrix.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["title", "year", "venue", "doi", "url", "source", "query", "score"])
        for p in papers:
            w.writerow([p.title, p.year, p.venue, p.doi, p.url, p.source, p.query, f"{p.score:.3f}"])
    return path


def main():
    papers = gather()
    path = write_csv(papers)
    print(json.dumps({"count": len(papers), "path": path}, indent=2))
    return 0 if papers else 1


if __name__ == "__main__":
    raise SystemExit(main())
