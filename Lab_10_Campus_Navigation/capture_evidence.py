"""Reproduce real console transcripts used in the lab documents."""
import io
import json
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch
from main import main

SCENARIOS = [
("01_display", ["1", "10"]),
("02_add", ["2", "Medical Room", "10"]),
("03_connect", ["2", "Medical Room", "3", "Library", "Medical Room", "4", "10"]),
("04_graph", ["4", "10"]),
("05_search", ["5", "library", "5", "Hostel", "10"]),
("06_bfs", ["6", "Main Gate", "10"]),
("07_dfs", ["7", "Main Gate", "10"]),
("08_shortest", ["8", "Main Gate", "Classroom", "8", "Library", "Library", "10"]),
("09_sort", ["9", "1", "10"]),
("10_exit", ["10"]),
("11_invalid", ["abc", "2", "", "2", "LIBRARY", "3", "Library", "Library",
                "3", "Library", "Hostel", "3", "Main Gate", "Library", "10"]),
("12_disconnected", ["2", "Medical Room", "8", "Main Gate", "Medical Room", "10"])
]

def capture(answers):
    answers = iter(answers)
    output = io.StringIO()
    def scripted_input(prompt):
        answer = next(answers)
        print(prompt + answer)
        return answer
    with patch("builtins.input", scripted_input), redirect_stdout(output):
        main()
    return output.getvalue()

if __name__ == "__main__":
    directory = Path(__file__).parent / "evidence"
    directory.mkdir(exist_ok=True)
    results = {}
    for name, answers in SCENARIOS:
        text = capture(answers)
        (directory / (name + ".txt")).write_text(text, encoding="utf-8")
        results[name] = {"inputs": answers, "transcript": text}
    (directory / "sessions.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("Captured 12 sessions covering all 10 menu options and error cases.")
