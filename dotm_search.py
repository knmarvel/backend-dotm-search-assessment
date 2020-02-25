#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import sys
import zipfile

""" Check that the current python version is python3 """
if sys.version_info[0] < 3:
    raise Exception("This program requires python3 interpreter")


__author__ = "Janell.Huyck with help from madarp and knmarvel"


def parse_arguments():
    """ Require and get the arguments passed in on the command line
    when the program is called."""

    parser = argparse.ArgumentParser()
    parser.add_argument('search_text', action="store")
    parser.add_argument('--dir', "-d", action="store",
                        default=os.getcwd())
    result = parser.parse_args()

    return result


def select_dotm_files(search_directory):
    """ Return a list of all files with the suffix .dotm"""

    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(search_directory):
        for filename in filenames:
            if filename.endswith(".dotm"):
                file_list.append(os.path.join(dirpath, filename))
    return file_list


def perform_search(search_directory, search_text):
    """Extract zip files and search them for the search_text.
    Print search results to screen"""

    file_list = select_dotm_files(search_directory)
    match_count = 0

    for file in file_list:
        with zipfile.ZipFile(file, 'r') as zip_files:
            zip_files.extractall("./extracted")
        with open('./extracted/word/document.xml', "r") as words:
            words = words.read()

        search_context = find_search_context(words, search_text)
        if search_context != "-1":
            print("Match found in: ", file)
            print("Context is: ", search_context)
            match_count += 1

    print("Number of files searched: ", len(file_list))
    print('Found {} files with "{}".'.format(match_count, search_text))


def find_search_context(file_data, search_text):
    """Return a string of approximately 40 characters on either side of the
    searched text.  Account for if the searched text is near either end of
    the file."""

    search_index = file_data.find(search_text)

    if search_index == -1:
        return '-1'

    end_slice = min([len(file_data), search_index + 40])

    if search_index < 40:
        return file_data[0:end_slice]
    else:
        return file_data[search_index - 40: end_slice]


def main():
    """Print to the terminal a list of all files and an excerpt from them
    for a given directory (default = cwd) and search term."""

    search_terms = parse_arguments()
    search_text = search_terms.search_text
    search_directory = search_terms.dir
    perform_search(search_directory, search_text)


if __name__ == '__main__':
    main()
