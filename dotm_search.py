#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import zipfile
parser = argparse.ArgumentParser()


"""
Given a directory path, search all files in the path for a given text string
within the 'word/document.xml' section of a MSWord .dotm file.
"""
__author__ = "knmarvel"
#   time spent on this project: 2 hrs


def examine_files(directory, character):
    files = {}
    print(len(os.listdir(directory)))
    total_files_searched = 0
    for filename in os.listdir(directory):
        filepath = directory + "/" + filename
        if zipfile.is_zipfile(filepath):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall("./extracted")
            with open('./extracted/word/document.xml', "r") as words:
                words = words.read()
            if "office/word" in words:
                total_files_searched += 1
                if character in words:
                    files[filename] = words[words.index(character) - 40: words.index(character) + 40]
    print("Number of files searched: " + str(total_files_searched))
    print("Number of files found: " + str(len(files)))
    print("\n".join([": ".join([x, files[x]]) for x in files]))
    return ("; ".join([": ".join([x, files[x]]) for x in files]))


def main():
    parser.add_argument('--dir', help='directory to find data',
                        type=str, default='--dir')
    parser.add_argument('--char',
                        help="the character you want to search for",
                        type=str,
                        default="$")
    args = parser.parse_args()
    return examine_files(args.dir, args.char)


if __name__ == '__main__':
    main()
