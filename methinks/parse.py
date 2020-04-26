import re


# Match sections from a methinks entry
# A title is any markdown style header
# Content is any text included on the next line after header
# Until you meet next header or end of file (\Z)
# (?P<name>...) Captures content in parentheses as attr name
# (?=...) Is a lookahead that checks content but doesn't consume input
RE_SPLIT_SECTIONS = r'(?P<section>^#+(?P<title>.*?)\n(?P<content>.*?))(?=^#|\Z)'


def parse_sections(text, triggers):

    reg = re.compile(RE_SPLIT_SECTIONS, re.MULTILINE | re.DOTALL)

    sections = []
    for match in reg.finditer(text):
        section, title = match['section'], match['title']
        title = title.strip()
        sec = triggers[title].from_text(section)
        sections.append(sec.propagate())
    return sections
