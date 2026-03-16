import os,sys,random
import numpy as np
import matplotlib.pyplot as plt

class AStar:
    def __init__(self):
        self.grid = None
        self.start = None
        self.goal = None
        self.open_set = []
        self.came_from = {}
        self.g_score = {}
        self.f_score = {}
    
    def generate_maze(self, width, height, obstacle_prob=0.2):
        """Generate a random maze with given dimensions and obstacle probability"""
        self.grid = [[0 if random.random() > obstacle_prob else 1 for _ in range(width)] for _ in range(height)]

    
    def save_maze(self):
        """Save the maze to a text file"""
        with open("maze.txt", "w") as f:
            for row in self.grid:
                f.write("".join(str(cell) for cell in row) + "\n")
    
    def load_maze(self):
        """Load the maze from a text file"""
        with open("maze.txt", "r") as f:
            self.grid = [[int(cell) for cell in line.strip()] for line in f]

    def heuristic(self, pos):
        """Manhattan distance heuristic"""
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])

    def get_neighbors(self, pos):
        """Get valid neighboring cells"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = pos[0] + dx, pos[1] + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                if self.grid[nx][ny] == 0:  # 0 = walkable
                    neighbors.append((nx, ny))
        return neighbors

    def display_maze(self):        
        """Visualize the maze using matplotlib"""
        plt.figure(figsize=(8, 8))
        plt.imshow(np.array(self.grid), cmap='binary')
        plt.title('Maze')
        plt.gca().set_xticks(np.arange(-0.5, len(self.grid[0]), 1), minor=True)
        plt.gca().set_yticks(np.arange(-0.5, len(self.grid), 1), minor=True)
        plt.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        # Add cell value labels
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                plt.text(j, i, str(self.grid[i][j]), ha='center', va='center', color='red', fontsize=8)
        # Draw the path if it exists
        if hasattr(self, 'last_path') and self.last_path:
            path = self.last_path
            for i, (x, y) in enumerate(path):
                if (x, y) != self.start and (x, y) != self.goal:
                    plt.plot(y, x, 'go', markersize=5)
                plt.plot(self.start[1], self.start[0], 'bs', markersize=8, label='Start')
                plt.plot(self.goal[1], self.goal[0], 'r*', markersize=15, label='Goal')
        plt.show()
    
    def reconstruct_path(self, current):
        """Reconstruct the path from start to goal"""
        total_path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            total_path.append(current)
        self.last_path = total_path[::-1]  # Store the path for visualization

    def solve(self,start, goal):
        """Execute A* algorithm and return path"""
        self.start = start
        self.goal = goal
        self.open_set = [start]
        self.came_from = {}
        self.g_score = {start: 0}
        self.f_score = {start: self.heuristic(start)}
        while self.open_set:
            print(f"Open set: {self.open_set}")
            current = min(self.open_set, key=lambda x: self.f_score[x])
            if current == self.goal: self.reconstruct_path(current)
            print(f"Current node: {current}, g_score: {self.g_score[current]}, f_score: {self.f_score[current]}")
            
            self.open_set.remove(current)
            for neighbor in self.get_neighbors(current):
                tentative_g = self.g_score[current] + 1
                if neighbor not in self.g_score or tentative_g < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g
                    self.f_score[neighbor] = tentative_g + self.heuristic(neighbor)
                    if neighbor not in self.open_set:
                        self.open_set.append(neighbor)


if __name__ == "__main__":
    astar = AStar()
    #astar.generate_maze(20, 20, obstacle_prob=0.3)
    #astar.save_maze()
    astar.load_maze()
    
    start = (0, 0)
    goal = (19, 19)
    path = astar.solve(start, goal)
    print("Path from {} to {}: {}".format(start, goal, path))
    astar.display_maze()