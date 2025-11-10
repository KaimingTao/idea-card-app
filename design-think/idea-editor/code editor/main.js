const editor = document.getElementById("editor");
const preview = document.getElementById("preview");

editor.addEventListener("keydown", (e) => {
  const start = editor.selectionStart;
  const end = editor.selectionEnd;

  // Handle Tab for indentation
  if (e.key === "Tab") {
    e.preventDefault();
    const indent = "  "; // 2 spaces (or use "\t" for a real tab)
    editor.value = editor.value.substring(0, start) + indent + editor.value.substring(end);
    editor.selectionStart = editor.selectionEnd = start + indent.length;
  }

  // Handle Enter for auto-indent
  if (e.key === "Enter") {
    e.preventDefault();

    // Get current line
    const value = editor.value;
    const lineStart = value.lastIndexOf("\n", start - 1) + 1;
    const line = value.slice(lineStart, start);

    // Match leading whitespace
    const indentMatch = line.match(/^\s*/);
    const indent = indentMatch ? indentMatch[0] : "";

    // Insert newline + indent
    const insert = "\n" + indent;
    editor.value = value.substring(0, start) + insert + value.substring(end);
    editor.selectionStart = editor.selectionEnd = start + insert.length;
  }
});

// Live preview
editor.addEventListener("input", () => {
  preview.srcdoc = editor.value;
});

// Optional: Initialize with sample code
editor.value = `<ul>\n  <li>Hello</li>\n</ul>`;
preview.srcdoc = editor.value;
