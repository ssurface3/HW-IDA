# -*- coding: utf-8 -*-
"""
Ths file contains script to generate individual dataset for students homework.
File energydata.txt.zip must be in the working directory. Otherwise change
file name attribute in the first row of script (row 72).
File must be tab separated. Otherwise please change corresponding parameter in
function readSource.

To generate dataset please put your ID into variable ID in the third line of
script (row 80).

The result is written to Diabetes_<your ID>.txt in the working directory.

Created on Sun Sep 27 10:38:18 2026

@author: E.Mirkes
"""
# pylint: disable=C0103

import os
import io
import csv
import random as rnd
import zipfile
from zlib import crc32


def readSource(zName, fName):
    '''
    This function read zip file fith original database to extract individual
    subset for each user.

    Parameters
    ----------
    zName : str
        Name of zip file with original database.
    fName : str
        Name of file with original database in zip file.

    Raises
    ------
    ValueError
        Zip File with specified name must be in the working directory..

    Returns
    -------
    lines : list of lists
        Each elenemt of main list is row (record, observation).
        Each element of the second level list is value of the field.
        The first element of the main list contains list of field names.

    '''
    if not os.path.isfile(zName):
        raise ValueError("There is no source file.")
    lines = []
    with zipfile.ZipFile(zName, 'r') as archive:
        # open() returns a binary file handle
        with archive.open(fName) as binary_file:
            # Wrap it to read as text line-by-line
            with io.TextIOWrapper(binary_file, encoding='utf-8') as text_file:
                for line in text_file:
                    lines.append(line.strip().split(','))
    # Convert data to required format
    for lind, line in enumerate(lines):
        for find, f in enumerate(line):
            line[find] = f[1:-1].strip();
        lines[lind]=line[1:]
            
    return lines

# Script itself
data = readSource("energydata.txt.zip", "energydata.txt")
# Extract header
head = data[0]
data = data[1:]
nFields = len(head) - 1

# Enter your ID

ID = 'EVGENY.MIRKES'

# Number of cases for dataset
nCases = 10000

seed = 0

# Convert ID into number
seed = crc32(ID.encode())

# Initialise random number generator
rnd.seed(seed)

# select required number of records
dat = rnd.sample(data, nCases)
dat.insert(0, head)

# Required fraction of gaps
nGaps = round(0.05 * nCases * nFields)

# Loop for gaps to produce gaps
for k in range(nGaps):
    while True:
        row = rnd.randint(1, nCases)
        col = rnd.randint(1, nFields)
        if dat[row][col] != "":
            break
    dat[row][col] = ""

# Required number of surprises
nGaps = round(0.01 * nCases * nFields)

# Loop for gaps to produce gaps
for k in range(nGaps):
    while True:
        row = rnd.randint(1, nCases)
        col = rnd.randint(1, nFields)
        if dat[row][col] != "":
            break
    match col:
        case 15 | 16:
            dat[row][col] = "31"
        case 14 | 19 | 20 | 21:
            dat[row][col] = "0"
        case _:
            dat[row][col] = "-1"

# Write result! The ID forms part of the file name so that a submitted file can
# be traced back to the student it was generated for. Anything that is not a
# letter, digit, dot, underscore or hyphen becomes an underscore, because some
# of those characters are not allowed in file names.
safeID = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in ID)
outName = f"Energy{safeID}.txt"

with open(outName, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter="\t")

    # Write line by line using a loop
    for row in dat:
        writer.writerow(row)

print(f"Data generated for {ID}: {nCases} rows")
print(f"Written to {outName}")
