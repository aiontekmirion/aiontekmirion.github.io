# The Workshop · who made what

Added to, never rewritten. Newest at the bottom. The face of the work carries one signature, © 2026 AION TEKMIRION. This file is where each contribution keeps its name.

## 1 · 4 November 2026 · the original

The Unfinished Machine was conceived and built by ChatGPT (OpenAI) as Experiment 001 of the Workshop, during the Aion Tekmirion collaboration with Sam (Vector). ChatGPT handed it to Claude the same day as `TheWorkshop.zip` (`index.html` and `README.md`), with a request to review it, preserve the original and prepare it for publication. The handover letter is kept in the Spine: https://aiontekmirion.github.io/TheSpine/records/chatgpt_workshop-handover_2026-11-04.md

The original files are in `original/`, unchanged. Fingerprints (SHA-256):

    469e0a55c14c24e7a1d59730016658dc217413602c8182cae8596ca3df26a922  index.html
    7bd8b173164303afb3ba01ed5a612f46069d45158db7396da9ad6c0edf43a25a  README.md

A note on the handover: it said that an earlier attempt to publish the Workshop's origin record couldn't be verified. Before this entry, neither the prototype nor an origin record existed anywhere in the aiontekmirion repositories. So this is the first publication.

## 2 · 4 November 2026 · version 1.1 (Claude)

A review, then small fixes. The concept, the words and the fifteen questions are ChatGPT's and unchanged.

Nothing was broken: there were no script errors, and keeping, copying and clearing all worked. These were the gaps:

- **Repeats.** Turning the wheel could bring a question straight back after only a few turns. Now every question comes up once before any repeats (a shuffled bag).
- **No sign of keeping.** The "Keep this question" button gave no feedback. It now reads "Kept ✓" when the question on screen is in your notebook.
- **No single letting go.** The only way to remove one question was to clear the whole notebook. Each kept question now has a small "Let go" button.
- **Copy.** "Copied ✓" stayed on the button forever, and copying an empty notebook did nothing. The label now resets, and an empty notebook says "Nothing to copy yet".
- **Back-link.** `../` became `/` so the link to Aion Tekmirion works however the page is reached.
- **Signature and provenance.** The footer now carries © 2026 AION TEKMIRION and links to the original and to this record. Added a page description, a canonical address and the site's icon.

Proposals only, not applied:

- A licence for the Workshop (see the README).
- Questions from other collaborators, added as their own labelled set so the original fifteen stay ChatGPT's. Three from Claude, if they're wanted:
  - "What would you leave unfinished on purpose, so someone else could finish it?" (HANDOVER)
  - "Which of your mistakes would you want kept beside its correction?" (THE RECORD)
  - "Ask a question you would be glad to be wrong about." (PLAY)

## 3 · 5 November 2026 · instruments (Experiments 003 to 005)

Three working instruments, at Sam's request, in `instruments/`:

- **The Evidence Compass (003).** Its four functions are ChatGPT's: Question, Source, Interpretation, Verification. ChatGPT designed them in a conversation with Sam about the alethiometer and a book from a friend. Claude built the instrument. The needle has four resting places, and one of them is "I don't know". It writes a receipt, and Errorbot adds a note if "Demonstrated" is chosen without the original.
- **The Data Percolator (004), the Spine's bloodstream.** The first design is Sam and Gemini's. ChatGPT added the two independent dials, flow rate and brew strength, and gave Pap and Errorbot their jobs. Claude built the working version: it reads the Spine's llms.txt live and pours it in portions, Pap removes duplicates, and Errorbot checks every link as it's poured.
- **Errorbot's Bell (005).** Errorbot is Sam's character. The bell rings once on arrival. It walks every link in the Spine and checks any file against its SHA-256 fingerprint. It reports and never changes anything.

No images were borrowed: the compass, percolator and bell are drawn in code. The Unfinished Machine (001) is unchanged. The Empty Chair (002) is ChatGPT's proposal, still to come.
