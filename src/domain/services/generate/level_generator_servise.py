from ...models.game_models.level import Level, Room, List
import random

class LevelGenerator:
    
    def generate(self, size_x: int, size_y: int, uuid: int = random.randint(10**6, 9 * 10**6)) -> Level:
        lvl = Level(uuid)
        random.seed(uuid)
        
        while size_x % 3: size_x -= 1
        while size_y % 3: size_y -= 1
        
        for i in range(9):
            lvl.rooms.append(self.gen_room(int(size_x / 3), int(size_y / 3), i))
            if random.randint(0, 1):
                lvl.rooms[i] = self.gen_items(lvl.rooms[i])
            
        lvl = self.gen_coridors(lvl)
        
            
        
        return lvl
    
    
    def gen_room(self, size_x: int, size_y: int, iteration) -> Room:
        room = Room()
        room.size_x = random.randint(int(size_x / 3), size_x - 4)
        room.size_y = random.randint(int(size_y / 3), size_y - 4)

        room.pos_x = random.randint(1, size_x - room.size_x - 1)
        room.pos_y = random.randint(1, size_y - room.size_y - 1)

        for i in range(size_y):
            line: list[object] = []              
            if i == room.pos_y - 1:
                for j in range(room.pos_x - 1): line.append(None)
                for j in range(room.size_x + 2): line.append('=')
                for j in range(size_x - room.size_x - room.pos_x - 1): line.append(None)
            elif i > room.pos_y - 1 and i < room.pos_y + room.size_y:
                for j in range(room.pos_x - 1): line.append(None)
                line.append('|')
                for j in range(room.size_x): line.append(None)
                line.append('|')
                for j in range(size_x - room.size_x - room.pos_x - 1): line.append(None)
            elif i == room.pos_y + room.size_y:
                for j in range(room.pos_x - 1): line.append(None)
                for j in range(room.size_x + 2): line.append('-')
                for j in range(size_x - room.size_x - room.pos_x - 1): line.append(None)
            else:
                for j in range(size_x): line.append(None)
                
            room.room_map.append(line)
        
        return room
    
    
    def gen_item(self, room: Room) -> Room:
        x = random.randint(0, room.size_x)
        y = random.randint(0, room.size_y)
        
        room.room_map[y][x] = rand_item()
        
        return room
    
    
    def rand_item() -> item: