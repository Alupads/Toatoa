# ui.py
import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, on_click_callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click_callback

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)
        
        bg_color = STONE_LIGHT if hovered else STONE
        border_color = MOSS_GREEN if hovered else GOLD
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (20, 25, 20), self.rect, width=3, border_radius=4)
        pygame.draw.rect(surface, border_color, self.rect, width=1, border_radius=4)
        
        text_surf = BUTTON_FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

# --- NEW: TEXT INPUT BOX ---
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = MOSS_GREEN
        self.text = text
        self.txt_surface = TEXT_FONT.render(text, True, WHITE)
        self.active = True # Always active for simplicity in this menu

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                pass # Handled by a separate save button
            else:
                # Limit name length
                if len(self.text) < 15: 
                    self.text += event.unicode
            self.txt_surface = TEXT_FONT.render(self.text, True, WHITE)

    def draw(self, screen):
        pygame.draw.rect(screen, STONE, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))

def draw_visual_novel_ui(surface):
    box_rect = pygame.Rect(0, TEXT_BOX_Y, WIDTH, TEXT_BOX_HEIGHT)
    pygame.draw.rect(surface, STONE, box_rect)
    inner_rect = box_rect.inflate(-20, -20)
    pygame.draw.rect(surface, (25, 30, 25), inner_rect, border_radius=5)
    pygame.draw.rect(surface, GOLD, box_rect, width=4)
    pygame.draw.line(surface, MOSS_GREEN, (10, TEXT_BOX_Y + 10), (WIDTH - 10, TEXT_BOX_Y + 10), 2)

def draw_text_wrapped(surface, text, x, y, max_width, color=WHITE):
    paragraphs = text.split('\n')
    current_y = y
    
    for paragraph in paragraphs:
        words = paragraph.split(' ')
        line = []
        for word in words:
            line.append(word)
            fw, fh = TEXT_FONT.size(' '.join(line))
            if fw > max_width:
                line.pop()
                surface.blit(TEXT_FONT.render(' '.join(line), True, color), (x, current_y))
                line = [word]
                current_y += fh + 4
        if line:
            surface.blit(TEXT_FONT.render(' '.join(line), True, color), (x, current_y))
            current_y += fh + 4
        current_y += 10 

def draw_stats_bar(surface, x, y, width, height, current_val, max_val, color, label):
    frame_rect = pygame.Rect(x - 4, y - 4, width + 8, height + 8)
    pygame.draw.rect(surface, STONE_LIGHT, frame_rect, border_radius=3)
    pygame.draw.rect(surface, (10, 10, 10), (x, y, width, height))
    fill_width = max(0, int((current_val / max_val) * width))
    pygame.draw.rect(surface, color, (x, y, fill_width, height))
    label_surf = BUTTON_FONT.render(label, True, WHITE)
    surface.blit(label_surf, (x, y - 22))

def draw_start_screen_graphics(surface):
    surface.fill(JUNGLE_DARK) 
    for i in range(8):
        pygame.draw.circle(surface, (15, 35, 20), (i * 120, 100), 150)
    cx = WIDTH // 2
    pygame.draw.polygon(surface, STONE, [(cx - 150, 400), (cx + 150, 400), (cx + 120, 320), (cx - 120, 320)])
    pygame.draw.polygon(surface, STONE_LIGHT, [(cx - 100, 320), (cx + 100, 320), (cx + 70, 240), (cx - 70, 240)])
    pygame.draw.polygon(surface, GOLD, [(cx - 40, 240), (cx + 40, 240), (cx + 30, 180), (cx - 30, 180)])
    pygame.draw.rect(surface, (5, 5, 5), (cx - 20, 350, 40, 50))
    for i in range(6):
        start_x = i * 160 + 40
        pygame.draw.line(surface, MOSS_GREEN, (start_x, 0), (start_x + 20, 180), 8)
        pygame.draw.line(surface, JUNGLE_DARK, (start_x + 30, 0), (start_x + 10, 220), 5)
    title_text = "TEMPLE ESCAPE RPG"
    shadow_surf = TITLE_FONT.render(title_text, True, (0, 0, 0))
    title_surf = TITLE_FONT.render(title_text, True, GOLD)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
    surface.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
    surface.blit(title_surf, title_rect)