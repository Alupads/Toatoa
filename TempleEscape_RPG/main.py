# main.py
import pygame
import sys
import json # NEW: For saving/loading files
import os
from settings import *
from player import Player
from ui import Button, InputBox, draw_text_wrapped, draw_stats_bar, draw_visual_novel_ui, draw_start_screen_graphics
from story import get_story_node

SAVE_FILE = "saves.json"

class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Temple Escape RPG")
        self.clock = pygame.time.Clock()
        
        self.player = Player()
        self.current_node = None
        self.next_node = None
        
        # State Management
        self.state = "START_SCREEN" 
        self.char_x = -50
        self.char_y = 250
        
        # UI Elements
        self.buttons = []
        self.menu_buttons = []
        self.input_box = None
        self.active_slot = None

        # Load saves file
        self.saves = self.load_save_file()
        self.build_start_screen()

    # --- SAVE / LOAD LOGIC ---
    def load_save_file(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    return json.load(f)
            except: pass
        # Default empty slots
        return {"1": None, "2": None, "3": None}

    def write_save_file(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.saves, f)

    def execute_load(self, slot_key):
        data = self.saves[slot_key]
        if data:
            self.player = Player()
            self.player.load_dict(data["player"])
            self.current_node = data["node"]
            self.next_node = data["node"]
            self.state = "IDLE"
            self.apply_node_logic() # Refresh UI for the loaded node

    def prompt_save_name(self, slot_key):
        self.active_slot = slot_key
        self.state = "INPUT_NAME"
        self.input_box = InputBox(WIDTH//2 - 125, 200, 250, 40)
        self.menu_buttons = [
            Button(WIDTH//2 - 100, 260, 200, 40, "Confirm Save", self.execute_save),
            Button(WIDTH//2 - 100, 320, 200, 40, "Cancel", lambda: self.set_state("IDLE"))
        ]

    def execute_save(self):
        name = self.input_box.text if self.input_box.text.strip() != "" else "Unnamed Slot"
        self.saves[self.active_slot] = {
            "name": name,
            "node": self.current_node,
            "player": self.player.to_dict()
        }
        self.write_save_file()
        self.set_state("IDLE") # Return to game

    # --- SCREEN BUILDERS ---
    def build_start_screen(self):
        self.menu_buttons.clear()
        self.current_node = None 
        
        button_y = 420
        start_btn = Button(WIDTH//2 - 120, button_y, 240, 40, "NEW GAME", lambda: self.trigger_transition("intro"))
        load_btn = Button(WIDTH//2 - 120, button_y + 50, 240, 40, "LOAD GAME", lambda: self.build_slot_screen("LOAD"))
        quit_btn = Button(WIDTH//2 - 120, button_y + 100, 240, 40, "FLEE", sys.exit)
        
        self.menu_buttons.extend([start_btn, load_btn, quit_btn])

    def build_slot_screen(self, mode):
        self.state = mode + "_MENU" # Becomes LOAD_MENU or SAVE_MENU
        self.menu_buttons.clear()
        
        y_offset = 150
        for i in range(1, 4):
            slot_key = str(i)
            slot_data = self.saves[slot_key]
            text = f"Slot {i}: " + (slot_data["name"] if slot_data else "Empty")
            
            if mode == "LOAD":
                # Only allow clicking if there is data
                action = (lambda k=slot_key: self.execute_load(k)) if slot_data else (lambda: None)
            else: # SAVE mode
                action = lambda k=slot_key: self.prompt_save_name(k)

            self.menu_buttons.append(Button(WIDTH//2 - 150, y_offset, 300, 50, text, action))
            y_offset += 70
        
        # Back Button
        back_action = self.build_start_screen if mode == "LOAD" else lambda: self.set_state("IDLE")
        self.menu_buttons.append(Button(WIDTH//2 - 100, y_offset + 30, 200, 40, "Back", back_action))

    def set_state(self, new_state):
        self.state = new_state
        if new_state == "START_SCREEN":
            self.build_start_screen()

    def trigger_transition(self, next_node_id):
        self.next_node = next_node_id
        self.state = "TRANSITION"
        self.char_x = -50  
        self.buttons.clear()
        self.menu_buttons.clear() 
        self.player = Player() # Fresh player for a new run

    def apply_node_logic(self):
        self.current_node = self.next_node
        node_data = get_story_node(self.current_node)
        
        if not node_data: return

        if "damage" in node_data: self.player.take_damage(node_data["damage"])
        if "sanity_loss" in node_data: self.player.lose_sanity(node_data["sanity_loss"])
        if "give_item" in node_data: self.player.add_item(node_data["give_item"])
        if "remove_item" in node_data: self.player.remove_item(node_data["remove_item"])
        if "flag_saved" in node_data: self.player.saved_survivor = True

        self.buttons.clear()
        
        # Endings / Death Buttons
        if self.player.is_dead() or len(node_data.get("choices", [])) == 0:
            self.buttons.append(Button(WIDTH - 250, TEXT_BOX_Y + 120, 200, 40, "Restart", lambda: self.trigger_transition("intro")))
            self.buttons.append(Button(WIDTH - 250, TEXT_BOX_Y + 170, 200, 40, "Main Menu", lambda: self.set_state("START_SCREEN")))
            return

        # Regular Story Choices
        y_offset = TEXT_BOX_Y + 30
        for choice in node_data.get("choices", []):
            if "requires" in choice and not self.player.has_item(choice["requires"]):
                continue 
            btn = Button(WIDTH - 260, y_offset, 230, 35, choice["text"], 
                         lambda next_id=choice["next"]: self.trigger_transition(next_id))
            self.buttons.append(btn)
            y_offset += 45

        # --- SYSTEM MENU IN-GAME ---
        self.buttons.append(Button(WIDTH - 260, TEXT_BOX_Y + 170, 110, 35, "Save", lambda: self.build_slot_screen("SAVE")))
        self.buttons.append(Button(WIDTH - 140, TEXT_BOX_Y + 170, 110, 35, "Menu", lambda: self.set_state("START_SCREEN")))


    def draw_hud(self):
        draw_stats_bar(self.screen, 30, 40, 150, 15, self.player.hp, self.player.max_hp, BLOOD_RED, "HP")
        draw_stats_bar(self.screen, 220, 40, 150, 15, self.player.sanity, 100, TEMPLE_BLUE, "SANITY")
        
        inv_rect = pygame.Rect(WIDTH - 250, 20, 220, 40)
        pygame.draw.rect(self.screen, STONE, inv_rect, border_radius=5)
        pygame.draw.rect(self.screen, GOLD, inv_rect, width=2, border_radius=5)
        
        inv_text = "Satchel: " + (", ".join(self.player.inventory) if self.player.inventory else "Empty")
        inv_surf = BUTTON_FONT.render(inv_text, True, WHITE)
        self.screen.blit(inv_surf, (inv_rect.x + 15, inv_rect.y + 10))

    def draw_character(self):
        bob = 0
        if self.state == "TRANSITION":
            bob = (self.char_x % 40) // 10 
        pygame.draw.rect(self.screen, KHAKI, (self.char_x, self.char_y - bob, 30, 50), border_radius=5)
        pygame.draw.rect(self.screen, LEATHER, (self.char_x + 5, self.char_y + 20 - bob, 20, 15))
        pygame.draw.rect(self.screen, LEATHER, (self.char_x - 5, self.char_y - 5 - bob, 40, 10), border_radius=2)
        pygame.draw.circle(self.screen, GOLD, (self.char_x + 35, self.char_y + 15 - bob), 6)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Event Delegation based on state
                if self.state in ["START_SCREEN", "LOAD_MENU", "SAVE_MENU", "INPUT_NAME"]:
                    for btn in self.menu_buttons: btn.handle_event(event)
                    if self.state == "INPUT_NAME": self.input_box.handle_event(event)
                elif self.state == "IDLE":
                    for btn in self.buttons: btn.handle_event(event)

            if self.state == "TRANSITION":
                self.char_x += 12  
                if self.char_x > WIDTH + 50:
                    self.state = "IDLE"
                    self.apply_node_logic()  

            # DRAWING LOGIC
            self.screen.fill(JUNGLE_DARK) 

            if self.state in ["START_SCREEN", "LOAD_MENU"]:
                draw_start_screen_graphics(self.screen)
                if self.state == "START_SCREEN":
                    draw_visual_novel_ui(self.screen) 
                else: # Dark overlay for load menu
                    pygame.draw.rect(self.screen, (0,0,0, 180), (0,0,WIDTH,HEIGHT))
                    title = TITLE_FONT.render("LOAD GAME", True, WHITE)
                    self.screen.blit(title, title.get_rect(center=(WIDTH//2, 80)))
                
                for btn in self.menu_buttons: btn.draw(self.screen)

            elif self.state in ["SAVE_MENU", "INPUT_NAME"]:
                # Draw the game in background so it feels like a pause menu
                pygame.draw.rect(self.screen, STONE, (0, self.char_y + 50, WIDTH, TEXT_BOX_Y - (self.char_y + 50)))
                self.draw_character()
                self.draw_hud()
                draw_visual_novel_ui(self.screen)
                
                # Overlay
                s = pygame.Surface((WIDTH,HEIGHT))
                s.set_alpha(200)
                s.fill((0,0,0))
                self.screen.blit(s, (0,0))
                
                if self.state == "SAVE_MENU":
                    title = TITLE_FONT.render("SAVE GAME", True, GOLD)
                    self.screen.blit(title, title.get_rect(center=(WIDTH//2, 80)))
                else:
                    title = TITLE_FONT.render("NAME YOUR SAVE", True, GOLD)
                    self.screen.blit(title, title.get_rect(center=(WIDTH//2, 100)))
                    self.input_box.draw(self.screen)

                for btn in self.menu_buttons: btn.draw(self.screen)

            else: # Game Active States (IDLE / TRANSITION)
                pygame.draw.rect(self.screen, STONE, (0, self.char_y + 50, WIDTH, TEXT_BOX_Y - (self.char_y + 50)))
                pygame.draw.line(self.screen, MOSS_GREEN, (0, self.char_y + 50), (WIDTH, self.char_y + 50), 3) 
                
                self.draw_character()
                self.draw_hud()

                if self.state == "IDLE":
                    draw_visual_novel_ui(self.screen)
                    node_data = get_story_node(self.current_node)
                    text_to_draw = node_data["text"] if node_data else "Error loading story."
                    
                    if self.player.is_dead():
                        text_to_draw = "THE JUNGLE HAS CLAIMED YOU.\n\nGAME OVER."

                    draw_text_wrapped(self.screen, text_to_draw, 40, TEXT_BOX_Y + 40, WIDTH - 340)
                    for btn in self.buttons: btn.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = GameApp()
    game.run()