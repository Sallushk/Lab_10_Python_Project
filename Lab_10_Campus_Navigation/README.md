# Lab 10 Campus Navigation and Shortest Path Finder

A beginner-friendly terminal application using an undirected, unweighted graph.
Python 3.8 or later is sufficient. No packages or internet connection are needed.

## Run in a terminal or VS Code
1. Extract this ZIP.
2. Open the extracted folder in VS Code.
3. Open Terminal > New Terminal.
4. Run `python main.py` (or `py main.py` on Windows).
5. Enter choices 1 through 10 at the menu.

## Features
1. Display locations in insertion order.
2. Add a location.
3. Connect two locations with a bidirectional pathway.
4. Display the adjacency list.
5. Search using explicit linear search.
6. BFS using a FIFO queue implemented with a list and front index.
7. Iterative DFS using a list as a LIFO stack.
8. Find a route with the fewest pathways using BFS.
9. Alphabetical display using explicit bubble sort.
10. Exit.

Sample map: 7 vertices, 8 undirected edges. It starts fresh each run.
Location matching ignores case and repeated spaces. Names retain their original
capitalization. Empty, nonprintable or over-40-character normalized names are rejected.
Self-loops, duplicate edges and unknown endpoints are rejected.

A route minimizes edge count, not physical distance or travel time.
Tie-breaking follows adjacency-list insertion order. DFS order also depends on
the stack strategy; reversed neighbor insertion visits the first listed neighbor first.

## Sample demonstration
- 4: show the graph.
- 6, Main Gate: BFS traversal.
- 7, Main Gate: DFS traversal.
- 8, Main Gate, Classroom: Main Gate -> Library -> Computer Lab -> Classroom
  (3 pathways).
- 2, Medical Room: add an isolated vertex.
- 8, Main Gate, Medical Room: no route exists.
- 3, Library, Medical Room: connect it; repeat option 8.
- 9: alphabetical locations.
- 10: exit.

## Verification
`python -m unittest -v test_project.py`
`python capture_evidence.py` regenerates the captured sessions.
The evidence directory contains verbatim output from the actual main() function.
Prompts and scripted answers are echoed by the capture harness. These are console
transcripts, not screenshots. The docs identify them as such.

## Syllabus mapping
- Module 1 Unit 1.1: data structures and time/space complexity; Big-O self-learning.
- Module 1 Unit 1.2: applications.
- Module 2 Unit 2.2: stack ADT and operations.
- Module 2 Unit 2.3: queue ADT and applications.
- Module 3 Unit 3.2: graph representation, BFS and DFS.
- Module 4 Unit 4.2: dictionary ADT.
- Module 5 Unit 5.1: bubble sort.
- Module 5 Unit 5.2: linear search.

Python lists implement dynamic sequences, and dictionaries implement the visited
and parent mappings. No Dijkstra, network library, GUI or external dependency is used.

## Files
- main.py: complete application
- test_project.py: 21 automated tests, including all 49 sample endpoint pairs
- capture_evidence.py: reproducible console sessions
- evidence/: real outputs and test results
- diagrams/: campus graph, traversals, route and flowchart
- README.md: this guide

## Upload to GitHub
Create a repository in your GitHub account, add these project files, and commit
them. Copy the resulting repository URL into the report's GitHub placeholder.
For a browser upload, use the repository's file-upload action and select the
extracted files. Use a repository visibility setting permitted by your course.
No repository has been created or published for you.

## Before submission
Fill in all student details, repository URL and actual individual contributions.
The assignment asks for your previous experiment's template; transfer the report
into that template if your college requires an exact format.
Demonstrate and understand the code before submission.
