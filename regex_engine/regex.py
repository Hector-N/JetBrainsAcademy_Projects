import sys
sys.setrecursionlimit(20000)


def char(re, ch):
    """
    Match single character with 'dot' metacharacter.

    :param re: str, len <= 1, metacharacter
    :param ch: str, len <= 1, searched character
    """
    if len(re) > 1 or len(ch) > 1:
        raise ValueError("Args to 'char()' must be of 0 or 1 length")

    if not re:
        return True
    elif not ch:
        if re in ('', '*', '+', '?'):
            return True
        return False
    elif re == '.' and ch:
        return True
    else:
        if re == ch:
            return True
        return False


def string(re, st):
    """
    Compare equal length strings.
    Supports ?, *, + metacharacters.
    Supports matching metacharacter by escaping it with \.

    :param re: str, regular expression
    :param st: str, string to match with 're'
    """

    sl = None
    if re[0:1] == '\\':  # \
        re = re[1:]
        sl = True

    if not re:
        return True
    elif re and not st:
        if re == '$':
            return True
        return False
    elif sl:
        if not char(re[0], st[0]):
            return False
        else:
            return string(re[1:], st[1:])
    elif len(re) >= 2 and re[1] == '?':  # ?
        if not char(re[0], st[0:1]):
            return string(re[2:], st)
        else:
            return string(re[2:], st[1:])
    elif len(re) >= 2 and re[1] == '*':  # *
        if not char(re[0], st[0:1]):
            return string(re[2:], st)
        else:
            if len(st) == 1:
                return True
            else:
                return string(re, st[1:])
    elif len(re) >= 2 and re[1] == '+':  # +
        if char(re[0], st[0:1]):
            if len(st) == 1:
                return True
            elif st[0] == st[1]:
                return string(re, st[1:])
            else:
                return string(re[2:], st[1:])
    elif not char(re[0], st[0]):
        return False
    else:
        return string(re[1:], st[1:])


def match(re, st):
    """
    Match strings of different lengths.
    """
    # sl = None
    # if re[0:2] == '\\':  # \
    #     re = re[1:]
    #     sl = True

    if len(re) == 0:
        return True
    if re.startswith('^'):
        if char(re[1], st[0]):
            return string(re[1:], st)
    for i, v in enumerate(st):
        if string(re, st[i:]):
            return True
    return False


if __name__ == '__main__':
    while True:
        re, inp = input("Regex engine support ., *, ?, +, $, ^, \\ metacharacters.\n"
                        "Enter regex and string to match, separated with blank, example: colou?r color: \n").split()
        m = match(re, inp)
        if m:
            print(f"{re} - {inp} -> ++Match++")
        else:
            print(f"{re} - {inp} -> --Mismatch--")
        print()

# re, inp = input().split('|')
# print(match(re, inp))
