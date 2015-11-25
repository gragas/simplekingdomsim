import sys
sys.path[0] = sys.path[0][:-13]
import _profile

def main():
    print("Constructor (with only loading) tests...")
    try:
        test_profile = _profile.Profile(name="test_profile")
        test_profile.save()
    except:
        print("ERROR: Could not initialize TEST 1!")
        sys.exit(1)
    s = "TEST 1..."
    try:
        test_profile = _profile.Profile(name="test_profile", load_from_file=True)
    except:
        s += "FAILED!"
    else:
        s += "PASSED"
    print(s + "\n")

if __name__ == "__main__":
    main()
