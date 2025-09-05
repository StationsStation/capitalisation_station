#!/usr/bin/env python

"""
confpick — resolve Git conflict markers non-interactively or per-conflict.

Usage:
  confpick path/to/file                           # list conflicts only
  confpick file --mode ours --in-place            # keep HEAD in all conflicts
  confpick file --mode theirs -o out.yml          # keep incoming in all conflicts
  confpick file --picks 1:ours,3:theirs -o out    # choose per-conflict index
  confpick file --prefer "bafybei" --prefer-side ours --in-place
  confpick file --json                            # machine-readable summary

Conflict markers handled:
  <<<<<<< HEAD
  ... ours ...
  =======
  ... theirs ...
  >>>>>>> <label>
"""
from __future__ import annotations
import argparse
import json
import sys
import textwrap
from dataclasses import dataclass
from typing import List, Optional, Tuple

START = "<<<<<<< "
MID   = "======="
END   = ">>>>>>> "

@dataclass
class Conflict:
    index: int
    start_line: int           # 0-based
    end_line: int             # inclusive
    ours: List[str]
    theirs: List[str]
    head_label: str           # after "<<<<<<< "
    incoming_label: str       # after ">>>>>>> "
    context_preview: str      # first non-empty of ours|theirs trimmed

def parse_conflicts(lines: List[str]) -> List[Conflict]:
    i = 0
    idx = 1
    out: List[Conflict] = []
    n = len(lines)
    while i < n:
        if lines[i].startswith(START):
            head_label = lines[i].strip()[len(START):] or "HEAD"
            i += 1
            ours: List[str] = []
            while i < n and not lines[i].startswith(MID):
                ours.append(lines[i])
                i += 1
            if i >= n or not lines[i].startswith(MID):
                raise ValueError(f"Incomplete conflict: missing '{MID}' near line {i+1}")
            i += 1  # skip MID
            theirs: List[str] = []
            while i < n and not lines[i].startswith(END):
                theirs.append(lines[i])
                i += 1
            if i >= n or not lines[i].startswith(END):
                raise ValueError(f"Incomplete conflict: missing '{END}' near line {i+1}")
            incoming_label = lines[i].strip()[len(END):] or ""
            end_line = i
            # record conflict
            preview = ""
            for block in (ours, theirs):
                for s in block:
                    t = s.strip()
                    if t:
                        preview = (t[:120] + ("…" if len(t) > 120 else ""))
                        break
                if preview:
                    break
            out.append(Conflict(
                index=idx,
                start_line=end_line,  # temporarily store; fixed below
                end_line=end_line,
                ours=ours,
                theirs=theirs,
                head_label=head_label,
                incoming_label=incoming_label,
                context_preview=preview
            ))
            # fix start_line by backtracking length
            total_marker_len = 3  # start, mid, end
            start_line = end_line - (len(ours) + len(theirs) + total_marker_len) + 1
            out[-1].start_line = start_line
            i += 1
            idx += 1
        else:
            i += 1
    return out

def apply_resolution(lines: List[str],
                     conflicts: List[Conflict],
                     default_mode: Optional[str],
                     picks: dict[int, str],
                     prefer_contains: List[str],
                     prefer_side: str) -> Tuple[str, List[int]]:
    removed_spans = []
    # Work on a copy of lines as a mutable list of chars: easier to rebuild by slicing spans
    # We'll rebuild by streaming with a pointer.
    spans = []
    last = 0
    for c in conflicts:
        # choose mode
        mode = picks.get(c.index)
        if mode is None:
            # heuristic prefer
            mode = None
            if prefer_contains:
                ours_text = "".join(c.ours)
                theirs_text = "".join(c.theirs)
                for token in prefer_contains:
                    if prefer_side == "ours" and token in ours_text:
                        mode = "ours"; break
                    if prefer_side == "theirs" and token in theirs_text:
                        mode = "theirs"; break
            if mode is None:
                mode = default_mode
        # determine replacement
        if mode == "ours":
            repl = c.ours
        elif mode == "theirs":
            repl = c.theirs
        elif mode in (None, "keep"):  # leave markers intact
            repl = lines[c.start_line:c.end_line+1]
        else:
            raise ValueError(f"Unknown mode '{mode}' for conflict {c.index}")
        # append span before conflict unchanged
        spans.append(lines[last:c.start_line])
        # append replacement
        spans.append(repl)
        removed_spans.append(c.index)
        last = c.end_line + 1
    # tail
    spans.append(lines[last:])
    resolved = "".join("".join(chunk) for chunk in spans)
    return resolved, removed_spans

