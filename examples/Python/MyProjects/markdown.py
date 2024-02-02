import sys
from PyQt6.QtWidgets import QApplication, QTextEdit

text = """
# Markdown Demo
## This is heading 2
Markdown text can be easily displayed in a `QTextEdit` widget
using the `QTextEdit::setMarkdown()` function call.

This is *italic text*, while this is **bold text** and
this is _underlined text_.

Here is a bulleted list:
* Bullet item 1
* Bullet item 2

And this is a numbered list
1. First item
2. Second item

Here is some Python code:
```python
import os

print(f"Hello World! You are working in {os.getcwd()} directory")

```


This is a link to the [Google Gemini Documentation](https://ai.google.dev/docs), but I 
am unable to click through :(.
"""

app = QApplication(sys.argv)
app.setStyle("Fusion")

markdown_viewer = QTextEdit()
markdown_viewer.setReadOnly(True)
markdown_viewer.setMarkdown(text)
markdown_viewer.setMinimumSize(640, 480)
markdown_viewer.show()

sys.exit(app.exec())
