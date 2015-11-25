import os
import sys
sys.path[0] = sys.path[0][:-13]
import subprocess
import _profile

def main():
    print("Save tests...")
    try:
        test_profile = _profile.Profile(name="test_profile")
    except:
        print("ERROR: Could not initialize TEST 1!")
        sys.exit(1)
    s = "TEST 1..."
    try:
        test_profile.save()
        test_profile = _profile.Profile(name="test_profile", load_from_file=True)
    except:
        s += "FAILED!"
    else:
        s += "PASSED"
    print(s + "\n")
    subprocess.call(["rm", os.path.join("profiles", "test_profile")])

if __name__ == "__main__":
    main()
