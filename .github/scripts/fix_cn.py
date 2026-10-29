#!/usr/bin/env python3
"""Remove international WorkBuddy / CodeBuddy domains from the cn geosite list.

These domains serve the international product line and must not be treated as
mainland-China destinations by the routing rules. The upstream cn list is
regenerated on every build, so this script is applied as a post-processing step
inside the workflow instead of editing the generated files by hand.
"""
import json
import sys

TARGETS = {
    "codebuddy.ai",
    "codebuddy.info",
    "codebuddy.net",
    "codebuddy.pro",
    "codebuddy.work",
    "workbuddy.ai",
    "workbuddy.host",
    "workbuddy.link",
}
KEYS = ("domain", "domain_suffix", "domain_keyword", "domain_regex")


def main(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    removed = []
    for rule in data.get("rules", []):
        for key in KEYS:
            values = rule.get(key)
            if not isinstance(values, list):
                continue
            kept = [v for v in values if v not in TARGETS]
            removed.extend(v for v in values if v in TARGETS)
            rule[key] = kept

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))

    removed = sorted(set(removed))
    if removed:
        print("removed %d entries: %s" % (len(removed), ", ".join(removed)))
    else:
        print("::warning::no target domains found in %s (upstream list may have changed)" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
