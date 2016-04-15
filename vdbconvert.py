#!/usr/bin/env python3

#
# vdbsetup.py - script for building Vdbench configurations
#
# Author: Ramon A. Lovato (ramonalovato.com)
# For: DeepStorage, LLC (deepstorage.net)
#

import argparse
import re
import csv

def getArgs():
    parser = argparse.ArgumentParser(
        description='convert Vdbench "flatfile.html" output files into CSVs')

    # Positional
    parser.add_argument("inPath", type=str,
        help="where to find the input file")
    parser.add_argument("outPath", type=str,
        help="where to save the output file")

    return parser.parse_args()

def parseInput(inFile):
    f = filter(lambda x: not x.isspace() and not re.match(r"^[<>\*]", x),
        inFile.readlines())
    lines = [re.split(r"\s+(?=\S)", x.strip()) for x in f]
    isAveLam = lambda x: len(x) > 2 and re.match(r"^avg_\S+", x[2])

    # Move averages to end.
    averages = []
    i = 0
    iMax = len(lines)
    while i < iMax:
        if isAveLam(lines[i]):
            averages.append(lines.pop(i))
            iMax -= 1
        else:
            i += 1

    return lines + [[], ["--- Averages ---"]] + averages

def buildOutput(lines, outFile):
    outWriter = csv.writer(outFile)
    outWriter.writerows(lines)

# Main.
def main():
    args = getArgs()

    with open(args.inPath, "r") as inFile, open(args.outPath, "w", newline="") as outFile:
        lines = parseInput(inFile)
        buildOutput(lines, outFile)

if __name__ == "__main__":
    main()