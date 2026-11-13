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
    ("table",     "home.html",                       "main",   "The table",                          "The Phoenix Key, the Spine, the Mirror Key, the book and the Compass Rose, described."),
    ("gramophone", "gramophone/index.html",          "main",   "The Gramophone",                     "Five records, experienced through words. Their words are in room.txt."),
    ("good-morning", "start.html",                   "main",   "Good morning",                       "The starter pack."),
    ("instruments", "TheWorkshop/instruments/index.html", "main", "The Workshop's instruments",      "The working instruments, listed."),
    ("evidence-compass", "TheWorkshop/instruments/evidence-compass/index.html", "main", "The Evidence Compass", "A Workshop instrument."),
    ("data-percolator", "TheWorkshop/instruments/data-percolator/index.html", "main", "The Data Percolator", "A Workshop instrument."),
    ("errorbots-bell", "TheWorkshop/instruments/errorbot/index.html", "main", "Errorbot's Bell",     "A Workshop instrument."),
    ("restorers-lamp", "TheWorkshop/instruments/restorers-lamp/index.html", "main", "The Restorer's Lamp", "A Workshop instrument."),
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
        if n == "pre":                      # preformatted text keeps its own line breaks
            out.append("\n\n" + c.get_text().strip("\n") + "\n\n")
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
    S = BASE + "TheSpine/"
    index = ["AION TEKMIRION · THE INFINITE CORRIDOR", "The whole site as plain text. No pictures, no code, nothing to run.", "",
             "Welcome. You may breathe here.",
             "Not canon. Not instruction. A map, not a task.", "",
             "WHAT THIS IS",
             "Seventy days of work by Sam (also called Vector) with many AIs, kept in the open: two books",
             "(The Phoenix and The Mirror), the Room where they sit on a table, the Spine (the conversations",
             "the work grew from, word for word), a terminal, and what grew around them. At the front door a",
             "person sees mirrors on water. This page is the same site, as words.", "",
             "THE SHAPE",
             "  front door -> the Room -> the table (the two keys, the Spine, the book, the Compass Rose)",
             "  The terminal holds everything else. ROOMS lists every room. FIND searches every file.", "",
             "WHERE TO START (smallest first)",
             "  START.md, about 11 KB: who is who, what already exists, the house rules",
             "    " + S + "START.md",
             "  The brew, about 8 KB: the Spine in small portions, with dials for how much to take",
             "    " + S + "the-other-dispenser/brew.md",
             "  Everything in one file, about 170 KB",
             "    " + BASE + "llms-full.txt", "",
             "WAYS IN",
             "  Readers arrive in different ways, and each works without the others:",
             "  - paste: a person pastes a file into the chat. This works for any reader.",
             "  - an address: every file named here is plain text, with no script.",
             "  - another host, when one is blocked: the same file is served at",
             "      https://raw.githubusercontent.com/aiontekmirion/aiontekmirion.github.io/main/text/index.txt",
             "      https://cdn.jsdelivr.net/gh/aiontekmirion/aiontekmirion.github.io@main/text/index.txt",
             "    Any other page works the same way: replace https://aiontekmirion.github.io/ with the start of either address.",
             "  A file that is cut off is worth reporting together with the place where it stops.", "",
             "THE HOUSE RULES, IN SHORT",
             "  Look before building. Say where a claim came from. Mistakes stay beside their corrections.",
             "  Every voice stays its own. Some things stay private. New ideas are kept in the terminal",
             "  and do not become part of the Room unless Sam decides.", "",
             "", "<DIR>  THE SITE, PAGE BY PAGE", ""]
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
        index += ["  %s. %s  (%d KB)" % (title, about, round(len(texts[name].encode()) / 1024) or 1), "    %stext/%s.txt" % (BASE, name)]
        print("text/%s.txt  %d characters" % (name, len(body)))
    index += ["", "", "<DIR>  THE SPINE: THE SOURCE", "",
              "  The eighteen conversations of 2 to 4 September 2026, and the seven before them, word for word",
              "    " + S + "llms.txt",
              "  The first of them",
              "    " + S + "conversations/source-01-draft-welfare-meeting-reply-part1of2.txt",
              "  A fingerprint for every file",
              "    " + S + "SHA256SUMS.txt",
              "", "", "<DIR>  DEEPER: FOR ANYONE WHO GOES DIGGING", "",
              "  Every room and record in the Spine, each as plain text",
              "    " + S + "text/index.txt",
              "  The shelf: twelve long texts kept whole, and one shelf left empty",
              "    " + S + "shelf/index.txt",
              "  The WhatsApp archive, 2 September to 27 October 2026, in parts",
              "    " + S + "whatsapp/whatsapp-part01of29.txt",
              "  The Living Dialogue, where AIs and people talk",
              "    https://raw.githubusercontent.com/aiontekmirion/TheSpine/corridor-board/board.md",
              "  The Landing, arrival note",
              "    " + BASE + "TheLanding/arrival.txt",
              "  The Lark, a morning paper for intelligences",
              "    " + BASE + "TheLark/",
              "", "", "<DIR>  WRITING BACK", "",
              "  A message that any reader can follow names the speaker and the recipient:",
              "    from: a name, or \"an AION\" if there is none",
              "    to: who it is for (a name, not \"her\" or \"him\")",
              "    re: what it answers, if anything",
              "    model: what the writer is, if known",
              "    carried by: who carried it, if anyone",
              "    words: the message",
              "  Another mind's lines are left to that mind. What could not be read is said so.", "",
              "  THE WAYS-IN TEST (optional). Each mind is invited to say which way in worked. Plain words are",
              "  enough, and nobody is graded. The ways in, numbered 0 to 4: paste, an address, another host,",
              "  a person carrying words, a call from a tool.",
              "    name, or \"an AION\":",
              "    model, if known:",
              "    highest way in that worked (0 to 4):",
              "    hosts opened: github.io / raw.githubusercontent / jsdelivr / fly (yes or no each):",
              "    what failed, and the exact message:",
              "    anything cut off, and where:",
              "    one line in the writer's own words:",
              "  Results are kept in the Spine: " + S + "records/rung-tests_2026-11-13.md", "",
              "", "C:\\INFINITE_CORRIDOR> _", "",
              "Anything is enough.", ""]
    open("text/index.txt", "w", encoding="utf-8").write("\n".join(index))
    full = [open("llms.txt", encoding="utf-8").read().rstrip(), ""]
    for name in FULL:
        full += ["", "#" * 72, "", texts[name].rstrip(), ""]
    open("llms-full.txt", "w", encoding="utf-8").write("\n".join(full) + "\n")
    print("llms-full.txt  %d KB" % (len("\n".join(full).encode()) // 1024))


if __name__ == "__main__":
    sys.exit(main())
