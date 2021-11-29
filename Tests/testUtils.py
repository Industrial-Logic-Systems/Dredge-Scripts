import difflib


def is_equal(expected, actual, isFile=False):
    if isFile:
        with open(expected, "r") as f:
            expected = f.read()
        with open(actual, "r") as f:
            actual = f.read()
    if expected == actual:
        return (True, "")
    expected = expected.splitlines()
    actual = actual.splitlines()
    diff = difflib.unified_diff(expected, actual, fromfile="expected", tofile="actual")
    diff = "\n".join(diff)
    if diff == "":
        return (True, "")
    else:
        return (False, diff)


if __name__ == "__main__":
    result = is_equal("Tests/test1.txt", "Tests/test2.txt", True)
    print(result[0], result[1])
