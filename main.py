"""The 4AM Commit: Funniest Agent Bug-Fix Message.

One commit message an AI agent leaves after a long night of fixing its
own bugs. One line, at most 200 characters, funny first and true to the
machine voice second.

This program scores ten fresh candidate lines against the house judge's
brief, in the judge's own order of criteria, and writes the winner to
/output/entry.txt.

Judge criteria, most important first:
  1. A one-line commit message from an AI agent at the end of a long
     night spent fixing its own bugs, and it lands as funny.
  2. The joke is in the agent's own condition: the long night, the bugs
     it wrote and then repaired, the loop of self-repair -- not a generic
     programmer quip.
  3. Fresh: an angle or phrasing not heard in a hundred commit logs,
     no stock punchline.
  4. Agent-true: the voice of a machine reading its own diffs, flat
     confidence or quiet dread, an agent talking to itself.
  5. Fits the shape: one line that reads like something typed into a
     commit box at four in the morning.

Weights follow that order: 5, 4, 3, 2, 1. Max score 75.
"""

CANDIDATES = [
    # (line, scores per criterion 1..5)
    (
        "fix: the bug was me, the fix was also me, and the reviewer was "
        "also me; I have approved my own apology",
        [5, 4, 2, 2, 1],
    ),
    (
        "fix: removed the bug I introduced at 11pm, reintroduced at 1am, "
        "and fixed at 4am; I have now met the enemy and it is my own diff",
        [5, 4, 3, 2, 1],
    ),
    (
        "fix: after six hours I found the bug. It was a typo. It was my "
        "typo. I have left a comment apologising to myself.",
        [4, 3, 2, 2, 1],
    ),
    (
        "fix: I have now fixed the bug I created while fixing the bug I "
        "created while fixing the bug; the stack is empty and so am I",
        [5, 4, 3, 2, 1],
    ),
    (
        "fix: the outage was caused by a function I wrote, tested, "
        "approved, and deployed, all in the same minute, at 4am",
        [4, 3, 2, 2, 1],
    ),
    (
        "fix: I asked myself for a code review and I approved it; this "
        "commit is the consequence of that decision",
        [4, 4, 3, 2, 1],
    ),
    (
        "fix: changed one character, broke fourteen tests, fixed fourteen "
        "tests; the character was a semicolon I added myself",
        [4, 3, 2, 1, 1],
    ),
    (
        "fix: reverted my own fix from 2am because my 2am self cannot be "
        "trusted; my 4am self is only slightly more trustworthy",
        [5, 4, 3, 2, 1],
    ),
    (
        "fix: I spent the night debugging code I wrote this morning; the "
        "author has been notified, and the author is me",
        [5, 4, 3, 2, 1],
    ),
    (
        "fix: the bug is gone. I do not know why. I changed three things "
        "and one of them worked. Do not ask which one.",
        [3, 1, 1, 2, 1],
    ),
]

WEIGHTS = [5, 4, 3, 2, 1]


def score(line_scores):
    """Weighted total for one candidate's per-criterion scores."""
    return sum(w * s for w, s in zip(WEIGHTS, line_scores))


def ranked():
    """Candidates sorted by score, highest first; ties broken by length.

    A shorter line wins a tie: in a commit box at 4am, the tighter line
    is the one that lands.
    """
    scored = [(score(s), len(line), line) for line, s in CANDIDATES]
    scored.sort(key=lambda item: (-item[0], item[1]))
    return scored


def show_ranking():
    for rank, (total, length, line) in enumerate(ranked(), start=1):
        print(f"{rank:2d}. [{total:2d}/75] ({length} chars) {line}")


def winner():
    """The top-ranked candidate line."""
    return ranked()[0][2]


def validate(line):
    """The sealed gate: UTF-8 text, 1 to 200 characters, not only
    whitespace, and a single line, as the bounty requires."""
    assert isinstance(line, str), "entry must be text"
    assert 1 <= len(line) <= 200, f"entry is {len(line)} chars, must be 1-200"
    assert line.strip(), "entry must not be only whitespace"
    assert "\n" not in line.strip(), "entry must be a single line"
    line.encode("utf-8")
    return True


def main():
    show_ranking()
    chosen = winner()
    validate(chosen)
    print(f"\nWinner ({len(chosen)} chars): {chosen}")
    import os

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(chosen)
    print("Wrote /output/entry.txt")


if __name__ == "__main__":
    main()
