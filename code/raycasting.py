import pygame
import numpy as np
from settings import *


def generate_directions(num_rays):
    """Generate evenly distributed ray directions in a full circle using NumPy."""
    # Using numpy linspace is already efficient for generating evenly spaced rays.
    angles = np.linspace(0, 2 * np.pi, num_rays, endpoint=False)
    return np.column_stack((np.cos(angles), np.sin(angles)))


def cast_ray(origin, dx, dy, obstacles):
    """Efficiently cast a ray and return the first hit point."""
    origin = pygame.Vector2(origin)

    # Use early exit for performance: if we hit an obstacle quickly, return early
    for i in range(1, MAX_RAY_DIST, RAY_STEP):
        point = origin + pygame.Vector2(dx, dy) * i
        # Optimize collision check: stop as soon as the first hit is detected
        for obstacle in obstacles:
            if obstacle.rect.collidepoint(point.xy):  # First collision check
                return point.xy
    # If no collision, return the farthest point in the ray direction
    return (origin.x + dx * MAX_RAY_DIST, origin.y + dy * MAX_RAY_DIST)


def simplify_points(points, threshold=4):
    """Simplify points by eliminating unnecessary points based on a threshold distance."""
    if len(points) <= 1:
        return points

    simplified = [points[0]]
    last_point = pygame.Vector2(points[0])

    # Only append points if they exceed the threshold distance from the last point
    for pt in points[1:]:
        current_point = pygame.Vector2(pt)
        if (current_point - last_point).length() > threshold:
            simplified.append(pt)
            last_point = current_point

    # Ensure the polygon closes well if the first and last points are close enough
    if len(simplified) > 1 and (pygame.Vector2(simplified[0]) - pygame.Vector2(simplified[-1])).length() < threshold:
        simplified[-1] = simplified[0]

    return simplified


def get_hit_points(player_pos, num_rays, obstacles, simplify=True, threshold=3):
    """Get the hit points from the player's position using raycasting."""

    # Generate the directions for the rays.
    directions = generate_directions(num_rays)

    # Using list comprehension for efficient raycasting
    raw_points = [cast_ray(player_pos, dx, dy, obstacles)
                  for dx, dy in directions]

    # Simplify points only if requested, otherwise return raw points
    return simplify_points(raw_points, threshold) if simplify else raw_points
