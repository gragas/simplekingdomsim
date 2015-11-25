import sys
sys.path[0] = sys.path[0][:-13]
import _profile

def main():
    print("Constructor (without loading) tests...")
    s = "TEST 1..."
    try:
        test_profile = _profile.Profile(name="test_profile")
    except:
        s += "FAILED!"
    else:
        s += "PASSED"
    print(s + "\n")

if __name__ == "__main__":
    main()
