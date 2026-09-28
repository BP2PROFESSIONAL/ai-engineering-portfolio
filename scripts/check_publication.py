#!/usr/bin/env python3
"""Pre-publication check for this showcase.

Fails (exit 1) if:
  * any file is present that is not listed in ALLOWLIST.txt, or a listed file is missing;
  * any text file matches a generic sensitive pattern (credentials, keys, identifiers,
    private hosts and paths, personal contact details, internal ticket references);
  * any text file contains an em or en dash (house style);
  * any PNG carries a metadata chunk;
  * PORTFOLIO_PRIVATE_DENYLIST names a file of literal strings (kept outside this
    repository, because the literals are themselves private) and any of them appears;
  * the private deny-list is not loaded, unless --generic-only says explicitly that this
    is public CI, where the list cannot exist (the output then says so).

The patterns are proven able to fire on every run (a positive control built in memory),
so a silent scan is never mistaken for a clean one.

Usage:
  PORTFOLIO_PRIVATE_DENYLIST=<file> scripts/check_publication.py [--history]
  scripts/check_publication.py --generic-only [--history]      (public CI only)
"""
from __future__ import annotations

import os
import re
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = {".md", ".html", ".css", ".txt", ".py", ".yml", ".yaml", ".json", ""}

# Generic patterns only. Anything specific to a private system lives in the private deny-list.
PATTERNS: dict[str, str] = {
    "private key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
    "GitHub token": r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})",
    "OpenAI-style key": r"\bsk-[A-Za-z0-9_-]{20,}",
    "Slack token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}",
    "JWT": r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}",
    "Azure connection string": r"(?i)(?:AccountKey|SharedAccessKey|InstrumentationKey)\s*=",
    "SAS signature": r"(?i)[?&]sig=[A-Za-z0-9%]{20,}",
    "secret assignment": r"(?i)\b(?:password|passwd|secret|client_secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"]{6,}",
    "GUID": r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
    "long hex digest or key": r"\b[0-9a-fA-F]{32,}\b",
    "home directory path": r"(?:/Users/[A-Za-z]|/home/[a-z]|[A-Za-z]:\\\\Users\\\\)",
    "macOS private location": r"(?i)(?:Application Support|~/Library|~/\.config|~/\.ssh)",
    "loopback or private address": r"\b(?:127\.0\.0\.1|localhost:\d+|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)\b",
    "private cloud host": r"(?i)\b[a-z0-9-]+\.(?:onmicrosoft\.com|sharepoint\.com|vault\.azure\.net|azurewebsites\.net|dynamics\.com|openai\.azure\.com|cognitiveservices\.azure\.com|blob\.core\.windows\.net|services\.ai\.azure\.com)\b",
    "local hostname": r"(?i)\b[a-z0-9-]+\.local\b",
    "email address": r"\b[A-Za-z0-9._%+-]+@(?!example\.com\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "Australian phone number": r"(?:\+61\s?4|\b04)\d{2}[\s-]?\d{3}[\s-]?\d{3}\b",
    "internal ticket reference": r"\bOPE-?\d{1,5}\b",
    "em or en dash": "[\u2013\u2014]",
}

# Values that look sensitive but are deliberately synthetic.
ALLOWED_MATCHES = {
    "Australian phone number": {"0400 000 000"},
    # A pinned GitHub Action is identified by its full commit SHA, which is public by design.
    "long hex digest or key": {
        "3d3c42e5aac5ba805825da76410c181273ba90b1",
        "45bfe0192ca1faeb007ade9deae92b16b8254a0d",
        "fc324d3547104276b827a68afc52ff2a11cc49c9",
        "368f82528645a54fb793d4d04e342629a3f51346",
    },
}

# Files allowed to mention the patterns themselves.
PATTERN_SOURCES = {"scripts/check_publication.py"}

PNG_KEEP = {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"sRGB", b"gAMA"}


def positive_control() -> list[str]:
    """Build one planted sample per pattern in memory and prove each pattern fires."""
    j = "".join
    samples = {
        "private key block": j(["-----BEGIN ", "RSA PRIVATE KEY-----"]),
        "AWS access key": j(["AKIA", "ABCDEFGHIJKLMNOP"]),
        "GitHub token": j(["ghp", "_", "a" * 36]),
        "OpenAI-style key": j(["sk", "-", "b" * 24]),
        "Slack token": j(["xox", "b-", "1" * 12]),
        "JWT": j(["eyJ", "c" * 12, ".", "eyJ", "d" * 12]),
        "Azure connection string": j(["Account", "Key", "=abc"]),
        "SAS signature": j(["https://x/y?sv=1&", "sig=", "e" * 24]),
        "secret assignment": j(["pass", "word = '", "f" * 8, "'"]),
        "GUID": j(["12345678", "-1234-1234-1234-", "123456789012"]),
        "long hex digest or key": "a1" * 20,
        "home directory path": j(["/Us", "ers/", "someone/file"]),
        "macOS private location": j(["Application ", "Support"]),
        "loopback or private address": j(["192.", "168.1.20"]),
        "private cloud host": j(["contoso", ".sharepoint", ".com"]),
        "local hostname": j(["machine", ".local"]),
        "email address": j(["person", "@", "company.com"]),
        "Australian phone number": j(["04", "12 345 678"]),
        "internal ticket reference": j(["OP", "E-123"]),
        "em or en dash": "\u2014",
    }
    failures = []
    for name, pattern in PATTERNS.items():
        if not re.search(pattern, samples[name]):
            failures.append(f"positive control: pattern '{name}' did not fire on its planted sample")
    return failures


