#!/usr/bin/env python3
import re
import os
import sys

IRREGULARS = {
    "children": ("child", "PL"),
    "men": ("man", "PL"),
    "women": ("woman", "PL"),
    "people": ("person", "PL"),
    "mice": ("mouse", "PL"),
    "geese": ("goose", "PL"),
    "teeth": ("tooth", "PL"),
    "feet": ("foot", "PL"),
    "oxen": ("ox", "PL"),
    
}

VOWELS = set("aeiou")

WORD_RE = re.compile(r"^[a-z]+$") 

def load_words(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    tokens = [t.strip().lower() for t in re.split(r"\s+", text) if t.strip()]
    tokens = [t for t in tokens if WORD_RE.match(t)]
    return sorted(set(tokens))


def build_candidate_roots(all_words):
    all_set = set(all_words)
    roots = set()

    for w in all_words:
        if not w.endswith("s"):
            roots.add(w)

    for w in all_words:
        if w.endswith("ies"):
            cand = w[:-3] + "y"
            if cand in all_set:
                roots.add(cand)
        if w.endswith("es"):
            cand = w[:-2]
            if cand in all_set:
                roots.add(cand)
        if w.endswith("s"):
            cand = w[:-1]
            if cand in all_set:
                roots.add(cand)

 
    for surf, (root, num) in IRREGULARS.items():
        roots.add(root)

    return roots


def analyze_word(w, roots):
    w = w.lower().strip()
    if not w or not WORD_RE.match(w):
        return "Invalid Word"

    if w in IRREGULARS:
        root, num = IRREGULARS[w]
        return f"{root}+N+{num}"


    if w in roots:
        return f"{w}+N+SG"

    
    if w.endswith("ies"):
        stem = w[:-3]
        if not stem:
            return "Invalid Word"
        
        root = stem + "y"
        
        if stem and (stem[-1] not in VOWELS):
            if root in roots:
                return f"{root}+N+PL"
        return "Invalid Word"

   
    if w.endswith("es"):
        root_candidate = w[:-2]
        if not root_candidate:
            return "Invalid Word"
        if (root_candidate.endswith(("ch", "sh"))
            or (root_candidate and root_candidate[-1] in ("s", "z", "x"))):
            if root_candidate in roots:
                return f"{root_candidate}+N+PL"
        return "Invalid Word"


    if w.endswith("s"):
        root_candidate = w[:-1]
        if not root_candidate:
            return "Invalid Word"

        
        if root_candidate.endswith(("ch", "sh")) or (root_candidate and root_candidate[-1] in ("s", "z", "x")):
            return "Invalid Word"

        
        if root_candidate.endswith("y"):
            if len(root_candidate) >= 2 and root_candidate[-2] in VOWELS:
                if root_candidate in roots:
                    return f"{root_candidate}+N+PL"
                return "Invalid Word"
            else:
                return "Invalid Word"

        
        if root_candidate in roots:
            return f"{root_candidate}+N+PL"

        return "Invalid Word"

    
    return "Invalid Word"


def process_corpus(infile="brown_nouns.txt", outfile="brown_nouns_morphs.txt"):
    if not os.path.exists(infile):
        print(f"ERROR: input file '{infile}' not found.", file=sys.stderr)
        return

    words = load_words(infile)
    roots = build_candidate_roots(words)

    results = {}
    for w in sorted(words):
        results[w] = analyze_word(w, roots)

    
    with open(outfile, "w", encoding="utf-8") as out:
        for w in sorted(results.keys()):
            out.write(f"{w} = {results[w]}\n")

    print(f"Done. Results written to {outfile}")
    
    sample = ["fox", "foxes", "foxs", "try", "bus", "busss", "boys", "watch", "watches"]
    print("\nSample outputs:")
    for s in sample:
        print(f"{s} -> {analyze_word(s, roots)}")



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="FST analyzer for brown_nouns")
    parser.add_argument("inpath", nargs="?", default="brown_nouns.txt",
                        help="Input file (default: brown_nouns.txt)")
    parser.add_argument("outpath", nargs="?", default="brown_nouns_morphs.txt",
                        help="Output file (default: brown_nouns_morphs.txt)")

    args, unknown = parser.parse_known_args()

    inpath = args.inpath
    outpath = args.outpath

   
    process_corpus(infile=inpath, outfile=outpath)