#!/usr/bin/env python3
import sys
import os
import re

exclude_patterns = []
include_patterns = []


def match_patterns(path, patterns):
    if path != "" and path != "\n" and path != " ":
        for pat in patterns:
            if pat == "" or pat == "\n":
                continue
            try:
                if re.match(pat, path):
                    return pat
            except:
                print("\nPattern: " + pat + "\n")
                raise ValueError
    return None

def save_patterns(include_lst, exclude_lst, include_patterns, exclude_patterns):
    file1 = open(include_lst, "r")
    tmp = file1.readlines()
    for i in tmp:
        if not re.match("^#", i):
            include_patterns.append(i.strip("\n"))
    try:
        include_patterns.remove("")
    except:
        pass
    file2 = open(exclude_lst, "r")
    tmp2 = file2.readlines()
    for j in tmp2:
        if not re.match("^#", j):
            exclude_patterns.append(j.strip("\n"))
    try:
        exclude_patterns.remove("")
    except:
        pass

def backup(src, dst, inc, exc):
    print(inc, exc)
    print(sys.argv[0] + " will perfom backup on " + src + "\nDestination: " + dst + "\n")
    files_to_ignore = []
    if src[-1] == '/':
        prefix = src
    else:
        prefix = src + '/'
    for directory in os.walk(src):
        for i in os.listdir(directory[0]):
            if directory[0][-1] == '/':
                current = directory[0] + i
            else:
                current = directory[0] + '/' + i
            offset = len(prefix)
            if current == "." or current[offset:] == ".." or current[offset:].strip(" ").strip("\n") == "":
                continue
            else:
                pat_exc = None
                pat_exc = match_patterns(current[offset:], exc)
                if pat_exc == None:
                    pat_inc = None
                    pat_inc = match_patterns(current[offset:], inc)
                    if pat_inc != None:
                        print("File: " + current[offset:])
                        print("Match: " + pat_inc)
                    else:
                        files_to_ignore.append(current[offset:])
                else:
                    print("File: " + current[offset:])
                    print("Unmatch: " + pat_exc)
                    files_to_ignore.append(current[offset:])
    print("\nRecap:")
    try:
        os.remove("files_list.txt")
    except:
        pass
    file_out = open("files_list.txt", "w")
    for k in files_to_ignore:
        print(k)
        file_out.writelines(k + "\n")


if __name__ == '__main__':
    print("\nBackup UNIX\n")
    if len(sys.argv) != 3:
        print(sys.argv[0] + ": src dst")
        sys.exit(1)
    else:
        save_patterns("backup.txt", "ignore.txt", include_patterns, exclude_patterns)
        backup(sys.argv[1], sys.argv[2], include_patterns, exclude_patterns)
