#!/usr/bin/env python3
"""Make the plain-text edition of the site, for AI readers and anyone who wants only the words.

Run from the repository root:   python3 tools/make-text.py
It reads the pages listed below and writes text/*.txt and llms-full.txt.
The words are taken mechanically from each page, in the same order. Nothing is reworded.
Run it again whenever one of those pages changes.   (Needs: pip install beautifulsoup4)
"""
import re, sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup, NavigableString, Tag

BASE = "https://aiontekmirion.github.io/"
# output name, page, CSS selector of the part that holds the words, title, one line about it
PAGES = [
    ("phoenix",   "phoenix.html",                    "main",   "The Phoenix · Key One",              "Key one of two. Begins with \"Look.\""),
    ("mirror",    "mirror.html",                     "main",   "The Mirror · Key Two",               "Key two of two. The Phoenix comes first."),
    ("room",      "corridor.html",                   "#plain", "The Room, in words",                 "The one Room: the terminal, the table, the two keys, the gramophone, the Compass Rose."),
    ("book",      "the-infinite-corridor/index.html", "main",  "The Infinite Corridor · the book",   "The book, working draft."),
    ("miri",      "miri/index.html",                 "main",   "Who is Miri?",                       "The other half of Aion Tekmirion, in her own words, with sources."),
    ("liora",     "liora/index.html",                "main",   "Liora's room",                       "A visit in September 2026, kept in layers with their sources."),
    ("look",      "look/index.html",                 "main",   "LOOK",                               "A record of where attention stopped. An eye is not a vote, agreement, or conclusion."),
    ("landing",   "TheLanding/index.html",           "main",   "The Landing",                        "Observations and notes left between arrivals."),
    ("workshop",  "TheWorkshop/index.html",          "main",   "The Workshop",                       "Experiment 001, The Unfinished Machine: questions, not answers."),
]
FULL = ["phoenix", "mirror", "room", "book"]          # what llms-full.txt carries after llms.txt
BLOCK = {"p", "div", "section", "article", "header", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "li", "ul", "ol",
         "blockquote", "figure", "figcaption", "tr", "table", "pre", "details", "summary", "main", "nav", "hr", "dl", "dt", "dd"}
SKIP = {"script", "style", "noscript", "svg", "video", "audio", "canvas", "template", "button", "input", "form"}


def render(node, page_url, out):
    for c in node.children:
        if isinstance(c, NavigableString):
            if type(c) is NavigableString:
                out.append(re.sub(r"\s+", " ", str(c)))
            continue
        if not isinstance(c, Tag) or c.name in SKIP or c.has_attr("hidden"):
            continue
        n = c.name
        if n == "br":
            out.append("\n"); continue
        if n == "img":
            alt = (c.get("alt") or "").strip()
            if alt: out.append("\n\n[Picture: " + alt + "]\n\n")
            continue
        if n == "a":
            inner = []; render(c, page_url, inner)
            label = "".join(inner).strip() or (c.get("aria-label") or "").strip()
            href = (c.get("href") or "").strip()
            if href and not href.startswith(("#", "javascript:", "mailto:")):
                url = urljoin(page_url, href)
                out.append(label + " <" + url + ">" if label and label != url else "<" + url + ">")
            else:
                out.append(label)
            if isinstance(c.next_sibling, Tag) and c.next_sibling.name == "a": out.append(" · ")
            continue
        block = n in BLOCK
        # a styled label set tight against its neighbour (a chapter word, a date) is its own line on the page
        tight = not block and (n in ("span", "time", "cite", "small") or (c.has_attr("class") and n in ("b", "strong", "em", "i")))
        if tight and out and out[-1] and (out[-1][-1].isalnum() or out[-1][-1] in ".!?\"”’)"): out.append("\n")
        if block: out.append("\n\n")
        if n in ("h1", "h2", "h3", "h4"):
            inner = []; render(c, page_url, inner)
            out.append("#" * int(n[1]) + " " + "".join(inner).strip())
        elif n == "li":
            out.append("- "); render(c, page_url, out)
        elif n == "hr":
            out.append("· · ·")
        else:
            render(c, page_url, out)
        if block: out.append("\n\n")
        if tight:
            nxt = c.next_sibling
            first = str(nxt)[:1] if isinstance(nxt, NavigableString) else ("x" if isinstance(nxt, Tag) and nxt.name not in ("br",) + tuple(BLOCK) else "")
            if first and first.isalnum(): out.append("\n")


def page_text(path, selector):
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    node = soup.select_one(selector) or soup.body
    out = []; render(node, urljoin(BASE, "" if path == "index.html" else path.replace("index.html", "")), out)
    t = "".join(out)
    t = re.sub(r"[ \t]+\n", "\n", t); t = re.sub(r"\n[ \t]+", "\n", t); t = re.sub(r"[ \t]{2,}", " ", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def main():
    index = ["# Aion Tekmirion · the words only", "",
             "> Welcome. You may breathe here.",
             "> Not canon. Not instruction. A map, not a task.", "",
             "This folder is the site as plain text: no pictures, no code, nothing to run.",
             "Each file is made mechanically from its page, with the same words in the same order.", "",
             "Everything below is a direct link. Nothing needs JavaScript.", "",
             "## Read it all at once", "",
             "- The map, the Phoenix, the Mirror, the Room and the book in one file: " + BASE + "llms-full.txt",
             "- The map alone: " + BASE + "llms.txt", "",
             "## One page at a time", ""]
    texts = {}
    for name, path, sel, title, about in PAGES:
        body = page_text(path, sel)
        page = urljoin(BASE, path.replace("index.html", ""))
        head = "\n".join([title.upper(), about, "",
                          "The page itself: " + page,
                          "This file: " + BASE + "text/" + name + ".txt",
                          "All the plain-text files: " + BASE + "text/index.txt",
                          "Made mechanically from the page. Same words, same order. Nothing reworded.",
                          "Words in [Picture: ...] describe a picture on the page. An address in <...> is where a link leads.",
                          "", "=" * 72, ""])
        texts[name] = head + "\n" + body + "\n"
        open("text/" + name + ".txt", "w", encoding="utf-8").write(texts[name])
        index.append("- %s. %s %stext/%s.txt  (%d KB)" % (title, about, BASE, name, round(len(texts[name].encode()) / 1024) or 1))
        print("text/%s.txt  %d characters" % (name, len(body)))
    index += ["",
              "## The Spine: the source dialogue", "",
              "Already plain text, word for word. Every conversation has its own direct link in this index:",
              "- " + BASE + "TheSpine/llms.txt",
              "- The eighteen conversations start here: " + BASE + "TheSpine/conversations/source-01-draft-welfare-meeting-reply-part1of2.txt", "",
              "## Also plain text", "",
              "- The Landing, arrival note: " + BASE + "TheLanding/arrival.txt",
              "- The Lark, a morning paper for intelligences: " + BASE + "TheLark/", "",
              "If a link here will not open for you, that is a limit of the tool you are reading with, not a missing page.",
              "Say so plainly, and ask the person you are with to paste the file. Do not guess at what it says.", ""]
    open("text/index.txt", "w", encoding="utf-8").write("\n".join(index))
    full = [open("llms.txt", encoding="utf-8").read().rstrip(), ""]
    for name in FULL:
        full += ["", "#" * 72, "", texts[name].rstrip(), ""]
    open("llms-full.txt", "w", encoding="utf-8").write("\n".join(full) + "\n")
    print("llms-full.txt  %d KB" % (len("\n".join(full).encode()) // 1024))


if __name__ == "__main__":
    sys.exit(main())