def load(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def save(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def list_conflicts(conflicts: List[Conflict], json_out: bool) -> None:
    if json_out:
        data = [{
            "index": c.index,
            "start_line": c.start_line + 1,
            "end_line": c.end_line + 1,
            "head_label": c.head_label,
            "incoming_label": c.incoming_label,
            "preview": c.context_preview
        } for c in conflicts]
        print(json.dumps(data, indent=2))
        return
    if not conflicts:
        print("No conflicts found")
        return
    for c in conflicts:
        print(f"[{c.index}] lines {c.start_line+1}-{c.end_line+1}  head='{c.head_label}'  incoming='{c.incoming_label}'")
        print(f"  preview: {c.context_preview}")

def parse_picks(s: Optional[str]) -> dict[int, str]:
    if not s:
        return {}
    out = {}
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise argparse.ArgumentTypeError(f"Invalid --picks item '{part}', expected N:ours|theirs")
        idx_str, choice = part.split(":", 1)
        try:
            idx = int(idx_str)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid index '{idx_str}' in --picks")
        choice = choice.strip().lower()
        if choice not in ("ours", "theirs"):
            raise argparse.ArgumentTypeError(f"Invalid choice '{choice}' in --picks, use 'ours' or 'theirs'")
        out[idx] = choice
    return out
import os

ALLOWED_EXTS = {".yaml", ".yml", ".json"}
START = "<<<<<<< "
MID   = "======="
END   = ">>>>>>> "

def file_has_conflict_markers(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            seen_start = False
            for line in f:
                if not seen_start and line.startswith(START):
                    seen_start = True
                elif seen_start and line.startswith(MID):
                    # keep scanning to ensure we also see END, but MID is enough to mark as candidate
                    return True
        return False
    except OSError:
        return False

import glob
import os



from pathlib import Path
import glob

ALLOWED_EXTS = {".yaml", ".yml", ".json"}
from pathlib import Path
from typing import Iterator

ALLOWED_EXTS = {".yaml", ".yml", ".json"}

def scan_for_extensions(root: str, extensions: set[str]) -> Iterator[Path]:
    """Recursively yield all files under `root` with suffix in `extensions`."""
    root_path = Path(root)
    if not root_path.is_dir():
        raise NotADirectoryError(root)
    for path in root_path.rglob("*"):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path

def file_has_conflict_markers(path: Path) -> bool:
    """Detect Git conflict markers in a file."""
    try:
        seen_start = False
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if not seen_start and line.startswith("<<<<<<< "):
                    seen_start = True
                elif seen_start and line.startswith("======="):
                    return True
        return False
    except OSError:
        return False

def find_conflicted_files(root: str = ".") -> list[str]:
    """Return all YAML/JSON files under `root` that contain conflict markers."""
    conflicted = []
    for path in scan_for_extensions(root, ALLOWED_EXTS):
        if file_has_conflict_markers(path):
            conflicted.append(str(path.resolve()))
    return sorted(conflicted)



def resolve_file(path: str, *, mode: str, picks: dict[int, str], prefer_tokens: list[str], prefer_side: str) -> tuple[bool, str]:
    """Return (changed, message)."""
    lines = load(path)
    conflicts = parse_conflicts(lines)
    if not conflicts:
        return (False, f"{path}: no conflicts")
    resolved, _ = apply_resolution(
        lines, conflicts,
        default_mode=mode,
        picks=picks,
        prefer_contains=prefer_tokens,
        prefer_side=prefer_side
    )
    save(path, resolved)
    return (True, f"{path}: resolved {len(conflicts)} conflict(s)")

def main():
    ap = argparse.ArgumentParser(
        prog="confpick",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(__doc__ or "")
    )
    ap.add_argument("file", nargs="?", help="Path to conflicted file (omit when using --scan)")
    ap.add_argument("--mode", choices=["ours", "theirs", "keep"], default="ours",
                    help="Default resolution for all conflicts.")
    ap.add_argument("--picks", type=str, default=None,
                    help="Comma-separated per-conflict choices, e.g. '1:ours,3:theirs'")
    ap.add_argument("--prefer", action="append", default=[],
                    help="Token to bias selection toward (--prefer-side decides which side). May be used multiple times.")
    ap.add_argument("--prefer-side", choices=["ours", "theirs"], default="ours",
                    help="Which side to prefer when --prefer token is found")
    ap.add_argument("--in-place", action="store_true", help="Write back to the same file")
    ap.add_argument("-o", "--output", help="Write to this path instead of stdout")
    ap.add_argument("--json", action="store_true", help="Print conflicts as JSON and exit (ignores resolution args)")
    ap.add_argument("--scan", nargs="*", metavar="PATH", default="packages",
                    help="Scan paths for conflicted YAML/JSON and resolve each in place with current options")
    args = ap.parse_args()

    # Batch scan/resolve mode
    if args.scan is not None:
        targets = find_conflicted_files(args.scan)
        if not targets:
            print("No conflicted YAML/JSON files found")
            return
        picks = parse_picks(args.picks)
        for fp in targets:
            changed, msg = resolve_file(
                fp,
                mode=args.mode,
                picks=picks,
                prefer_tokens=args.prefer,
                prefer_side=args.prefer_side
            )
            print(msg)
        return

    # Single-file mode
    if not args.file:
        ap.error("FILE is required unless using --scan")

    lines = load(args.file)
    conflicts = parse_conflicts(lines)

    if args.json or (args.mode is None and not args.picks and not args.prefer and not args.in_place and not args.output):
        list_conflicts(conflicts, json_out=args.json)
        return

    picks = parse_picks(args.picks)
    resolved, _ = apply_resolution(
        lines, conflicts,
        default_mode=args.mode,
        picks=picks,
        prefer_contains=args.prefer,
        prefer_side=args.prefer_side
    )
    if args.in_place:
        save(args.file, resolved)
    elif args.output:
        save(args.output, resolved)
    else:
        sys.stdout.write(resolved)


if __name__ == "__main__":
    main()