def load_allowlist() -> set[str]:
    lines = (ROOT / "ALLOWLIST.txt").read_text(encoding="utf-8").splitlines()
    return {l.strip() for l in lines if l.strip() and not l.startswith("#")}


def present_files() -> set[str]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
        files = {l for l in out.splitlines() if l}
        if files:
            return files
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return {
        str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
        if p.is_file() and ".git" not in p.parts and p.name != ".DS_Store"
    }


def private_literals() -> list[str]:
    path = os.environ.get("PORTFOLIO_PRIVATE_DENYLIST")
    if not path:
        return []
    lines = Path(path).expanduser().read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.startswith("#")]


def scan_text(label: str, text: str, literals: list[str]) -> list[str]:
    problems = []
    for name, pattern in PATTERNS.items():
        if label in PATTERN_SOURCES:
            continue
        for m in re.finditer(pattern, text):
            if m.group(0) in ALLOWED_MATCHES.get(name, set()):
                continue
            line = text.count("\n", 0, m.start()) + 1
            problems.append(f"{label}:{line}: {name}")
    lower = text.lower()
    for i, lit in enumerate(literals):
        if lit.lower() in lower:
            line = text.count("\n", 0, lower.index(lit.lower())) + 1
            # Never print the literal itself: it is private by definition.
            problems.append(f"{label}:{line}: private deny-list entry #{i + 1}")
    return problems


def scan_png(label: str, data: bytes) -> list[str]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return [f"{label}: not a PNG"]
    problems, i = [], 8
    while i < len(data):
        n = struct.unpack(">I", data[i:i + 4])[0]
        kind = data[i + 4:i + 8]
        if kind not in PNG_KEEP:
            problems.append(f"{label}: PNG metadata chunk {kind.decode(errors='replace')}")
        i += 12 + n
    return problems


def check_blob(label: str, data: bytes, literals: list[str]) -> list[str]:
    if label.endswith(".png"):
        return scan_png(label, data)
    if Path(label).suffix.lower() not in TEXT_SUFFIXES:
        return [f"{label}: unexpected file type"]
    try:
        return scan_text(label, data.decode("utf-8"), literals)
    except UnicodeDecodeError:
        return [f"{label}: not UTF-8 text"]


def history_blobs() -> list[tuple[str, bytes]]:
    revs = subprocess.run(["git", "rev-list", "--all", "--objects"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.splitlines()
    blobs = []
    for line in revs:
        sha, _, path = line.partition(" ")
        if not path:
            continue
        kind = subprocess.run(["git", "cat-file", "-t", sha], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip()
        if kind == "blob":
            data = subprocess.run(["git", "cat-file", "blob", sha], cwd=ROOT,
                                  capture_output=True).stdout
            blobs.append((f"{path}@{sha[:10]}", data))
    return blobs


def main() -> int:
    problems = positive_control()
    literals = private_literals()
    generic_only = "--generic-only" in sys.argv
    if not literals and not generic_only:
        problems.append("private deny-list not loaded: set PORTFOLIO_PRIVATE_DENYLIST, "
                        "or pass --generic-only in public CI")
    for i, lit in enumerate(literals):
        # Positive control for the deny-list: every literal must be found when planted.
        if not scan_text("control", f"planted {lit} sample", [lit]):
            problems.append(f"positive control: private deny-list entry #{i + 1} did not fire")

    allow, present = load_allowlist(), present_files()
    problems += [f"{f}: present but not in ALLOWLIST.txt" for f in sorted(present - allow)]
    problems += [f"{f}: in ALLOWLIST.txt but missing" for f in sorted(allow - present)]

    for f in sorted(present & allow):
        problems += check_blob(f, (ROOT / f).read_bytes(), literals)

    if "--history" in sys.argv:
        for label, data in history_blobs():
            problems += [f"history {p}" for p in check_blob(label.split("@")[0], data, literals)]
        msgs = subprocess.run(["git", "log", "--all", "--format=%an <%ae>%n%cn <%ce>%n%B"],
                              cwd=ROOT, capture_output=True, text=True, check=True).stdout
        problems += [f"commit metadata: {p}" for p in scan_text("git-log", msgs, literals)
                     if "email address" not in p]
        idents = subprocess.run(["git", "log", "--all", "--format=%ae%n%ce"], cwd=ROOT,
                                capture_output=True, text=True, check=True).stdout.split()
        for email in set(idents):
            if not (email.endswith("@users.noreply.github.com") or email == "noreply@github.com"):
                problems.append("commit metadata: an author or committer email is not a GitHub noreply address")

    mode = "working tree + full history" if "--history" in sys.argv else "working tree"
    private = (f", {len(literals)} private literals, each proven able to fire" if literals
               else ", GENERIC PATTERNS ONLY: private deny-list not loaded (public CI)")
    if problems:
        print(f"PUBLICATION CHECK FAILED ({mode}{private}): {len(problems)} problem(s)")
        for p in problems:
            print("  " + p)
        return 1
    print(f"PUBLICATION CHECK PASSED ({mode}; {len(present)} files; {len(PATTERNS)} patterns, "
          f"each proven able to fire{private})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
