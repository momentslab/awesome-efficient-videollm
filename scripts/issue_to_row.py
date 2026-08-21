#!/usr/bin/env python3
"""Turn an "Add a paper" issue-form submission into a README row.

Reads the issue body from $ISSUE_BODY. If the paper already exists, reports
its category without changing README; otherwise inserts a year-sorted row and
normalizes the file. The body is untrusted input, so every field is sanitized
and every link must be a plain https URL.

    ISSUE_BODY="$(gh issue view N --json body -q .body)" python3 scripts/issue_to_row.py
    python3 scripts/issue_to_row.py --self-test
"""
import os, re, sys, unicodedata
from urllib.parse import urlsplit

import normalize_readme as N

FIELDS = {"abbreviation": "abbrev", "paper title": "title", "paper link": "paper",
          "venue": "venue", "year": "year", "code link": "code",
          "weights link": "weights", "where does it belong?": "section"}
URL_OK = re.compile(r"https://[\w.-]+/[\w./#?=&%+~-]*$")


def parse(body):
    """Issue-form bodies are '### Label\\n\\nvalue' blocks."""
    out = {}
    for chunk in re.split(r"^### ", body.replace("\r\n", "\n"), flags=re.M)[1:]:
        label, _, value = chunk.partition("\n")
        key = FIELDS.get(label.strip().lower())
        value = value.strip()
        if key and value and value != "_No response_":
            out[key] = value
    return out


def clean(value, limit=300):
    """One line, no table-breaking pipes, no markdown links smuggled in."""
    value = re.sub(r"\s+", " ", value).replace("|", "/").strip()
    return re.sub(r"[\[\]<>`]", "", value)[:limit]


def url(value, field):
    value = value.strip()
    if not URL_OK.fullmatch(value):
        sys.exit(f"error: {field} must be a plain https URL, got: {value[:80]!r}")
    return value


def paper_key(value):
    """Stable paper identity: versionless arXiv ID, DOI, or exact URL."""
    parts = urlsplit(value.strip())
    host = (parts.hostname or "").lower().removeprefix("www.")
    path = parts.path.rstrip("/")
    if host == "arxiv.org":
        m = re.fullmatch(r"/(?:abs|pdf|html)/(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?",
                         path, re.I)
        if m:
            return "arxiv:" + m.group(1)
    if host in {"doi.org", "dx.doi.org"}:
        return "doi:" + path.lstrip("/").casefold()
    return host + path + (("?" + parts.query) if parts.query else "")


def title_key(value):
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join("".join(c if c.isalnum() else " " for c in value).split())


def find_duplicate(text, fields):
    """Return the existing method and real category for the same paper."""
    wanted_url, wanted_title = paper_key(fields["paper"]), title_key(fields["title"])
    stage = section = ""
    for line in text.splitlines():
        if m := re.match(r"^## (\d+)\. ", line):
            stage, section = m.group(1), ""
        elif line.startswith("## "):
            stage = section = ""
        elif line.startswith("### "):
            section = line[4:].strip()
        elif stage and section and line.startswith("| **"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) not in (4, 6):
                continue
            link = N.LINK.search(cells[1])
            if not link and len(cells) == 6:
                link = N.LINK.search(cells[4])
            if link and (paper_key(link.group(2)) == wanted_url or
                         wanted_title and title_key(link.group(1)) == wanted_title):
                return cells[0].replace("**", "").strip(), f"{stage}. {section}"


def build_row(f):
    links = []
    if f.get("code"):
        links.append(f"[code]({url(f['code'], 'code link')})")
    if f.get("weights"):
        links.append(f"[weights]({url(f['weights'], 'weights link')})")
    return (f"| **{clean(f['abbrev'], 60)}** | {clean(f['title'])} | {clean(f['year'], 4)} "
            f"| {clean(f['venue'], 40)} | [paper]({url(f['paper'], 'paper link')}) "
            f"| {' & '.join(links) or '—'} |")


def row_year(line):
    m = re.search(r"-(\d{4})-(?:%s|%s)" % (N.ARXIV_RED, N.VENUE_BLUE), line)
    return int(m.group(1)) if m else 0


