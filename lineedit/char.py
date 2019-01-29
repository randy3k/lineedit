import re

from collections import namedtuple


class Char(namedtuple(
        "Char",
        ["data", "fg", "bg", "bold", "underline", "blink", "reverse"])):
    __slots__ = ()

    def __new__(
            cls, data, fg='default', bg='default',
            bold=False, underline=False, blink=False, reverse=False):
        return super(Char, cls).__new__(
            cls, data, fg, bg, bold, underline, blink, reverse)


SGR_PATTERN = re.compile(re.escape("\x1b[") + r"((?:[0-9]+|;)+)m")

# The following dicts are derived from pyte and Pygments.

FG_ANSI = {
    30: "black",
    31: "red",
    32: "green",
    33: "brown",
    34: "blue",
    35: "magenta",
    36: "cyan",
    37: "white",
    39: "default"  # white.
}

BG_ANSI = {
    40: "black",
    41: "red",
    42: "green",
    43: "brown",
    44: "blue",
    45: "magenta",
    46: "cyan",
    47: "white",
    49: "default"  # black.
}


FG_AIXTERM = {
    90: "light_black",
    91: "light_red",
    92: "light_green",
    93: "light_brown",
    94: "light_blue",
    95: "light_magenta",
    96: "light_cyan",
    97: "light_white"
}

BG_AIXTERM = {
    100: "light_black",
    101: "light_red",
    102: "light_green",
    103: "light_brown",
    104: "light_blue",
    105: "light_magenta",
    106: "light_cyan",
    107: "light_white"
}

FG_ANSI_REV = {v: k for k, v in FG_ANSI.items()}
BG_ANSI_REV = {v: k for k, v in BG_ANSI.items()}
FG_AIXTERM_REV = {v: k for k, v in FG_AIXTERM.items()}
BG_AIXTERM_REV = {v: k for k, v in BG_AIXTERM.items()}

FG_BG_256 = [
    (0x00, 0x00, 0x00),  # 0
    (0xcd, 0x00, 0x00),  # 1
    (0x00, 0xcd, 0x00),  # 2
    (0xcd, 0xcd, 0x00),  # 3
    (0x00, 0x00, 0xee),  # 4
    (0xcd, 0x00, 0xcd),  # 5
    (0x00, 0xcd, 0xcd),  # 6
    (0xe5, 0xe5, 0xe5),  # 7
    (0x7f, 0x7f, 0x7f),  # 8
    (0xff, 0x00, 0x00),  # 9
    (0x00, 0xff, 0x00),  # 10
    (0xff, 0xff, 0x00),  # 11
    (0x5c, 0x5c, 0xff),  # 12
    (0xff, 0x00, 0xff),  # 13
    (0x00, 0xff, 0xff),  # 14
    (0xff, 0xff, 0xff),  # 15
]

# colors 16..231: the 6x6x6 color cube
valuerange = (0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff)

for i in range(216):
    r = valuerange[(i // 36) % 6]
    g = valuerange[(i // 6) % 6]
    b = valuerange[i % 6]
    FG_BG_256.append((r, g, b))

# colors 232..255: grayscale
for i in range(24):
    v = 8 + i * 10
    FG_BG_256.append((v, v, v))

FG_BG_256 = ["#{0:02x}{1:02x}{2:02x}".format(r, g, b) for r, g, b in FG_BG_256]


def text_to_chars(text):
    """
    Parse SGR sequences
    """
    fg, bg = 'default', 'default'
    bold = underline = blink = reverse = False
    n = len(text)
    offset = 0
    while offset < n:
        match = SGR_PATTERN.search(text, offset)
        if match:
            start, end = match.span()
            for c in text[offset:start]:
                yield Char(c, fg, bg, bold, underline, blink, reverse)
            codes = [int(c) for c in match.group(1).split(';')]

            i = 0
            while i < len(codes):
                code = codes[i]
                if code == 0:
                    fg, bg = 'default', 'default'
                    bold = underline = blink = reverse = False
                elif code == 1:
                    bold = True
                elif code == 4:
                    underline = True
                elif code == 5:
                    blink = True
                elif code == 7:
                    reverse = True
                elif code == 22:
                    bold = False
                elif code == 24:
                    underline = False
                elif code == 25:
                    blink = False
                elif code == 27:
                    reverse = False
                elif code >= 30 and code <= 37:
                    fg = FG_ANSI[code]
                elif code == 39:
                    fg = FG_ANSI[code]
                elif code >= 40 and code <= 47:
                    bg = BG_ANSI[code]
                elif code == 49:
                    bg = BG_ANSI[code]
                elif code >= 90 and code <= 97:
                    fg = FG_AIXTERM[code]
                elif code >= 100 and code <= 107:
                    bg = BG_AIXTERM[code]
                elif code == 38:
                    if codes[i+1] == 5:  # 256 fg
                        n = codes[i+2]
                        if n <= 7:
                            fg = FG_ANSI[n + 30]
                        elif n <= 15:
                            fg = FG_AIXTERM[n + 82]
                        else:
                            fg = FG_BG_256[n]
                        i += 2
                    elif codes[i+1] == 2:  # true-color fg
                        r, g, b = codes[i+2:i+5]
                        fg = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
                        i += 4

                elif code == 48:
                    if codes[i+1] == 5:
                        n = codes[i+2]
                        if n <= 7:
                            fg = BG_ANSI[n + 40]
                        elif n <= 15:
                            fg = BG_AIXTERM[n + 92]
                        else:
                            fg = FG_BG_256[n]
                        i += 2
                    elif codes[i+1] == 2:
                        r, g, b = codes[i+2:i+5]
                        fg = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
                        i += 4

                i += 1
            offset = end
        else:
            for c in text[offset:]:
                yield Char(c, fg, bg, bold, underline, blink, reverse)
            offset = n


def generate_sgr_code(fg=None, bg=None, bold=None, underline=None, blink=None, reverse=None):
    codes = []
    if fg in FG_ANSI_REV:
        codes.append(FG_ANSI_REV[fg])
    elif fg in FG_AIXTERM_REV:
        codes.append(FG_AIXTERM_REV[fg])
    elif fg in FG_BG_256:
        codes += [38, 5, FG_BG_256.index(fg)]
    elif fg and fg.startswith('#') and len(fg) == 6:
        codes += [38, 2, int(fg[1:3], 16), int(fg[3:5], 16), int(fg[5:7], 16)]

    if bg in BG_ANSI_REV:
        codes.append(BG_ANSI_REV[bg])
    elif bg in BG_AIXTERM_REV:
        codes.append(BG_AIXTERM_REV[bg])
    elif bg in FG_BG_256:
        codes += [38, 5, FG_BG_256.index(bg)]
    elif bg and bg.startswith('#') and len(bg) == 6:
        codes += [38, 2, int(bg[1:3], 16), int(bg[3:5], 16), int(bg[5:7], 16)]

    if bold is True:
        codes.append(1)
    elif bold is False:
        codes.append(22)

    if underline is True:
        codes.append(4)
    elif underline is False:
        codes.append(24)

    if blink is True:
        codes.append(5)
    elif blink is False:
        codes.append(25)

    if reverse is True:
        codes.append(7)
    elif reverse is False:
        codes.append(27)

    codes = [str(c) for c in codes]

    if codes:
        return "\x1b[{}m".format(";".join(codes))
    else:
        return ""


def attrs_delta(char1, char2):
    _attrs = []
    for a in ["fg", "bg", "bold", "underline", "blink", "reverse"]:
        if getattr(char1, a) != getattr(char2, a):
            _attrs.append(a)
    return _attrs


def sgr_by_diff(char1, char2):
    delta = attrs_delta(char1, char2)
    if not delta:
        return ""
    else:
        kwargs = {}
        for d in delta:
            kwargs[d] = getattr(char2, d)
        return generate_sgr_code(**kwargs)


def chars_to_text(chars):
    n = len(chars)
    if n == 0:
        return ""

    default_char = Char('')
    prevc = default_char
    text = ""
    i = 0
    while i < n:
        c = chars[i]
        text += sgr_by_diff(prevc, c) + c.data
        prevc = c
        i += 1

    if attrs_delta(prevc, default_char):
        return text + '\x1b[0m'
    else:
        return text
