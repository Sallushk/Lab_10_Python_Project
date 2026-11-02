"""Run with python -m unittest -v test_project.py."""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from main import CampusGraph, Queue, create_sample_campus, main

BFS = ["Main Gate", "Library", "Canteen", "Computer Lab", "Auditorium", "Classroom", "Playground"]
DFS = ["Main Gate", "Library", "Computer Lab", "Classroom", "Playground", "Auditorium", "Canteen"]

class CampusTests(unittest.TestCase):
    def setUp(self):
        self.campus = create_sample_campus()

    def test_initial_graph(self):
        self.assertEqual(len(self.campus.graph), 7)
        self.assertEqual(sum(map(len, self.campus.graph.values())), 16)

    def test_undirected_edges(self):
        for first, neighbors in self.campus.graph.items():
            for second in neighbors:
                self.assertIn(first, self.campus.graph[second])

    def test_queue_fifo(self):
        queue = Queue()
        queue.enqueue("A")
        queue.enqueue("B")
        self.assertEqual(queue.dequeue(), "A")
        self.assertEqual(queue.dequeue(), "B")
        self.assertTrue(queue.is_empty())
        with self.assertRaises(IndexError):
            queue.dequeue()

    def test_add_and_normalize(self):
        self.assertEqual(self.campus.add_location("  Medical   Room "), "Medical Room")
        self.assertEqual(self.campus.graph["Medical Room"], [])

    def test_duplicate_location(self):
        with self.assertRaises(ValueError):
            self.campus.add_location("  LIBRARY ")

    def test_invalid_names(self):
        for name in ("  ", "A" * 41, "Bad\x00name"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.campus.add_location(name)

    def test_linear_search(self):
        self.assertEqual(self.campus.find_location(" computer   LAB "), "Computer Lab")
        self.assertIsNone(self.campus.find_location("Hostel"))

    def test_connect(self):
        self.campus.add_location("Medical Room")
        self.campus.connect_locations("medical room", "library")
        self.assertEqual(self.campus.graph["Medical Room"], ["Library"])
        self.assertIn("Medical Room", self.campus.graph["Library"])

    def test_invalid_connections(self):
        for pair in (("Library", "Hostel"), ("Library", "Library"), ("Library", "Main Gate")):
            with self.subTest(pair=pair), self.assertRaises(ValueError):
                self.campus.connect_locations(*pair)

    def test_bfs_order(self):
        self.assertEqual(self.campus.bfs("Main Gate"), BFS)

    def test_dfs_order(self):
        self.assertEqual(self.campus.dfs("Main Gate"), DFS)

    def test_shortest_route(self):
        self.assertEqual(self.campus.shortest_path("Main Gate", "Classroom"),
                         ["Main Gate", "Library", "Computer Lab", "Classroom"])

    def test_same_start_end(self):
        self.assertEqual(self.campus.shortest_path("library", "Library"), ["Library"])

    def test_disconnected(self):
        self.campus.add_location("Medical Room")
        self.assertIsNone(self.campus.shortest_path("Main Gate", "Medical Room"))
        self.assertEqual(self.campus.bfs("Medical Room"), ["Medical Room"])
        self.assertEqual(self.campus.dfs("Medical Room"), ["Medical Room"])

    def test_nonexistent_starts(self):
        for method in (self.campus.bfs, self.campus.dfs):
            with self.assertRaises(ValueError):
                method("Hostel")
        with self.assertRaises(ValueError):
            self.campus.shortest_path("Library", "Hostel")

    def test_bubble_sort_and_no_mutation(self):
        before = list(self.campus.graph)
        self.assertEqual(self.campus.alphabetical_locations(),
                         ["Auditorium", "Canteen", "Classroom", "Computer Lab",
                          "Library", "Main Gate", "Playground"])
        self.assertEqual(list(self.campus.graph), before)

    def test_empty_graph(self):
        campus = CampusGraph()
        self.assertEqual(campus.alphabetical_locations(), [])
        self.assertIsNone(campus.find_location("A"))

    def test_all_pairs_shortest_distance(self):
        # Independent repeated edge relaxation checks all 49 endpoint pairs.
        graph = self.campus.graph
        for start in graph:
            distance = {v: float("inf") for v in graph}
            distance[start] = 0
            for _ in range(len(graph) - 1):
                for first in graph:
                    for second in graph[first]:
                        distance[second] = min(distance[second], distance[first] + 1)
            for end in graph:
                route = self.campus.shortest_path(start, end)
                self.assertEqual(len(route) - 1, distance[end])
                for first, second in zip(route, route[1:]):
                    self.assertIn(second, graph[first])

    def test_menu_all_options(self):
        inputs = ["1", "2", "Medical Room", "3", "Library", "Medical Room",
                  "4", "5", "library", "6", "Main Gate", "7", "Main Gate",
                  "8", "Main Gate", "Classroom", "9", "10"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
            main()
        text = output.getvalue()
        for marker in ("Campus locations:", "Added location:", "Pathway added",
                       "Campus adjacency list:", "Found: Library", "BFS:", "DFS:",
                       "Shortest route:", "Locations in alphabetical order:", "Goodbye!"):
            self.assertIn(marker, text)

    def test_menu_errors_and_disconnection(self):
        inputs = ["abc", "", "11", "2", "", "2", "LIBRARY", "3", "Library", "Hostel",
                  "3", "Library", "Library", "3", "Main Gate", "Library",
                  "5", "Hostel", "6", "Hostel", "7", "Hostel",
                  "8", "Library", "Hostel", "2", "Medical Room",
                  "8", "Library", "Medical Room", "10"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
            main()
        text = output.getvalue()
        for marker in ("Invalid choice.", "Location already exists", "Location not found",
                       "Choose two different", "Pathway already exists", "No route exists"):
            self.assertIn(marker, text)

    def test_eof_and_keyboard_interrupt(self):
        for exception in (EOFError, KeyboardInterrupt):
            output = io.StringIO()
            with patch("builtins.input", side_effect=exception), redirect_stdout(output):
                main()
            self.assertIn("Session ended.", output.getvalue())

if __name__ == "__main__":
    unittest.main()
