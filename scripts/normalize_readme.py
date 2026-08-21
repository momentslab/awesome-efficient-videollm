#!/usr/bin/env python3
"""Rewrite the paper tables in README.md into their canonical badge form.

Contributors can add a row in plain markdown -- either the legacy six-column
shape (`| **X** | Title | 2026 | ICLR 2026 | [paper](u) | [code](u) |`) or the
four-column one with plain text -- and this script turns it into the badge form
the README uses. Running it on an already-normalized README changes nothing.

It also regenerates the Contents list and the paper-count badge.

    python3 scripts/normalize_readme.py            # rewrite in place
    python3 scripts/normalize_readme.py --check    # exit 1 if a rewrite is needed
    python3 scripts/normalize_readme.py --self-test
"""
import os, re, sys

SHIELD = "https://img.shields.io/badge/"
ARXIV_RED, VENUE_BLUE = "b31b1b", "1f6feb"
HEADER = "| Method | Title | Venue | Code & Weights |"
SEP = "| --- | --- | :-: | :-: |"
MONTHS = {"January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"}
STAGE_COLORS = {"1": "E4FF77", "2": "FF8934", "3": "6342E8", "4": "ADAAFF"}
STAGE_COLORS = {"1": "E4FF77", "2": "FF8934", "3": "6342E8", "4": "ADAAFF"}
LINK = re.compile(r"\[([^\]]*)\]\((?!#\))([^)]+)\)")
IMG_LINK = re.compile(r"\[!\[([^\]]*)\]\((.*?)\)\]\((.*?)\)")


def esc(s):
    """Escape a string for a shields.io badge path segment."""
    return s.replace("-", "--").replace("_", "__").replace(" ", "_")


def unesc(s):
    return s.replace("__", "\x00").replace("--", "\x01").replace("_", " ") \
            .replace("\x00", "_").replace("\x01", "-")


def arxiv_year(url):
    m = re.search(r"arxiv\.org/abs/(\d{2})(\d{2})\.", url)
    return "20" + m.group(1) if m else ""


def venue_badge(venue, year, paper_url):
    """venue/year in any shape -> the canonical venue badge."""
    m = re.search(re.escape(SHIELD) + r"([^-]+)-(\d{4})-", venue)
    if m:                                     # already a badge
        label, year = unesc(m.group(1)), m.group(2)
    else:
        words = [w for w in venue.strip().split() if w not in MONTHS]
        if words and re.fullmatch(r"\d{4}", words[-1]):
            year, words = words[-1], words[:-1]
        label = " ".join(words)
    year = year.strip() or arxiv_year(paper_url)
    if label.lower() == "arxiv":
        return f"![arXiv]({SHIELD}arXiv-{year}-{ARXIV_RED})"
    return f"![venue]({SHIELD}{esc(label)}-{year}-{VENUE_BLUE})"


def links_badges(cell):
    """Any mix of plain links and badges -> canonical code/weights badges."""
    found = []                                # (kind, url, unofficial)
    for alt, img, target in IMG_LINK.findall(cell):
        blob = (alt + img).lower()
        found.append(("weights" if "weight" in blob else "code", target,
                      "unofficial" in blob))
        cell = cell.replace(f"[![{alt}]({img})]({target})", "")
    for text, url in LINK.findall(cell):
        low = text.lower()
        found.append(("weights" if "weight" in low else "code", url,
                      "unofficial" in low))
    out = []
    for kind, url, unofficial in sorted(found, key=lambda f: f[0] != "code"):
        m = re.match(r"https://github\.com/([^/]+)/([^/#?]+)", url)
        if kind == "code" and m and not unofficial:
            out.append(f"[![Star](https://img.shields.io/github/stars/"
                       f"{m.group(1)}/{m.group(2)}.svg?style=social&label=Star)]({url})")
        elif kind == "code":
            out.append(f"[![Code]({SHIELD}Code-unofficial-lightgrey?logo=github)]({url})")
        elif "huggingface.co" in url:
            label = "%F0%9F%A4%97_Weights" + ("_%28unofficial%29" if unofficial else "")
            out.append(f"[![Weights]({SHIELD}{label}-FFD21E)]({url})")
        elif "drive.google.com" in url:
            out.append(f"[![Weights]({SHIELD}Weights-Drive-4285F4"
                       f"?logo=googledrive&logoColor=white)]({url})")
        else:
            out.append(f"[![Weights]({SHIELD}Weights-link-181717"
                       f"?logo=github&logoColor=white)]({url})")
    return " ".join(out) or "—"


def normalize_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) == 6:                       # legacy: abbr title year venue paper code
        abbr, title, year, venue, paper, links = cells
    elif len(cells) == 4:                     # current: abbr title venue links
        abbr, title, venue, links = cells
        year, paper = "", ""
    else:
        raise ValueError(f"expected 4 or 6 columns, got {len(cells)}: {line[:60]}")
    m = LINK.search(paper) or LINK.search(title)
    url = m.group(2) if m else ""
    if not LINK.search(title):
        title = f"[{title}]({url})" if url else title
        paper = ""                            # paper link folded into the title
    links = links_badges(links + " " + paper if paper else links)
    return f"| {abbr} | {title} | {venue_badge(venue, year, url)} | {links} |"


def nav_chip(num, title, count):
    return (f"[![Stage {num}]({SHIELD}{num}-{esc(title)}_%28{count}%29-{STAGE_COLORS[num]}"
            f"?style=for-the-badge)]({anchor(num + '. ' + title)})")


def section_chip(num, title, count):
    return (f"![Stage {num}]({SHIELD}Stage_{num}-{esc(title)}_%28{count}%29"
            f"-{STAGE_COLORS[num]}?style=flat-square)")


def anchor(heading):
    slug = re.sub(r"[^a-z0-9 -]", "", heading.lower())
    return "#" + slug.replace(" ", "-")


def normalize(text):
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if re.match(r"^## 1\.", l))
    stop = next(i for i, l in enumerate(lines) if l.startswith("## Contributing"))
    body = lines[start:stop]

    stages, counts, fenced = [], {}, False   # pass 1: how many papers per stage
    for line in body:
        if line.startswith("```"):
            fenced = not fenced
        elif fenced:
            continue
        elif (m := re.match(r"^## (\d+)\. (.+)$", line)):
            stages.append((m.group(1), m.group(2)))
            counts[m.group(1)] = 0
        elif line.startswith("| ") and not re.match(r"^\| (Method|Abbreviation|\s*:?-)", line):
            counts[stages[-1][0]] += 1

    out, toc, fenced, eat_blank = [], [], False, False  # pass 2: rows, chips and the TOC
    for line in body:
        if line.startswith("```"):
            fenced = not fenced
        if fenced:
            out.append(line)
            continue
        if line.startswith("![Stage "):      # regenerated from the heading below
            continue
        if eat_blank:                        # the blank line that preceded that chip
            eat_blank = False
            if not line.strip():
                continue
        if (m := re.match(r"^## (\d+)\. (.+)$", line)):
            num, title = m.group(1), m.group(2)
            toc.append(f"- [{num}. {title}]({anchor(line[3:])})")
            out += [line, "", section_chip(num, title, counts[num])]
            eat_blank = True
            continue
        if line.startswith("### "):
            toc.append(f"  - [{line[4:]}]({anchor(line[4:])})")
        if line.startswith("| Method |") or line.startswith("| Abbreviation |"):
            out.append(HEADER)
        elif re.match(r"^\|\s*:?-+:?\s*\|", line):
            out.append(SEP)
        elif line.startswith("| "):
            out.append(normalize_row(line))
        else:
            out.append(line)

    head = lines[:start]
    nav = [nav_chip(num, title, counts[num]) for num, title in stages]
    first = next(i for i, l in enumerate(head) if l.startswith("[![Stage "))
    last = max(i for i, l in enumerate(head) if l.startswith("[![Stage "))
    head = head[:first] + nav + head[last + 1:]

    lines = head + out + lines[stop:]
    c = lines.index("## Contents")
    end = next(i for i, l in enumerate(lines[c + 1:], c + 1) if l.startswith("## "))
    lines = lines[:c + 1] + [""] + toc + [""] + lines[end:]
    text = re.sub(r"badge/papers-[0-9]+-", f"badge/papers-{sum(counts.values())}-",
                  "\n".join(lines))
    for line in text.split("\n"):
        if ")](https://img.shields.io" in line:   # a badge is never a link destination
            sys.exit("error: corrupted badge link, the real URL is lost:\n  " + line.strip())
    return text


def self_test():
    legacy = ("| **X** | A Title | 2026 | ICLR 2026 | [paper](https://arxiv.org/abs/2601.00001) "
              "| [code](https://github.com/o/r) & [weights](https://huggingface.co/o/r) |")
    once = normalize_row(legacy)
    assert once == normalize_row(once), "not idempotent:\n%s\n%s" % (once, normalize_row(once))
    assert "ICLR-2026-" + VENUE_BLUE in once and "github/stars/o/r" in once, once
    assert "%F0%9F%A4%97_Weights-FFD21E" in once and "[A Title](https://arxiv.org/abs/2601.00001)" in once, once
    bare = normalize_row("| **Y** | [T](https://arxiv.org/abs/2605.09999) | arXiv | — |")
    assert f"arXiv-2026-{ARXIV_RED}" in bare, bare      # year recovered from the arXiv id
    assert bare.endswith("| — |"), bare
    assert anchor("Query- / budget-based resampling") == "#query---budget-based-resampling"
    unoff = normalize_row("| **Z** | [T](https://arxiv.org/abs/2204.14198) | NeurIPS 2022 "
                          "| [(unofficial) weights](https://huggingface.co/o/m) |")
    assert unoff == normalize_row(unoff), "unofficial badge not idempotent:\n%s" % unoff
    assert "%28unofficial%29" in unoff, unoff
    assert nav_chip("3", "Connector & Token Reduction", 7).endswith("(#3-connector--token-reduction)")
    parens = ("| **W** | [T](https://arxiv.org/abs/2204.14198) | NeurIPS 2022 | "
              "[![Weights](" + SHIELD + "%F0%9F%A4%97_Weights_(unofficial)-FFD21E)]"
              "(https://huggingface.co/o/m) |")     # an unencoded-paren badge must still parse
    assert "huggingface.co/o/m" in normalize_row(parens), normalize_row(parens)
    print("self-test ok")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if "--self-test" in sys.argv:
        self_test(); sys.exit(0)
    src = open("README.md").read()
    new = normalize(src)
    if "--check" in sys.argv:
        if src != new:
            sys.exit("README.md is not normalized — run scripts/normalize_readme.py")
        print("README.md is normalized")
    elif src != new:
        open("README.md", "w").write(new)
        print("README.md normalized")
    else:
        print("no changes")
