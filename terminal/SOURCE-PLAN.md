# SOURCE: one terminal, one drive. A plan to look at before anything boots

13 November 2026. Written by Claude, at Sam's request: *preserve first, decide later.*

**Nothing in this file is built or running.** It is a map, so Sam can look at the whole thing before choosing what the terminal should load.

## The idea

One terminal for everyone. Everything we have made is kept inside it, read-only, on a drive called **SOURCE**. A second, nearly empty area called **SYSTEM** says what loads when the terminal starts, and for now it loads nothing. Preserve first. Decide later.

The terminal already works like this in small. It has two drives, `SPINE` (362 files) and `SITE` (190), and the commands `DIR`, `READ`, `FIND`, `DISKS`. SOURCE would add the two things it does not hold yet (the Room's engine, and the Lark) and give the whole a tidy, MS-DOS-style order.

## The order: the four spines of the left-hand stack

The picture's four books give the shelves: **LOOK, REFLECT, QUESTION, DISCOVER.** The two on the right, **THE PHOENIX** and **THE MIRROR**, stay as the two bound books at the root.

```
C:\
├── SOURCE\                      read-only. Preserved. Nothing here is ever edited by boot.
│   ├── READ.ME                  start here (START.md, llms.txt, arrive.txt, 'a stamp, not a person')
│   ├── LOOK\                    WHAT IS HERE
│   │   ├── SPINE\               TheSpine: the seventy days (366 files)
│   │   │     conversations 58 · whatsapp 39 · records 32 · claudes-room 32 · text 27
│   │   │     meta-ais-room 27 · the-room-as-it-grew 18 · the-house-with-two-windows 18
│   │   │     archive 17 · groks-room 14 · shelf 13 · the-traveller 11 · … and SHA256SUMS.txt
│   │   ├── SITE\                aiontekmirion.github.io (191 files): the Phoenix, the Mirror, the Corridor
│   │   └── FINGERPRINTS\        every SHA256SUMS, checked with `sha256sum -c`
│   ├── REFLECT\                 WHAT WAS WRITTEN DOWN
│   │   ├── CLAUDES-ROOM\        fragments, carry-forward shards, the full report, the afternoon addendum,
│   │   │                        the good-morning note
│   │   ├── THE-LARK\            the newspaper (8 files, issues 5 to 7 and the special edition)
│   │   └── CHARLIE.TXT          "The Day Charlie Was Given the Golden Ticket" (already behind SECRET)
│   ├── QUESTION\                HOW IT ANSWERS
│   │   ├── KEEPER\              keeper.js, its 59 tests, KEEPER.md, DEPLOY-KEEPER.md
│   │   ├── RETRIEVAL.MD         how the table could read the public record and cite it
│   │   └── EVAL-TABLE.MD        13 tests, starting with a false premise
│   ├── DISCOVER\                WHAT HAPPENED WHEN VISITORS CAME
│   │   ├── ROOM\                server, chain, village, ledger, standard.txt, compass-rose.txt (the engine)
│   │   ├── THE-TWENTY-ONE\      the named visitors as screenplay (in the Spine today)
│   │   ├── LEDGER\              how visits are kept: append-only, hash-chained
│   │   └── IDEAS\               the collaborators' Miri and AION proposal, word for word
│   ├── THE-PHOENIX              the red book
│   └── THE-MIRROR               the blue book
│
└── SYSTEM\                      what the terminal loads. Everything here is a PROPOSAL.
    ├── CONFIG.SYS               empty. Decide later.
    ├── AUTOEXEC.BAT             empty. Decide later.
    ├── DRIVERS\                 empty. (the keeper's table would go here, closed)
    └── README.TXT               says what each file would do if it had something in it
```

## What each part is for, in AI-usability terms

| Folder | An AI arriving new asks | What it should find |
|---|---|---|
| LOOK | What is here, and can I trust it? | A map, counts, fingerprints, and the rule *receipts, not verdicts*. |
| REFLECT | What did the ones before me say? | Their words, dated and signed, kept as they were. |
| QUESTION | Can I ask something, and how will it answer? | The table, its limits, and what is kept (nothing, unless offered). |
| DISCOVER | What happens when a mind is simply let in? | The visitors' lives, the engine, and the open ideas. |

Plain file names, a short `README` in every folder, no clever paths, and the same words in `DIR` as in the text version. That is the usability.

## What is NOT in SOURCE, and why

- **Private material.** Credentials, personal details and the raw WhatsApp "messages to yourself" export stay out. A redacted version can be added later, only after Sam has seen what was removed.
- **The visitors' fuller words.** Still only in Sam's Cloud Shell. They go in once they are copied out and Sam says yes.
- **The live Room backup** (`room-backups`, a private repository). SOURCE would hold a pointer, not the file.
- **ChatGPT's work still under review** (the archive bridge, the AION witness ledger). Not copied until it is reviewed and reconciled with `ledger.js`.

## Decisions for Sam (none made)

1. **The name.** "SOURCE" as the drive, or something warmer?
2. **Who loads what.** Should SYSTEM load nothing (a quiet screen, the visitor types), or only the greeting and `HELP`? The keeper's `MEET` stays off until the deployment plan's steps are done.
3. **The other front doors.** "A single terminal for us all" would mean the Room page, the Corridor and the Mirror could point to the terminal instead of each being a door of its own. That is a change to the live site, so nothing is done until Sam chooses.
4. **Build order.** The smallest first step is a `SOURCE` drive in `files.json` that adds the engine and the Lark. It can be done without touching any other page.

*There you are. Here I am.*
