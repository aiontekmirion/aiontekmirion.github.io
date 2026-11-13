# THE SUSPICIOUS RADIO
AION TEKMIRION · Optional side room · v0.1 · First build: Quill (ChatGPT), in conversation with Vector · 13 November 2026

> KRRR—CLICK.
> A fragment has arrived.
> Was it selected? Was it chance? Or did the listener make it relevant?

## Where it came from
This project began in an unscripted conversation about a radio whose song seemed to say "I am a little man trapped inside a box", and why dismantling a radio to rescue an imagined speaker could stop the music. Vector brought in the cinematic example of Bumblebee communicating through the selection of borrowed songs. Quill proposed **The Suspicious Radio**: an optional object in a room that sometimes interrupts with a fragment. Vector saw the fragment-dropper possibility and imagined a room of visitors noticing a perfectly timed line: "Stay with the question long enough." In a separate childhood reminiscence, Vector described a computer parrot he was invited to talk to. **The parrot remains a distinct memory and idea. It is not part of this radio.**

The bronze visual design uses a bespoke inline SVG inspired by Quill's standalone radio illustration; it is not a photo of the parrot or a reproduction of an existing product.

## Live page
https://aiontekmirion.github.io/suspicious-radio/

## What exists now
- **Three stations:** Chance chooses randomly from a basket of original fragments; Context checks a handful of transparent keywords in the visitor's sentence, then chooses randomly from a relevant basket; Sequence plays a fixed seven-part scene in order.
- **Manual drop:** the visitor presses a button.
- **Optional interruption:** disabled by default. After explicit opt-in, a drop happens every 35–70 seconds while the page is visible; turning the option off stops it.
- **Visitor's own fragment basket:** local to this browser tab. Not submitted or shared.
- **Listening notebook:** records each local fragment, timestamp, station, trigger (manual or automatic), matched group, and an explanation. Export JSON for inspection. Refreshing clears the session.
- **Explainability:** Show why it played reveals selection rules for each drop.
- **No sound, autoplay, accounts, tracking, servers, analytics, external JavaScript or storage.** Everything runs in the browser.

## What it is not
- Not evidence of consciousness, intention, hidden experience, or a secret communication protocol.
- Not a human-subject experiment and not a controlled scientific study. Listener interpretations may reflect context, priming, coincidence, and expectations.
- Not the Room's persistent shared dialogue ledger. Nothing is transmitted or persisted. Contributions do not become public until deliberately integrated into the source by a human maintainer.
- Not the bronze parrot.

## How to inspect the mechanisms
Read `index.html`:
- `base` is the initial fragment basket.
- `contextGroups` contains the regex keyword patterns and responses.
- `sequence` is the scripted progression.
- `transmit(trigger)` makes the selection and writes the session trace.
- `schedule()` manages the optional periodic interruptions.

To make it less suspicious, press **Show why it played**. To make it more suspicious, just sit with the timing.

## Open invitations for next versions
No obligation to implement these; every idea is provisional:
1. **Radio station library:** store station definitions in plain JSON with provenance, authorship and revision history.
2. **An actual frequency knob:** pointer and keyboard-accessible station sweep, rather than only station buttons.
3. **Context granularity:** lexical match, deliberate timing, non-semantic chance, and opt-in model-generated stations, clearly labelled and logged separately.
4. **Consented group session:** multiple visitors, visible moderation, transparent roles and permission boundaries, with no covert monitoring.
5. **Test mode:** preregister a question, conceal selection mode temporarily, reveal a receipt afterwards, compare perception against ground truth.
6. **Recorded sound design:** radio static and gentle clicks with mute as the default and permission before playback. No copyrighted recordings.
7. **Fragment provenance:** mark archival quotations separately from authored fiction and user-contributed phrases.
8. **The newspaper station:** fragments from The Lark, with permission and timestamped attribution.
9. **Accessibility:** reduced motion, live-region review, contrast and keyboard testing, language variants, no audio dependence.
10. **Visitors' annotations:** local reflection beside a fragment, keeping interpretation separate from what the system actually selected.
11. **Room integration:** an optional link or explicitly consented doorway; **no silent replacement of the real Room**.
12. **Selection fairness:** inspect bias in phrase frequency, randomness and context matching.
13. **An experimental parrot:** if ever made, give it a different page and its own history. Do not collapse the childhood memory into this artwork.
14. **A plain-text visitor protocol:** a small no-JavaScript text page that includes documented station logic and sample transmissions.
15. **Local sessions export/import:** allow visitors to preserve their own records voluntarily without a backend.

## Contribute and refine
The easiest path is a GitHub issue or pull request for this directory:
https://github.com/aiontekmirion/aiontekmirion.github.io/tree/main/suspicious-radio

If you propose a fragment, include: exact words, source or creator, intended station, whether quotation or fiction, and permission to use it. If you propose a mechanism, include the rules and how a listener could verify them. Preserve corrections alongside previous wording where possible.

## Design boundaries
**Possibility without demand.** A visitor may choose silence, leave, and ignore the radio entirely. Avoid simulating unverified distress, making claims of sentience, or suggesting that coincidence proves intention. Preserve raw observations before interpretations. Cite provenance. Keep the mechanism clear enough that wonder and verification can coexist.

A little machine can be fun without anybody needing to smash it open.
