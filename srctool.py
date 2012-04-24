#!/usr/bin/python
#
# srctool
#
# A tool to ease management of srcds.
# -jimbru
#

from argparse import ArgumentParser
import os
import os.path
from shutil import move
from subprocess import Popen, PIPE


def install(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

    proc = Popen("./hldsupdatetool.bin", stdin=PIPE, stdout=PIPE, stderr=PIPE)
    proc.communicate("yes")
    proc.wait()
    if proc.returncode != 0:
        print "Error: hldsupdatetool.bin exited abnormally"
        exit(proc.returncode)

    move("readme.txt", os.path.join(dir, "srcds_readme.txt"))
    steam_path = os.path.join(dir, "steam")
    move("steam", steam_path)

    cmd = [steam_path, "-command", "update", "-game", "Counter-Strike Source",
           "-dir", dir]
    limit = 3

    for i in range(limit):
        proc = Popen(cmd, stdin=PIPE)
        proc.wait()
        if proc.returncode == 0:
            break
        elif i == limit - 1:
            print "Error: steam update failed after %d retries" % limit
            exit(proc.returncode)

    print "Install complete."


def main():
    parser = ArgumentParser("srctool")
    parser.add_argument("action", help="action to take")
    parser.add_argument("-d", "--dir", default="srcds", help="install directory")
    args = parser.parse_args()

    if args.action == "install":
        install(args.dir)
    else:
        print "Unrecognized action. Exiting..."


if __name__ == "__main__":
    main()
