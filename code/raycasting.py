import pygame
import math
from settings import *  

# utilities for edge detection

def normalize_edge(edge):
    """Sort edge points to make (A, B) and (B, A) equal, and round coordinates to integers."""
    p1 = tuple(round(coord) for coord in edge[0])
    p2 = tuple(round(coord) for coord in edge[1])
    return tuple(sorted([p1, p2]))


def get_adjacent_tiles(tile, grid_obstacles):
    """
    Return a list of tiles that are directly adjacent (sharing a side) to the given tile.
    Diagonal tiles are not considered adjacent here.
    """
    adjacent_tiles = []
    for other in grid_obstacles:
        if tile == other:
            continue
        if (
            (tile.x == other.x and abs(tile.y - other.y) == TILESIZE) or
            (tile.y == other.y and abs(tile.x - other.x) == TILESIZE)
        ):
            adjacent_tiles.append(other)
    return adjacent_tiles


def get_relevant_edges(tile, grid_obstacles):
    """
    Return edges of a tile that are not shared with any of its adjacent neighbors.
    This helps avoid redundant edges that won't affect raycasting.
    """
    all_edges = Raycaster.get_edges(tile)
    relevant_edges = []

    # Get tiles that are directly touching the current one
    adjacent_tiles = get_adjacent_tiles(tile, grid_obstacles)

    # Check each edge and remove it if it's shared with any adjacent tile
    for edge in all_edges:
        norm_edge = normalize_edge(edge)
        is_shared = False
        for adj_tile in adjacent_tiles:
            adj_edges = Raycaster.get_edges(adj_tile)
            for adj_edge in adj_edges:
                if norm_edge == normalize_edge(adj_edge):
                    is_shared = True
                    break
            if is_shared:
                break
        if not is_shared:
            relevant_edges.append(edge)

    return relevant_edges


def deduplicate_edges(edges):
    """
    Remove duplicate edges by normalizing them and keeping only unique ones.
    Ensures (A, B) and (B, A) are treated as the same.
    """
    seen = set()
    unique_edges = []
    for edge in edges:
        norm = normalize_edge(edge)
        if norm not in seen:
            seen.add(norm)
            unique_edges.append(edge) 
    return unique_edges


