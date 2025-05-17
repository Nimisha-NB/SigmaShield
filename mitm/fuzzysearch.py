from rapidfuzz import fuzz
from pathlib import Path
import os

def fuzzy_search_in_file(file_path, target_snippet, min_score=60):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        full_code = f.read()

    target_snippet = target_snippet.strip()
    best_score = 0
    best_match = ""
    best_index = -1

    code_lines = full_code.splitlines()
    snippet_lines = target_snippet.splitlines()
    snippet_len = len(snippet_lines)

    for i in range(len(code_lines) - snippet_len + 1):
        window = "\n".join(code_lines[i:i + snippet_len])
        score = fuzz.ratio(window.strip(), target_snippet)
        if score > best_score:
            best_score = score
            best_match = window
            best_index = i

    if best_score >= min_score:
        print(f"\n✅ Match found in file: {file_path}")
        print(f"📌 Match (score: {best_score}) starting at line {best_index + 1}:\n")
        print(best_match)
        return True  # Signal to stop further search

    return False  # No good match in this file

def fuzzy_search_in_folder(folder_path, target_snippet, min_score=60):
    folder = Path(folder_path)

    for file_path in folder.rglob("*.py"):
        found = fuzzy_search_in_file(file_path, target_snippet, min_score)
        if found:
            return  # Early return on first match

    print("❌ No matching code snippet found in any file.")

# 🧪 Example usage
fuzzy_search_in_folder(
    os.getcwd(),  # <- 🔁 Replace with your actual folder path
    """
def block(self, flow: http.HTTPFlow, reason: str):
    print(f"{reason} Blocking request to {flow.request.url}.")
    flow.response = http.Response.make(
        403,
        b"Request blocked: " + reason.encode(),
        {"Content-Type": "text/plain"}
    )
    """,
    min_score=70
)