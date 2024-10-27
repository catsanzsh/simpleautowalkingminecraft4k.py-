from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from threading import Timer

class AutoMinecraft(Ursina):
    def __init__(self):
        super().__init__()
        # Window settings
        window.fullscreen = False
        window.exit_button.visible = True
        window.fps_counter.enabled = True

        # Game variables
        self.RENDER_DISTANCE = 20
        self.WORLD_SIZE = 32
        self.blocks = {}
        self.block_pick = 1
        self.terrain_height = {}
        self.auto_playing = False
        self.player = None
        self.target_position = None

    def generate_terrain(self):
        # Generate simple terrain using random heights
        for z in range(-self.WORLD_SIZE, self.WORLD_SIZE):
            for x in range(-self.WORLD_SIZE, self.WORLD_SIZE):
                height = random.randint(0, 5)  # Simple random height
                self.terrain_height[(x, z)] = height
                
                # Generate basic terrain layers
                for y in range(height, -3, -1):
                    block = None
                    if y == height:
                        block = Block(position=(x, y, z), texture='grass')
                    elif y > height - 3:
                        block = Block(position=(x, y, z), texture='dirt')
                    else:
                        block = Block(position=(x, y, z), texture='stone')
                    self.blocks[(x, y, z)] = block

    def start_auto_play(self):
        self.auto_playing = True
        self.update_auto_player()

    def update_auto_player(self):
        if not self.auto_playing:
            return

        if not self.target_position or self.reached_target():
            # Choose new random target within world bounds
            x = random.randint(-self.WORLD_SIZE + 5, self.WORLD_SIZE - 5)
            z = random.randint(-self.WORLD_SIZE + 5, self.WORLD_SIZE - 5)
            y = self.terrain_height.get((x, z), 0) + 1
            self.target_position = Vec3(x, y, z)

        # Move towards target
        direction = (self.target_position - self.player.position).normalized()
        self.player.position += direction * time.dt * 5

        # Schedule next update
        Timer(0.05, self.update_auto_player).start()

    def reached_target(self):
        if not self.target_position:
            return True
        distance = (self.target_position - self.player.position).length()
        return distance < 1

class Block(Button):
    def __init__(self, position=(0,0,0), texture='grass'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            highlight_color=color.lime,
        )

def main():
    app = Ursina()
    game = AutoMinecraft()
    
    # Set up scene
    Sky()
    
    # Generate terrain
    game.generate_terrain()
    
    # Set up player
    game.player = FirstPersonController()
    game.player.gravity = 0.5
    game.player.jump_height = 2
    game.player.jump_duration = 0.3
    
    # Start auto-play after a short delay
    Timer(2.0, game.start_auto_play).start()
    
    # Run the game
    app.run()

if __name__ == '__main__':
    main()