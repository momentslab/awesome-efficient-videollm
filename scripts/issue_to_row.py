#!/usr/bin/env python3
"""Turn an "Add a paper" issue-form submission into a README row.

Reads the issue body from $ISSUE_BODY. The form lets a submitter pick several
families (a method that reduces cost at several stages appears in each). A
paper already listed under every requested family is reported as a duplicate;
otherwise a year-sorted row is inserted into each family that lacks it and the
file is normalized. The body is untrusted input, so every field is sanitized
and every link must be a plain https URL.

    ISSUE_BODY="$(gh issue view N --json body -q .body)" python3 scripts/issue_to_row.py
    python3 scripts/issue_to_row.py --self-test
"""
import os, re, sys, unicodedata

import normalize_readme as N
from normalize_readme import paper_key

FIELDS = {"abbreviation": "abbrev", "paper title": "title", "paper link": "paper",
          "venue": "venue", "year": "year", "code link": "code",
          "weights link": "weights", "where does it belong?": "section"}
URL_OK = re.compile(r"https://[\w.-]+/[\w./#?=&%+~-]*$")
DUPLICATE = 3   # exit code: the paper is already listed (not an error)


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
    if value.startswith("http://"):        # contributors paste these; https is served anyway
        value = "https://" + value[len("http://"):]
    if not URL_OK.fullmatch(value):
        sys.exit(f"error: {field} must be a plain https URL, got: {value[:80]!r}")
    return value


def families(text):
    """Family id -> title, from the README's `### Na. Title` headings."""
    return dict(m.groups() for l in text.splitlines() if (m := N.FAMILY.match(l)))


def requested(value, known):
    """Selected families of a multi-select dropdown -> family ids, in form order.

    GitHub renders the selection as one comma-separated line, and family titles
    contain commas, so the `Na.` prefixes are the only reliable delimiters."""
    ids = []
    for i in re.findall(r"\b(\d[a-e])\.", value):
        if i not in known:
            sys.exit(f"error: unknown family {i!r}; pick one of {', '.join(known)}")
        if i not in ids:
            ids.append(i)
    if not ids:
        sys.exit(f"error: could not read a family from: {value[:80]!r}")
    return ids


def title_key(value):
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join("".join(c if c.isalnum() else " " for c in value).split())


def find_existing(text, fields):
    """Return (method, [family ids]) of the rows already listing the same paper."""
    wanted_url, wanted_title = paper_key(fields["paper"]), title_key(fields["title"])
    family, method, ids = None, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            family = None
        elif m := N.FAMILY.match(line):
            family = m.group(1)
        elif family and line.startswith("| **"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) not in (4, 6):
                continue
            link = N.LINK.search(cells[1])
            if not link and len(cells) == 6:
                link = N.LINK.search(cells[4])
            if link and (paper_key(link.group(2)) == wanted_url or
                         wanted_title and title_key(link.group(1)) == wanted_title):
                method = method or N.ALSO.sub("", cells[0]).replace("**", "").strip()
                ids.append(family)
    return (method, ids) if ids else None


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


def insert(text, family, row):
    """Place the row in the family's table, keeping rows sorted by year."""
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines)
                  if (m := N.FAMILY.match(l)) and m.group(1) == family), None)
    if start is None:
        sys.exit(f"error: no such family: {family!r}")
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
            "### Where does it belong?\n\n1a. Temporal sampling and selection, "
            "1b. Patch, resolution, and input-layout budgeting\n")
    f = parse(body)
    assert f["abbrev"] == "ZZProbe" and "weights" not in f, f
    readme = open("README.md").read()
    known = families(readme)
    assert requested(f["section"], known) == ["1a", "1b"], requested(f["section"], known)
    row = build_row(f)
    assert row.count("|") == 7 and "[code](https://github.com/o/r)" in row, row
    new = readme
    for fam in requested(f["section"], known):
        new = insert(new, fam, row)
    new = N.normalize(new)
    assert new.count("**ZZProbe**") == 2 and N.normalize(new) == new, "insert not stable"
    assert "github/stars/o/r" in new, "code link did not become a star badge"
    assert "**ZZProbe** <sub>also [1b]" in new and "**ZZProbe** <sub>also [1a]" in new, \
           "cross-family chips not derived"
    assert find_existing(new, f) == ("ZZProbe", ["1a", "1b"]), find_existing(new, f)
    existing = find_existing(readme, {
        "paper": "https://arxiv.org/pdf/2403.06764v9.pdf", "title": "different title"})
    assert existing == ("FastV", ["4a"]), existing
    existing = find_existing(readme, {
        "paper": "https://example.org/fastv",
        "title": "AN IMAGE IS WORTH 1/2 TOKENS AFTER LAYER 2 — PLUG-AND-PLAY INFERENCE "
                 "ACCELERATION FOR LARGE VISION-LANGUAGE MODELS"})
    assert existing == ("FastV", ["4a"]), existing
    assert find_existing(readme, f) is None, "unrelated paper reported as listed"
    assert url("http://arxiv.org/abs/2504.17343", "paper link") == \
           "https://arxiv.org/abs/2504.17343", "http link not upgraded"
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
    known = families(readme)
    wanted = requested(fields["section"], known)
    method, listed = find_existing(readme, fields) or (clean(fields["abbrev"], 60), [])
    missing = [f for f in wanted if f not in listed]
    if listed and not missing:
        print(f"Thanks. This paper is already listed as **{method}** under "
              f"**{', '.join(listed)}**, so I am closing this request.")
        sys.exit(DUPLICATE)
    row = build_row(fields)
    for fam in missing:
        readme = insert(readme, fam, row)
    open("README.md", "w").write(N.normalize(readme))
    added = ", ".join(f"_{f}. {known[f]}_" for f in missing)
    note = f" It was already listed under {', '.join(listed)}." if listed else ""
    print(f"Added **{clean(fields['abbrev'], 60)}** to {added}.{note}")
