"""Expand %%CHAR:<prefix>%%, %%HALL:<prefix>:<far>%% and %%TALLYJS%% markers in compositions/."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from char import head  # noqa: E402
from hall import TALLY_JS, hall  # noqa: E402

root = pathlib.Path(__file__).resolve().parent.parent / "compositions"
for f in sorted(root.glob("*.html")):
    text = f.read_text()
    new = re.sub(r"%%CHAR:([a-z0-9]+)%%", lambda m: head(m.group(1)), text)
    new = re.sub(r"%%HALL:([a-z0-9]+):([a-z]+)%%", lambda m: hall(m.group(1), m.group(2)), new)
    new = new.replace("%%TALLYJS%%", TALLY_JS)
    if new != text:
        f.write_text(new)
        print("built", f.name)