def merge_edges(edges):
    """
    Merge colinear and connected edges into longer lines to reduce the number of edges.
    Only works for horizontal and vertical lines.
    """
    from collections import defaultdict

    def snap(p):
        """Snap a point to the nearest GRID_SIZE multiple to avoid small float mismatches."""
        return (round(p[0] // TILESIZE) * TILESIZE,
                round(p[1] // TILESIZE) * TILESIZE)

    # Separate edges into horizontal and vertical lines, grouped by their y or x coordinate
    horizontal_lines = defaultdict(list)
    vertical_lines = defaultdict(list)

    for edge in edges:
        p1, p2 = sorted([snap(edge[0]), snap(edge[1])])
        if p1[1] == p2[1]:  # horizontal
            y = p1[1]
            horizontal_lines[y].append((p1[0], p2[0]))
        elif p1[0] == p2[0]:  # vertical
            x = p1[0]
            vertical_lines[x].append((p1[1], p2[1]))

    def merge_line_segments(segments):
        """Merge overlapping or touching segments into longer continuous ones."""
        if not segments:
            return []
        segments.sort()
        merged = []
        curr_start, curr_end = segments[0]
        for start, end in segments[1:]:
            if start <= curr_end:  # Overlapping or touching
                curr_end = max(curr_end, end)
            else:
                merged.append((curr_start, curr_end))
                curr_start, curr_end = start, end
        merged.append((curr_start, curr_end))
        return merged

    # Reconstruct merged horizontal edges
    merged_edges = []

    for y, segments in horizontal_lines.items():
        merged = merge_line_segments(segments)
        for x1, x2 in merged:
            merged_edges.append(((x1, y), (x2, y)))

    # Reconstruct merged vertical edges
    for x, segments in vertical_lines.items():
        merged = merge_line_segments(segments)
        for y1, y2 in merged:
            merged_edges.append(((x, y1), (x, y2)))

    return merged_edges


def get_all_relevant_edges(obstacles):
    """
    Combines all relevant edges from the obstacle tiles and screen border edges.
    1. Get non-shared edges from each obstacle tile.
    2. Add screen border edges for limiting rays.
    3. Deduplicate and merge final edge list for optimization.
    """
    all_relevant_edges = []

    # Collect relevant (non-shared) edges from all obstacle tiles
    for tile in obstacles:
        edges = get_relevant_edges(tile, obstacles)
        all_relevant_edges.extend(edges)

    # Optimize the edge list by removing duplicates and merging
    all_relevant_edges = deduplicate_edges(all_relevant_edges)
    all_relevant_edges = merge_edges(all_relevant_edges)

    return all_relevant_edges


class Raycaster:
    @staticmethod
    def normalize(v):
        """
        Normalize a vector safely.
        Returns a zero vector if input has zero length.
        """
        if v.length() == 0:
            return pygame.Vector2(0, 0)
        return v.normalize()

    @staticmethod
    def get_edges(rect):
        """
        Return the 4 edges of a rectangle as a list of (point1, point2) tuples.
        Used for raycasting bounds like screen edges.
        """
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        return [
            ((x, y), (x + w, y)),             # Top edge
            ((x + w, y), (x + w, y + h)),     # Right edge
            ((x + w, y + h), (x, y + h)),     # Bottom edge
            ((x, y + h), (x, y))              # Left edge
        ]
    

    @staticmethod
    def find_intersect(edges, ray):
        """
        Find the closest intersection point between a ray and a list of edges.
        Improved version with better precision handling and corner cases.
        """
        origin, direction = ray
        r_px, r_py = origin.x, origin.y
        r_dx, r_dy = direction.x, direction.y

        EPSILON = 1e-10  # Small value for floating point comparisons
        closest_t1 = float("inf")
        closest_point = None

        for (s1, s2) in edges:
            s_px, s_py = s1
            s_dx = s2[0] - s_px
            s_dy = s2[1] - s_py

            # Calculate determinant for intersection
            denom = s_dx * r_dy - s_dy * r_dx

            # Skip if lines are parallel (near zero determinant)
            if abs(denom) < EPSILON:
                continue

            # Calculate intersection parameters
            t2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / denom
            
            # Skip if intersection is outside the edge segment
            if t2 < -EPSILON or t2 > 1 + EPSILON:
                continue

            # Calculate t1 more robustly by choosing the more numerically stable calculation
            if abs(r_dx) > abs(r_dy):
                t1 = (s_px + s_dx * t2 - r_px) / r_dx
            else:
                t1 = (s_py + s_dy * t2 - r_py) / r_dy

            # Skip if intersection is behind the ray origin
            if t1 < EPSILON:
                continue

            # Update closest intersection if this one is closer
            if t1 < closest_t1:
                closest_t1 = t1
                # Use precise intersection calculation
                px = s_px + s_dx * t2
                py = s_py + s_dy * t2
                closest_point = pygame.Vector2(px, py)

        return closest_point


    @staticmethod
    def get_unique_points(edges):
        """
        Return a list of unique points from a list of edges.
        Used to determine where to cast rays.
        """
        seen = set()
        points = []
        for a, b in edges:
            for p in [a, b]:
                if p not in seen:
                    seen.add(p)
                    points.append(p)
        return points

    @staticmethod
    def find_all_intersects(origin, edges):
        """
        Cast rays from the origin toward every unique edge point and corner.
        Improved version with better corner handling and more precise angles.
        """
        points = []
        EPSILON = 0.0001  # Smaller epsilon for tighter ray spread
        unique_points = Raycaster.get_unique_points(edges)

        def add_ray_at_angle(angle):
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            ray = (origin, direction)
            intersection = Raycaster.find_intersect(edges, ray)
            if intersection:
                points.append(intersection)

        # Cast rays to all unique points
        for px, py in unique_points:
            base_angle = math.atan2(py - origin.y, px - origin.x)
            
            # Cast 5 rays around each corner point for better coverage
            angles = [
                base_angle,  # Direct ray
                base_angle - EPSILON,  # Slightly left
                base_angle + EPSILON,  # Slightly right
                base_angle - 2 * EPSILON,  # Further left
                base_angle + 2 * EPSILON,  # Further right
            ]
            
            for angle in angles:
                add_ray_at_angle(angle)

        # Sort points by angle for proper polygon rendering
        # Use a more precise sorting method
        def get_angle(point):
            dx = point.x - origin.x
            dy = point.y - origin.y
            angle = math.atan2(dy, dx)
            return angle if angle >= 0 else angle + 2 * math.pi

        points.sort(key=get_angle)
        
        # Remove duplicate points that are very close to each other
        filtered_points = []
        for i, point in enumerate(points):
            if not filtered_points or (point - filtered_points[-1]).length() > EPSILON:
                filtered_points.append(point)

        return filtered_points
    
    