def insert(text, section, row):
    """Place the row in its subsection's table, keeping rows sorted by year."""
    heading = "### " + section.split(". ", 1)[1]
    lines = text.split("\n")
    try:
        start = lines.index(heading)
    except ValueError:
        sys.exit(f"error: no such subsection: {heading!r}")
    table = next(i for i, l in enumerate(lines[start:], start) if l.startswith("| ---"))
    end = next(i for i, l in enumerate(lines[table + 1:], table + 1) if not l.startswith("| "))
    year = int(clean(row.split("|")[3], 4))
    at = next((i for i in range(table + 1, end) if row_year(lines[i]) > year), end)
    return "\n".join(lines[:at] + [row] + lines[at:])


def self_test():
    body = ("### Abbreviation\n\nZZProbe\n\n### Paper title\n\nAn Image is Worth 1/2 Tokens\n\n"
            "### Paper link\n\nhttps://example.org/papers/zzprobe\n\n### Venue\n\nECCV 2024\n\n"
            "### Year\n\n2024\n\n### Code link\n\nhttps://github.com/o/r\n\n"
            "### Weights link\n\n_No response_\n\n"
            "### Where does it belong?\n\n1. Fixed coverage sampling\n")
    f = parse(body)
    assert f["abbrev"] == "ZZProbe" and "weights" not in f, f
    row = build_row(f)
    assert row.count("|") == 7 and "[code](https://github.com/o/r)" in row, row
    new = N.normalize(insert(open("README.md").read(), f["section"], row))
    assert new.count("**ZZProbe**") == 1 and N.normalize(new) == new, "insert not stable"
    assert "github/stars/o/r" in new, "code link did not become a star badge"
    readme = open("README.md").read()
    duplicate = find_duplicate(readme, {
        "paper": "https://arxiv.org/pdf/2403.06764v9.pdf", "title": "different title"})
    assert duplicate == ("FastV", "4. Decoder-layer token pruning & merging"), duplicate
    assert paper_key("https://arxiv.org/html/2403.06764v2") == "arxiv:2403.06764"
    assert paper_key("https://dx.doi.org/10.1007/ABC/?from=issue") == \
           paper_key("https://doi.org/10.1007/abc")
    duplicate = find_duplicate(readme, {
        "paper": "https://example.org/fastv",
        "title": "AN IMAGE IS WORTH 1/2 TOKENS AFTER LAYER 2 — PLUG-AND-PLAY INFERENCE "
                 "ACCELERATION FOR LARGE VISION-LANGUAGE MODELS"})
    assert duplicate == ("FastV", "4. Decoder-layer token pruning & merging"), duplicate
    assert find_duplicate(readme, f) is None, "unrelated paper reported as duplicate"
    evil = parse("### Abbreviation\n\na | b `x` [y](z)\n\n### Paper link\n\njavascript:alert(1)\n")
    assert clean(evil["abbrev"]) == "a / b x y(z)", clean(evil["abbrev"])  # link defused
    try:
        url(evil["paper"], "paper link"); assert False, "bad URL accepted"
    except SystemExit:
        pass
    print("self-test ok")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if "--self-test" in sys.argv:
        self_test(); sys.exit(0)
    fields = parse(os.environ["ISSUE_BODY"])
    missing = [k for k in ("abbrev", "title", "paper", "venue", "year", "section")
               if k not in fields]
    if missing:
        sys.exit(f"error: issue is missing required fields: {', '.join(missing)}")
    fields["paper"] = url(fields["paper"], "paper link")
    readme = open("README.md").read()
    if duplicate := find_duplicate(readme, fields):
        method, section = duplicate
        print(f"Thanks. This paper is already listed as **{method}** under **{section}**, "
              "so I am closing this request.")
        sys.exit(0)
    readme = insert(readme, fields["section"], build_row(fields))
    open("README.md", "w").write(N.normalize(readme))
    print(f"Added **{clean(fields['abbrev'], 60)}** to _{clean(fields['section'], 80)}_.")
