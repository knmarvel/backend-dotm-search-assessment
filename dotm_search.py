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


def examine_files(dir, char):
    files = {}
    total_files_searched = 0
    for filename in os.listdir(dir):
        filepath = dir + "/" + filename
        if zipfile.is_zipfile(filepath):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall("./extracted")
            with open('./extracted/word/document.xml', "r") as doc:
                doc = doc.read()
            if "office/word" in doc:
                total_files_searched += 1
                if char in doc:
                    files[filename] = doc[doc.index(char) - 40: doc.index(char) + 40]
    f_srched = "# of files searched: " + str(total_files_searched)
    f_fnd = "# of files found:" + str(len(files))
    f = "\n".join([": ".join([filename, files[filename]]) for filename in files])
    return (f_srched + "\n" + f_fnd + "\n" + f)


def parsing():
    parser.add_argument('--dir', help='directory of files to search',
                        type=str, default='./dotm_files')
    parser.add_argument('--char',
                        help="the character you want to search for",
                        type=str,
                        default="$")
    return parser.parse_args()


def main():
    args = parsing()
    ans = examine_files(args.dir, args.char)
    print(ans)
    return ans


if __name__ == '__main__':
    main()
