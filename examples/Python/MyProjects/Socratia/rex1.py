"""rex1.py - using regular expressions """
import re

names = [
    "Finn Bindeballe",
    "Geir Anders Berge",
    "HappyCodingRobot",
    "Ron Cromberge",
    "Sohil",
]

# find all people with just a single first & last name
regex = r"^\w+\s+\w+$"
for name in names:
    if re.search(regex, name):
        print(name)

# find all names for word char sequence starting with C
regex = r"C\w*"  # C followed by 0 or more word chars
for name in names:
    match = re.search(regex, name)
    if match:
        print(name)
        print(
            f"Match -> start: {match.start()} - end: {match.end()} - same as: {match.span()}"
        )
        print(f"   and this is the substring that matched: {match.group()}")
