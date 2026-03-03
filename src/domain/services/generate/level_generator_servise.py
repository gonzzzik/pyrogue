from typing import List, Tuple, Optional, Dict, Set
import random
import sys
import os

# Handle both relative imports (as module) and direct execution
try:
    from ...models.game_models.level import Level, Room
    from ...models.items.BasicItem import item
    from ...models.items.treasure import treasure
    from ...models.items.consumable import apple, elder_hero, gaala
    from ...models.items.weapons import arm, whole_sword
except ImportError:
    import os
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    if workspace_root not in sys.path:
        sys.path.insert(0, workspace_root)
    
    from src.domain.models.game_models.level import Level, Room
    from src.domain.models.items.BasicItem import item
    from src.domain.models.items.treasure import treasure
    from src.domain.models.items.consumable import apple, elder_hero, gaala
    from src.domain.models.items.weapons import arm, whole_sword



class DungeonRenderer:

    
    @staticmethod
    def draw_room(map_grid: List[List[str]], room: Room) -> None:

        x1, y1 = room.top_left
        x2, y2 = room.bot_right
        
        # Clamp to map bounds
        y1 = max(0, y1)
        y2 = min(len(map_grid) - 1, y2)
        x1 = max(0, x1)
        x2 = min(len(map_grid[0]) - 1, x2)
        
        # Draw walls on outline
        for y in range(y1, y2 + 1):
            map_grid[y][x1] = '#'  # left wall
            map_grid[y][x2] = '#'  # right wall
        
        for x in range(x1, x2 + 1):
            map_grid[y1][x] = '#'  # top wall
            map_grid[y2][x] = '#'  # bottom wall
        
        # Fill interior with floor
        for y in range(y1 + 1, y2):
            for x in range(x1 + 1, x2):
                if map_grid[y][x] == ' ':
                    map_grid[y][x] = '.'
    
    @staticmethod
    def draw_corridor(
        map_grid: List[List[str]], 
        room_a: Room,
        room_b: Room,
        width: int,
        height: int
    ) -> None:

        # Get room centers
        x1 = (room_a.top_left[0] + room_a.bot_right[0]) // 2
        y1 = (room_a.top_left[1] + room_a.bot_right[1]) // 2
        
        x2 = (room_b.top_left[0] + room_b.bot_right[0]) // 2
        y2 = (room_b.top_left[1] + room_b.bot_right[1]) // 2
        
        # Draw horizontal then vertical L-shaped corridor
        # Only mark cells that are currently empty
        corridor_char = '.'
        
        # Horizontal segment
        if x1 != x2:
            step = 1 if x2 > x1 else -1
            x = x1 + step
            while x != x2 + step:
                if 0 <= x < width and 0 <= y1 < height:
                    if map_grid[y1][x] == ' ':
                        map_grid[y1][x] = corridor_char
                x += step
        
        # Vertical segment  
        if y1 != y2:
            step = 1 if y2 > y1 else -1
            y = y1 + step
            while y != y2 + step:
                if 0 <= x2 < width and 0 <= y < height:
                    if map_grid[y][x2] == ' ':
                        map_grid[y][x2] = corridor_char
                y += step


class CorridorBuilder:

    
    def __init__(self, extra_link_probability: float = 0.15):
        self.extra_link_probability = extra_link_probability
    
    def build_corridors(self, rooms_grid: List[List[Optional[Room]]], lvl: Level) -> None:

        if not lvl.rooms:
            lvl.corridors = []
            return
        
        # Build adjacency info
        neighbors: Dict[int, List[int]] = {}
        sector_to_room: Dict[int, Room] = {}
        
        for row in range(3):
            for col in range(3):
                room = rooms_grid[row][col]
                if room is not None:
                    neighbors[room.sector] = []
                    sector_to_room[room.sector] = room
                    # Check 4 cardinal directions
                    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                        nr = row + dr
                        nc = col + dc
                        if 0 <= nr < 3 and 0 <= nc < 3:
                            neighbor_room = rooms_grid[nr][nc]
                            if neighbor_room is not None:
                                neighbors[room.sector].append(neighbor_room.sector)
        
        visited: Set[int] = set()
        corridors: List[Tuple[int, int]] = []
        
        start_sector = lvl.rooms[0].sector if lvl.rooms else 0
        
        def dfs(sector: int) -> None:
            visited.add(sector)
            if sector in neighbors:
                neighbors[sector].sort()  # deterministic
                for neighbor_sector in neighbors[sector]:
                    if neighbor_sector not in visited:
                        visited.add(neighbor_sector)
                        corridors.append((sector, neighbor_sector))
                        dfs(neighbor_sector)
        
        if start_sector in neighbors:
            dfs(start_sector)

        unvisited = [r.sector for r in lvl.rooms if r.sector not in visited]
        for unvisited_sector in unvisited:

            closest_sector = min(visited, 
                                key=lambda s: self._distance_between_rooms(
                                    sector_to_room[unvisited_sector],
                                    sector_to_room[s]
                                ))
            corridors.append((min(unvisited_sector, closest_sector), 
                            max(unvisited_sector, closest_sector)))
            visited.add(unvisited_sector)
        
        all_sectors = list(neighbors.keys())
        for i, sector_a in enumerate(all_sectors):
            for sector_b in all_sectors[i+1:]:
                if sector_b in neighbors.get(sector_a, []):
                    if random.random() < self.extra_link_probability:
                        key = (min(sector_a, sector_b), max(sector_a, sector_b))
                        if key not in corridors:
                            corridors.append(key)
        
        lvl.corridors = corridors
    
    @staticmethod
    def _distance_between_rooms(room_a: Room, room_b: Room) -> float:
        x1 = (room_a.top_left[0] + room_a.bot_right[0]) // 2
        y1 = (room_a.top_left[1] + room_a.bot_right[1]) // 2
        x2 = (room_b.top_left[0] + room_b.bot_right[0]) // 2
        y2 = (room_b.top_left[1] + room_b.bot_right[1]) // 2
        return abs(x1 - x2) + abs(y1 - y2)


