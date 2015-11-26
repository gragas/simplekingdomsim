import os
import sys
import subprocess

def main():
    print()
    test_folders = set()
    args = sys.argv
    if len(args) > 1:
        test_folders = set([os.path.join("tests", arg) for arg in args[1:]])
    if not test_folders:
        test_folders = next(os.walk("tests"))[1]
        test_folders = [os.path.join("tests", folder) for folder in test_folders]
        test_folders = set(test_folders)
    for folder in test_folders:
        print("{} tests...\n{}".format(folder, "="*20))
        tests = set([os.path.join(folder, fn) for fn in next(os.walk(folder))[2]])
        for test in tests:
            subprocess.call(["python3", test,])

if __name__ == "__main__":
    main()
