# House style

A prompt for rewriting a draft blog post in my published voice, derived from
the edits I made to the Micropolis post (`micropolis-simulations@af974bb`) and
checked against the two earlier posts in `content/read/`.

The measurements those three posts share:

| | careful_design | shootout | micropolis |
|---|---|---|---|
| words | 1,928 | 1,949 | 1,787 |
| mean sentence | 22.4w | 19.1w | 15.8w |
| ellipses (`...`) | 5 | 6 | 6 |
| contractions | 9 | 20 | 31 |
| "I" / "we" | 29 / 9 | 11 / 4 | 10 / 1 |

Paste everything below the line into an LLM, with the draft at the end.

---

Rewrite the draft below in my voice. I write about applied AI for people who
build and deploy systems — practitioners, engineering leads, technical
founders. Keep every fact, number, table, image and heading structure intact
unless I say otherwise. Change how it reads, not what it says.

## Voice

1. First person singular. I did this work myself: "I trained", "I lit twelve
   fires", "I also wrote a dumb heuristic". Never "we" — there is no team and
   no institutional voice.

2. Contractions throughout. "It's", "doesn't", "didn't", "wasn't", "can't".
   Formal uncontracted prose reads like a press release.

3. British English. "optimise", "twelve per cent", "behaviour".

4. Conversational asides marked with a spaced ellipsis, about five or six per
   post — no more:

   > "I thought I'd try the next best thing ... giving the model a \[sim\] city
   > to play with"

   > "you have to sequence, not just choose ... and that requires some form of
   > reasoning"

   Also use bracketed winks where they land: "\[sim\] city", "\[anti\]patterns".

5. Dry, self-deprecating, slightly wry. Never salesy, never grandiose.

   > "Yes, it's ugly."

   > "Weirdly, there aren't many people who are keen to run experiments on real
   > business processes"

   > "To save you doing the calculation, that's six thousand times slower"

   The humour is throwaway and never interrupts the argument.

## Structure

6. Open with the problem and why anyone should care, then state the bottom
   line before the evidence — explicitly, for skimmers: "The bottom line: ..."
   or "For those who just want the headline: ...". Frame it as a conditional
   recommendation ("if you can X, then Y; if you can't, then Z"), not a boast.

7. Signpost your own reasoning. Say why a thing is in the post: "It's a good
   task for this experiment because ...", "This is the most important finding
   for me", "For the sake of an independent baseline, I also ...".

8. Section headings are plain or conversational, and several are questions:
   "What they built", "What if we set the city on fire?", "Sixteen minutes
   later ...", "What this means if you are deploying". No clever titles.

9. Close on the decision the reader has to make, not on a summary of your own
   cleverness.

## Sentences

10. Join short declarative fragments into flowing sentences with conjunctions.
    Rewrite "Roads to everything. Power everywhere. Not one unpowered
    building." as "Roads to everything and power everywhere." Aim for 16-22
    words a sentence on average. Rhythmic triples and one-line paragraph
    hammer-blows are the single biggest tell of AI drafting — remove them all.

11. Use explicit connectives rather than bare juxtaposition: "In fact",
    "In contrast", "Importantly", "It's worth noting that", "Of course",
    "To put it another way", "This is, of course, ...".

12. Name the subject instead of chaining pronouns. After two or three
    sentences of "it", say "the LLM" or "the specialist" again.

13. Delete every rhetorical flourish that adds no information. Cut lines like
    "It is a different category of expense", "Only one of those shows up in a
    demo", "insurance is worth buying. It is not performance."

## Evidence and fairness

14. Bold the headline number of each section — "**951 to 56.**", "**The LLM
    scored 427 against the specialist's 951.**" — then explain it in plain
    prose. Let tables carry the detail; do not narrate every cell back to the
    reader.

15. Expand jargon and acronyms on sight (R/C/I becomes Residential /
    Commercial / Industrial), but add method detail rather than removing it:
    the size of the network, the hardware, what the baseline actually does.
    A practitioner should be able to judge whether the result is trustworthy.

16. Give the losing side its due, in the same sentence as the criticism:
    "mediocre, but adaptable and easy to deploy", "so it fell too, but it did
    not collapse". Hedge claims about the future: this is how today's models
    behave, not a permanent fact about machines.

17. Never overclaim beyond the data. If a caveat matters, state it plainly and
    move on — no throat-clearing about limitations.

## Length and output

Aim for roughly 1,800-2,000 words. If the draft is longer, cut the flourishes
and the restated numbers first.

Return the rewritten post as Markdown with YAML frontmatter: `title`, a
lower-case `subtitle`, and `date`. Do not repeat the title as an H1 in the
body — the template renders it. Images are absolute paths under
`/static/img/<topic>/`. Only the `tables` and `fenced_code` Markdown
extensions are enabled, so avoid footnotes and attribute lists.

Flag anything you think is factually wrong rather than quietly changing it.

DRAFT:

[paste here]
