import os,sys,random
import networkx as nx
import matplotlib.pyplot as plt

class Dijkstra:
    def __init__(self):
        self.graph = None
        self.graph_edges = None
    
    def generate_graph(self,total_nodes,weight_range=(1,10),edge_probability=0.5):
        self.graph = {i: {} for i in range(total_nodes)}
        for i in range(total_nodes):
            for j in range(i + 1, total_nodes):
                if random.random() < edge_probability:
                    weight = random.randint(*weight_range)
                    self.graph[i][j] = weight
                    self.graph[j][i] = weight
    
    def convert_graph_to_edges(self):
        self.graph_edges = []
        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                if (neighbor, node, weight) not in self.graph_edges:  # Avoid duplicates
                    self.graph_edges.append((node, neighbor, weight))
    
    def print_graph(self):
        print("Graph:", self.graph)
        print("Edges:", self.graph_edges)

    def save_graph(self):
        with open("graph.txt", "w") as f:
            for node, neighbors in self.graph.items():
                for neighbor, weight in neighbors.items():
                    f.write(f"{node} {neighbor} {weight}\n")

    def load_graph(self):
        self.graph = {}
        with open("graph.txt", "r") as f:
            for line in f:
                node, neighbor, weight = map(int, line.strip().split())
                if node not in self.graph:
                    self.graph[node] = {}
                self.graph[node][neighbor] = weight

    

    def display_graph(self):
        G = nx.Graph()
        for node in self.graph:
            for neighbor, weight in self.graph[node].items():
                G.add_edge(node, neighbor, weight=weight)

        pos = nx.spring_layout(G, seed=42, k=2, iterations=50)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=12, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)
        plt.title("Graph Visualization", fontsize=14, fontweight='bold')
        plt.axis('off')
        #plt.tight_layout()
        #plt.show()
        plt.savefig("graph_visualization.png", dpi=300)

    def dijkstra_from_graph(self, start_node, end_node):
        visited = {start_node: 0}
        path = {}

        nodes = set(self.graph.keys())

        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None or visited[node] < visited[min_node]:
                        min_node = node
            print(f"Current node: {min_node}, Visited: {visited}")
            if min_node is None:
                print("No more reachable nodes. Ending algorithm.")
                break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            for neighbor, weight in self.graph[min_node].items():
                print(f"Visiting neighbor {neighbor} of node {min_node} with edge weight {weight}")
                weight = current_weight + weight
                if neighbor not in visited or weight < visited[neighbor]:
                    if neighbor not in visited:print(f"Adding neighbor {neighbor} to visited with initial cost {weight}")
                    else: print(f"Updating neighbor {neighbor} in visited with new lower cost {weight} (previous cost was {visited[neighbor]})")
    
                    visited[neighbor] = weight
                    path[neighbor] = min_node
            print(f"Visited after processing node {min_node}: {visited}\n")
            print(f"Path mapping after processing node {min_node}: {path}\n")

        if end_node not in visited:
            print(f"No path found from node {start_node} to node {end_node}.")
            return None, float('inf')
        
        full_path = []
        current_node = end_node
        while current_node != start_node:
            full_path.append(current_node)
            current_node = path[current_node]
        full_path.append(start_node)
        full_path.reverse()

        return full_path, visited[end_node]
    
    def dijkstra_from_edges(self, start_node, end_node):
        visited = {start_node: 0}
        path = {}
        nodes = set()

        # Build nodes set from edges
        for node1, node2, weight in self.graph_edges:
            nodes.add(node1)
            nodes.add(node2)

        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None or visited[node] < visited[min_node]:
                        min_node = node
            
            print(f"Current node: {min_node}, Visited: {visited}")
            if min_node is None:
                print("No more reachable nodes. Ending algorithm.")
                break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            # Find neighbors from edge list
            for node1, node2, weight in self.graph_edges:
                neighbor = None
                if node1 == min_node:
                    neighbor = node2
                elif node2 == min_node:
                    neighbor = node1
                
                if neighbor is not None:
                    print(f"Visiting neighbor {neighbor} of node {min_node} with edge weight {weight}")
                    new_weight = current_weight + weight
                    if neighbor not in visited or new_weight < visited[neighbor]:
                        if neighbor not in visited:
                            print(f"Adding neighbor {neighbor} to visited with initial cost {new_weight}")
                        else:
                            print(f"Updating neighbor {neighbor} in visited with new lower cost {new_weight} (previous cost was {visited[neighbor]})")
                        visited[neighbor] = new_weight
                        path[neighbor] = min_node
            
            print(f"Visited after processing node {min_node}: {visited}\n")
            print(f"Path mapping after processing node {min_node}: {path}\n")

        if end_node not in visited:
            print(f"No path found from node {start_node} to node {end_node}.")
            return None, float('inf')

        full_path = []
        current_node = end_node
        while current_node != start_node:
            full_path.append(current_node)
            current_node = path[current_node]
        full_path.append(start_node)
        full_path.reverse()

        return full_path, visited[end_node]

if __name__ == "__main__":
    dijkstra = Dijkstra()
    #dijkstra.generate_graph(total_nodes=5, weight_range=(1, 10), edge_probability=0.5)
    #dijkstra.save_graph()
    dijkstra.load_graph()
    dijkstra.convert_graph_to_edges()
    dijkstra.print_graph()
    dijkstra.display_graph()
    start_node = 0
    end_node = 4
    path, cost = dijkstra.dijkstra_from_graph(start_node, end_node)
    print(f"Shortest path from node {start_node} to node {end_node}: {path} with total cost: {cost}")
    path, cost = dijkstra.dijkstra_from_edges(start_node, end_node)
    print(f"Shortest path from node {start_node} to node {end_node} (using edges): {path} with total cost: {cost}")