class LevelGenerator:
    
    def __init__(self, 
                 room_placement_chance: float = 0.7,
                 min_room_width: int = 3,
                 min_room_height: int = 3,
                 extra_corridor_probability: float = 0.15):
        self.room_placement_chance = room_placement_chance
        self.min_room_width = min_room_width
        self.min_room_height = min_room_height
        self.corridor_builder = CorridorBuilder(extra_corridor_probability)
        self.renderer = DungeonRenderer()
    
    def generate(self, size_x: int, size_y: int, uuid: int = None) -> Level:

        if uuid is None:
            uuid = random.randint(10**6, 9 * 10**6)
        
        lvl = Level(uuid)
        random.seed(uuid)
        

        size_x = (size_x // 3) * 3
        size_y = (size_y // 3) * 3
        
        cell_w = size_x // 3
        cell_h = size_y // 3
        

        lvl.rooms = self._generate_rooms(cell_w, cell_h, size_x)
        rooms_grid = self._create_rooms_grid(lvl.rooms)
        

        self.corridor_builder.build_corridors(rooms_grid, lvl)
        
        # Render to global map
        lvl.global_map = [[' ' for _ in range(size_x)] for _ in range(size_y)]
        self._render_dungeon(lvl, size_x, size_y)
        
        return lvl
    
    def _generate_rooms(self, cell_w: int, cell_h: int, total_width: int) -> List[Room]:

        target_rooms = random.randint(7, 9)
        rooms_grid = [[None for _ in range(3)] for _ in range(3)]
        room_list = []
        

        all_positions = [(r, c) for r in range(3) for c in range(3)]
        random.shuffle(all_positions)
        

        for row, col in all_positions:
            if len(room_list) >= target_rooms:
                break
            
            room = self._gen_room_in_sector(
                cell_w, cell_h, row, col, total_width
            )
            rooms_grid[row][col] = room
            room.grid_y = row
            room.grid_x = col
            room.sector = row * 3 + col
            room_list.append(room)
        
        return room_list
    
    def _gen_room_in_sector(
        self,
        cell_w: int, cell_h: int, 
        grid_row: int, grid_col: int,
        total_width: int
    ) -> Room:
        room = Room()
        
        # Sector bounds
        sector_x = grid_col * cell_w
        sector_y = grid_row * cell_h
        
        # Random room size inside sector
        room_w = random.randint(self.min_room_width, cell_w - 2)
        room_h = random.randint(self.min_room_height, cell_h - 2)
        
        # Random position within sector
        px = random.randint(1, cell_w - room_w - 1)
        py = random.randint(1, cell_h - room_h - 1)
        
        # Global coordinates
        room.top_left = (sector_x + px, sector_y + py)
        room.bot_right = (
            sector_x + px + room_w,
            sector_y + py + room_h
        )
        
        return room
    
    @staticmethod
    def _create_rooms_grid(rooms: List[Room]) -> List[List[Optional[Room]]]:
        """Create a 3x3 grid representation of rooms by sector."""
        grid = [[None for _ in range(3)] for _ in range(3)]
        for room in rooms:
            if 0 <= room.grid_y < 3 and 0 <= room.grid_x < 3:
                grid[room.grid_y][room.grid_x] = room
        return grid
    
    def _render_dungeon(self, lvl: Level, width: int, height: int) -> None:
        """Render rooms and corridors to the global map."""
        # Draw corridors first
        for a_sector, b_sector in lvl.corridors:
            room_a = next(r for r in lvl.rooms if r.sector == a_sector)
            room_b = next(r for r in lvl.rooms if r.sector == b_sector)
            self.renderer.draw_corridor(lvl.global_map, room_a, room_b, width, height)
        
        # Draw rooms last so they overwrite any corridor artifacts
        for room in lvl.rooms:
            self.renderer.draw_room(lvl.global_map, room)
    
    @staticmethod
    def rand_item() -> item:
        """Generate a random item.
        
        Returns:
            Random item object from available items
        """
        choice = random.choice([
            'treasure', 'apple', 'hero_scroll', 'gaala', 'arm', 'sword'
        ])
        if choice == 'treasure':
            return treasure(random.randint(1, 50))
        elif choice == 'apple':
            return apple()
        elif choice == 'hero_scroll':
            return elder_hero()
        elif choice == 'gaala':
            return gaala()
        elif choice == 'arm':
            return arm()
        elif choice == 'sword':
            return whole_sword()
        return treasure(1)


if __name__ == '__main__':
    # Demo: instantiate generator and create a level
    generator = LevelGenerator(
        room_placement_chance=0.7,
        min_room_width=3,
        min_room_height=3,
        extra_corridor_probability=0.15
    )
    
    lvl = generator.generate(30, 15)
    for row in lvl.global_map:
        print(''.join(row))
    print(f"\nrooms: {len(lvl.rooms)}, corridors: {len(lvl.corridors)}")