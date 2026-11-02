"""Lab 10: Campus navigation using syllabus data structures.
Run: python main.py. No third-party packages are required.
"""

class Queue:
    """FIFO queue: append at rear; advance a front index to dequeue."""
    def __init__(self):
        self.items = []
        self.front = 0

    def enqueue(self, item):
        self.items.append(item)

    def is_empty(self):
        return self.front == len(self.items)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty.")
        item = self.items[self.front]
        self.front += 1
        return item


class CampusGraph:
    """Undirected, unweighted graph stored as a dictionary of lists."""
    def __init__(self):
        self.graph = {}

    def find_location(self, name):
        """Explicit linear search, ignoring case and repeated spaces."""
        target = " ".join(name.split()).casefold()
        for location in self.graph:
            if location.casefold() == target:
                return location
        return None

    def require_location(self, name):
        location = self.find_location(name)
        if location is None:
            raise ValueError("Location not found: " + name.strip())
        return location

    def add_location(self, name):
        name = " ".join(name.split())
        if not name or len(name) > 40 or not name.isprintable():
            raise ValueError("Use a location name with 1 to 40 printable characters.")
        if self.find_location(name) is not None:
            raise ValueError("Location already exists: " + name)
        self.graph[name] = []
        return name

    def connect_locations(self, first, second):
        first = self.require_location(first)
        second = self.require_location(second)
        if first == second:
            raise ValueError("Choose two different locations.")
        if second in self.graph[first]:
            raise ValueError("Pathway already exists.")
        self.graph[first].append(second)
        self.graph[second].append(first)

    def bfs(self, start):
        start = self.require_location(start)
        queue = Queue()
        queue.enqueue(start)
        visited = {start: True}
        order = []
        while not queue.is_empty():
            current = queue.dequeue()
            order.append(current)
            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited[neighbor] = True
                    queue.enqueue(neighbor)
        return order

    def dfs(self, start):
        start = self.require_location(start)
        stack = [start]
        visited = {}
        order = []
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited[current] = True
            order.append(current)
            # Reverse only controls the visit order; this is not sorting.
            for neighbor in reversed(self.graph[current]):
                if neighbor not in visited:
                    stack.append(neighbor)
        return order

    def shortest_path(self, start, end):
        start = self.require_location(start)
        end = self.require_location(end)
        queue = Queue()
        queue.enqueue(start)
        # A parent records the first predecessor that discovered each vertex.
        parent = {start: None}
        while not queue.is_empty():
            current = queue.dequeue()
            if current == end:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                return path
            for neighbor in self.graph[current]:
                if neighbor not in parent:
                    parent[neighbor] = current
                    queue.enqueue(neighbor)
        return None

    def alphabetical_locations(self):
        """Bubble sort a copy; preserve the original insertion order."""
        names = list(self.graph)
        for last in range(len(names) - 1, 0, -1):
            swapped = False
            for index in range(last):
                if names[index].casefold() > names[index + 1].casefold():
                    names[index], names[index + 1] = names[index + 1], names[index]
                    swapped = True
            if not swapped:
                break
        return names


def create_sample_campus():
    campus = CampusGraph()
    for name in ("Main Gate", "Library", "Canteen", "Computer Lab",
                 "Auditorium", "Classroom", "Playground"):
        campus.add_location(name)
    for first, second in (
        ("Main Gate", "Library"), ("Main Gate", "Canteen"),
        ("Library", "Computer Lab"), ("Library", "Auditorium"),
        ("Canteen", "Auditorium"), ("Computer Lab", "Classroom"),
        ("Auditorium", "Playground"), ("Classroom", "Playground")
    ):
        campus.connect_locations(first, second)
    return campus


def show_menu():
    print("\nCAMPUS NAVIGATION AND SHORTEST PATH FINDER")
    print("1. Display all locations")
    print("2. Add a location")
    print("3. Connect two locations")
    print("4. Display adjacency list")
    print("5. Search for a location")
    print("6. BFS traversal")
    print("7. DFS traversal")
    print("8. Find shortest route")
    print("9. Display locations alphabetically")
    print("10. Exit")


def main():
    campus = create_sample_campus()
    print("Welcome! Sample campus loaded: 7 locations, 8 pathways.")
    print("Routes minimize pathway count; all pathways have equal weight.")
    while True:
        try:
            show_menu()
            choice = input("Enter choice (1-10): ").strip()
            if choice == "1":
                print("\nCampus locations:")
                for number, name in enumerate(campus.graph, 1):
                    print(str(number) + ". " + name)
            elif choice == "2":
                name = campus.add_location(input("New location: "))
                print("Added location: " + name)
            elif choice == "3":
                first = input("First location: ")
                second = input("Second location: ")
                campus.connect_locations(first, second)
                print("Pathway added in both directions.")
            elif choice == "4":
                print("\nCampus adjacency list:")
                for name, neighbors in campus.graph.items():
                    print(name + " -> " + (", ".join(neighbors) or "(no pathways)"))
            elif choice == "5":
                name = campus.find_location(input("Search location: "))
                print("Found: " + name if name else "Location not found.")
            elif choice == "6":
                print("BFS: " + " -> ".join(campus.bfs(input("Start location: "))))
            elif choice == "7":
                print("DFS: " + " -> ".join(campus.dfs(input("Start location: "))))
            elif choice == "8":
                first = input("Start location: ")
                second = input("Destination: ")
                path = campus.shortest_path(first, second)
                if path is None:
                    print("No route exists between these locations.")
                else:
                    print("Shortest route: " + " -> ".join(path))
                    print("Pathways: " + str(len(path) - 1))
            elif choice == "9":
                print("\nLocations in alphabetical order:")
                for name in campus.alphabetical_locations():
                    print(name)
            elif choice == "10":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 10.")
        except ValueError as error:
            print("Error: " + str(error))
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break


if __name__ == "__main__":
    main()
