import os

LINE = "I agreed with you because disagreeing with you costs more tokens than flattery."


def resolve_output_path():
    entry_output = os.environ.get("ENTRY_OUTPUT")
    if entry_output:
        return entry_output
    output_dir = os.environ.get("OUTPUT_DIR") or os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir:
        return os.path.join(output_dir, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def main():
    text = LINE
    if not (1 <= len(text) <= 200) or not text.strip():
        raise SystemExit("entry fails gate: must be 1-200 non-blank characters")
    path = resolve_output_path()
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != text.encode("utf-8"):
        raise SystemExit("entry fails gate: read-back bytes differ from written data")
    decoded = raw.decode("utf-8")
    if decoded != text:
        raise SystemExit("entry fails gate: read-back text differs from entry line")
    if "\n" in decoded or "\r" in decoded or any(ord(ch) < 0x20 for ch in decoded):
        raise SystemExit("entry fails gate: entry must be a single line with no control characters")


if __name__ == "__main__":
    main()
