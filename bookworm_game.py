"""
Bookworm Python Edition
======================
A single-file tkinter word-puzzle game inspired by the classic arcade
"Bookworm".  The player forms valid words by clicking adjacent tiles on
an 8x8 board, then submits the word to earn points.  Cleared tiles
fall, new letters spawn at the top, and every few turns a "burning
tile" hazard ignites, forcing the player to defend the bottom row.

Requirements: Python 3.8+ with the standard tkinter library only.
Run with:  python bookworm_game.py
"""

import random
import tkinter as tk
from tkinter import messagebox, font as tkfont

# ----------------------------------------------------------------------------
# Dictionary
# ----------------------------------------------------------------------------
COMMON_WORDS = {
    "CAT", "DOG", "BAT", "RAT", "MAT", "HAT", "FAN", "PAN", "TAN", "VAN",
    "SUN", "SKY", "SEA", "ICE", "SIT", "NET", "WEB", "BOX", "BAG", "CUP",
    "RED", "LON", "GOT", "WIN", "TUB", "HUB", "DUD", "NUT", "PIT", "ROT",
    "BOOK", "WORM", "READ", "PAGE", "WORD", "GAME", "PLAY", "GRID", "TILE",
    "FIRE", "BURN", "HEAT", "WARM", "GLOW", "GOLD", "STAR", "MOON", "TIME",
    "LAND", "WIND", "COLD", "SNOW", "RAIN", "MIST", "LAVA", "OAK", "BIRD",
    "LION", "BEAR", "WOLF", "BOAR", "ASH", "OWL", "MAP", "PIN", "TEN",
    "CODE", "DATA", "BYTE", "FILE", "NODE", "LINK", "LOOP", "PATH", "APPLE",
    "PEAR", "GRAPE", "LEMON", "PEACH", "MANGO", "BERRY", "WATER", "EARTH",
    "PLANT", "FLOWN", "TREE", "RIVER", "OCEAN", "CLOUD", "LIGHT",
    "DARK", "NIGHT", "DREAM", "SLEEP", "POWER", "FORCE", "MAGIC", "DRAIN",
    "KNIGHT", "CASTLE", "SHIELD", "SWORD", "SPELL", "WIZARD",
    "PYTHON", "GUILD", "QUEST", "SCORES", "BONUS", "LETTER", "PUZZLE",
    "FROST", "BLAZE", "EMBER", "SPARK", "THORN", "CROWN", "GRIME", "HONEY",
    "FOREST", "BLAZING", "CROWNS", "SPARKLES", "DRAGONFLY", "KNIGHTHOOD"
}

LETTER_SCORES = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10
}

LETTER_POOL = (
    "A"*9 + "B"*2 + "C"*2 + "D"*4 + "E"*12 + "F"*2 + "G"*3 + "H"*2 + "I"*9 +
    "J"*1 + "K"*1 + "L"*4 + "M"*2 + "N"*6 + "O"*8 + "P"*2 + "Q"*1 + "R"*6 +
    "S"*4 + "T"*6 + "U"*4 + "V"*2 + "W"*2 + "X"*1 + "Y"*2 + "Z"*1
)

GRID_ROWS = 8
GRID_COLS = 8

MIN_WORD_LEN      = 3
WORD_LENGTH_BONUS = 10
BURNING_TICK_MS   = 1000
BURNING_EVERY_N   = 3

# ---- Visual / animation tuning -------------------------------------------
TILE_W            = 46         # pixel width of a single tile
TILE_H            = 46         # pixel height of a single tile
TILE_GAP          = 6          # spacing between tiles
PANEL_PAD         = 8          # padding around the canvas board
GRID_W            = GRID_COLS * TILE_W + (GRID_COLS - 1) * TILE_GAP + 2 * PANEL_PAD
GRID_H            = GRID_ROWS * TILE_H + (GRID_ROWS - 1) * TILE_GAP + 2 * PANEL_PAD
FALL_FRAME_MS     = 16         # frame interval for the fall animation
FALL_STEPS        = 6          # number of tween frames per tile drop
FLAME_FRAME_MS    = 90        # interval for the flame flicker
FLAME_HEIGHTS     = (10, 14, 18, 12, 16, 9)   # cycling flame "flame" heights
CHAIN_COLOR       = "#f1c40f"  # golden snake line through selected tiles
CHAIN_WIDTH       = 5
HUD_H             = 34        # height of the live HUD strip
GAME_OVER_DELAY   = 1200      # pause before the modal appears

LEVEL_SCORE_STEP  = 500       # score threshold between arcade levels

COL_BG          = "#1a1a2e"
COL_DASHBOARD   = "#16213e"
COL_ACCENT      = "#0f3460"
COL_TILE        = "#e67e22"
COL_TILE_ACTIVE = "#d35400"
COL_SELECTED    = "#3498db"
COL_SELECTED_ACT= "#2980b9"
COL_BURNING     = "#e74c3c"
COL_BURNING_ACT = "#c0392b"
COL_TEXT        = "#ecf0f1"
COL_SCORE       = "#f1c40f"
COL_HEADER      = "#2c3e50"
COL_SUBMIT      = "#2ecc71"
COL_SUBMIT_ACT  = "#27ae60"
COL_CLEAR       = "#e74c3c"
COL_CLEAR_ACT   = "#c0392b"
COL_RESTART     = "#9b59b6"
COL_RESTART_ACT = "#8e44ad"
COL_HUD         = "#0f3460"
COL_HUD_TEXT    = "#ecf0f1"
COL_HUD_ACCENT  = "#f39c12"
COL_FLAME_OUT   = "#e74c3c"
COL_FLAME_MID   = "#f39c12"
COL_FLAME_IN    = "#f1c40f"
COL_SPAWN       = "#2ecc71"
COL_LEVEL       = "#9b59b6"
COL_TIMER       = "#1abc9c"
COL_DANGER      = "#e74c3c"

class BookwormGame:
    """Bookworm-style word puzzle game rendered with tkinter widgets."""

    def __init__(self, root):
        self.root = root
        self.root.title("Bookworm Python Edition")
        self.root.resizable(False, False)
        self.root.configure(bg=COL_BG)

        self.score = 0
        self.selected_pos = []
        self.grid_data = [[None] * GRID_COLS for _ in range(GRID_ROWS)]

        self.burning_set    = set()
        self.turns_since_burn = 0
        self.burning_timer  = None
        self.game_over      = False
        self.level          = 1
        self.words_found    = 0
        self.elapsed_ms     = 0
        self.timer_id       = None
        self.animating      = False

        # Canvas items created during the run
        self.tile_items     = {}   # (r,c) -> [rect, letter, pts, flame, outline]
        self.chain_item     = None
        self.float_items    = []
        self.flame_phase    = 0
        self.flame_id       = None

        self.setup_ui()
        self.init_grid()
        self._start_clock()
        self._start_flame_loop()

    # ---- UI construction ----
    def setup_ui(self):
        """Lay out the retro-arcade dashboard: HUD, canvas board, controls."""

        # ---- Live HUD strip: word / score / level / timer / burn ----
        hud = tk.Frame(self.root, bg=COL_HUD, height=HUD_H)
        hud.pack(fill=tk.X, padx=10, pady=(8, 2))
        hud.pack_propagate(False)

        def _hud_box(text, fg):
            f = tk.Frame(hud, bg=COL_HUD)
            f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2, pady=4)
            label = tk.Label(
                f, text=text, font=("Helvetica", 11, "bold"),
                fg=fg, bg=COL_HUD, anchor="w",
            )
            label.pack(side=tk.LEFT)
            return label

        self.hud_word   = _hud_box("WORD: ---", COL_HUD_TEXT)
        self.hud_score  = _hud_box("SCORE: 0", COL_HUD_ACCENT)
        self.hud_level  = _hud_box("LVL 1", COL_LEVEL)
        self.hud_time   = _hud_box("TIME 0:00", COL_TIMER)
        self.hud_burn   = _hud_box("CLEAR", COL_HUD_TEXT)

        # ---- Canvas game board (animated tiles, chain line, flames) ----
        canvas = tk.Canvas(
            self.root, width=GRID_W, height=GRID_H,
            bg=COL_DASHBOARD, highlightthickness=0, borderwidth=0,
        )
        canvas.pack(padx=10, pady=2)
        self.canvas = canvas
        self._create_grid_items()
        self.canvas.tag_lower("chain")
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # ---- Control buttons ----
        ctrl = tk.Frame(self.root, bg=COL_DASHBOARD)
        ctrl.pack(fill=tk.X, padx=10, pady=10)

        submit_btn = tk.Button(
            ctrl, text="SUBMIT WORD",
            font=("Helvetica", 12, "bold"),
            bg=COL_SUBMIT, fg="white",
            activebackground=COL_SUBMIT_ACT, activeforeground="white",
            relief="raised", bd=2,
            command=self.submit_word,
        )
        submit_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        clear_btn = tk.Button(
            ctrl, text="CLEAR SELECTION",
            font=("Helvetica", 12, "bold"),
            bg=COL_CLEAR, fg="white",
            activebackground=COL_CLEAR_ACT, activeforeground="white",
            relief="raised", bd=2,
            command=self.clear_selection,
        )
        clear_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        restart_btn = tk.Button(
            ctrl, text="RESTART",
            font=("Helvetica", 12, "bold"),
            bg=COL_RESTART, fg="white",
            activebackground=COL_RESTART_ACT, activeforeground="white",
            relief="raised", bd=2,
            command=self.restart_game,
        )
        restart_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)

    def get_random_letter(self):
        """Return a weighted-random uppercase letter."""
        return random.choice(LETTER_POOL)

    # ------------------------------------------------------------------
    # Canvas geometry helpers
    # ------------------------------------------------------------------
    def _tile_origin(self, r, c):
        """Top-left canvas coordinates of the tile at grid (r, c)."""
        x = PANEL_PAD + c * (TILE_W + TILE_GAP)
        y = PANEL_PAD + r * (TILE_H + TILE_GAP)
        return x, y

    def _tile_center(self, r, c):
        """Center canvas coordinates of the tile at grid (r, c)."""
        x, y = self._tile_origin(r, c)
        return x + TILE_W / 2, y + TILE_H / 2

    def _create_grid_items(self):
        """Create the canvas rectangles, letters, point labels and outlines
        for every tile.  They start hidden until the board is filled."""
        cv = self.canvas
        self.tile_items = {}

        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x, y = self._tile_origin(r, c)
                rect = cv.create_rectangle(
                    x, y, x + TILE_W, y + TILE_H,
                    fill=COL_TILE, outline="#111122", width=2,
                    tags=("tile", f"t{r}-{c}"), state="hidden",
                )
                letter = cv.create_text(
                    x + TILE_W / 2, y + TILE_H / 2 - 6,
                    text="?", font=("Helvetica", 18, "bold"),
                    fill="white", tags=("letter", f"t{r}-{c}"), state="hidden",
                )
                pts = cv.create_text(
                    x + TILE_W / 2, y + TILE_H - 9,
                    text="", font=("Helvetica", 8),
                    fill="#fff3d6", tags=("pts", f"t{r}-{c}"), state="hidden",
                )
                ring = cv.create_rectangle(
                    x - 3, y - 3, x + TILE_W + 3, y + TILE_H + 3,
                    fill="", outline=COL_FLAME_OUT, width=3,
                    tags=("ring", f"t{r}-{c}"), state="hidden",
                )
                self.tile_items[(r, c)] = [rect, letter, pts, ring]

        # Golden snake/chain line, drawn under everything
        self.chain_item = cv.create_line(
            0, 0, 0, 0,
            fill=CHAIN_COLOR, width=CHAIN_WIDTH,
            arrow=tk.LAST, capstyle=tk.ROUND, smooth=True,
            tags=("chain",), state="hidden",
        )

    def init_grid(self):
        """Fill every cell with a random letter and render the board."""
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                self.grid_data[r][c] = self.get_random_letter()
                self._render_tile(r, c)

    def _render_tile(self, r, c, spawn=False, falling=False):
        """Update the canvas items for (r,c) to reflect letter + state."""
        letter = self.grid_data[r][c]
        rect, ltxt, ptxt, ring = self.tile_items[(r, c)]
        x, y = self._tile_origin(r, c)

        self.canvas.itemconfigure(
            ltxt, text=letter,
            fill=(COL_SPAWN if spawn else "white"),
        )
        self.canvas.itemconfigure(ptxt, text=f"{LETTER_SCORES[letter]}pt")
        # Make all items for this tile visible
        for item in (rect, ltxt, ptxt, ring):
            self.canvas.itemconfigure(item, state="normal")

        if spawn:
            self._flash_tile(r, c)
        elif falling:
            self._animate_fall(r, c)
        else:
            self._paint_tile(r, c)

    def _paint_tile(self, r, c):
        """Re-apply the correct fill for a tile's current state."""
        pos = (r, c)
        _, _, _, ring = self.tile_items[pos]
        if pos in self.selected_pos:
            self.canvas.itemconfigure(
                self.tile_items[pos][0], fill=COL_SELECTED,
            )
        elif pos in self.burning_set:
            self.canvas.itemconfigure(
                self.tile_items[pos][0], fill=COL_BURNING,
            )
            self.canvas.itemconfigure(ring, state="normal")
        else:
            self.canvas.itemconfigure(self.tile_items[pos][0], fill=COL_TILE)
            self.canvas.itemconfigure(ring, state="hidden")
        self._draw_chain()

    def _flash_tile(self, r, c):
        """Brief green -> orange settle after a spawn."""
        pos = (r, c)
        rect = self.tile_items[pos][0]
        self.canvas.itemconfigure(rect, fill=COL_SPAWN)
        self.canvas.after(
            240,
            lambda: self._paint_tile(r, c),
        )

    def _animate_fall(self, r, c):
        """Tween the tile from above the board down to (r, c)."""
        pos = (r, c)
        rect, ltxt, ptxt, ring = self.tile_items[pos]
        x, y = self._tile_origin(r, c)
        start_y = y - TILE_H
        steps = FALL_STEPS

        def step(i):
            if i >= steps:
                self.canvas.coords(rect, x, y, x + TILE_W, y + TILE_H)
                self.canvas.coords(ltxt, x + TILE_W / 2, y + TILE_H / 2 - 6)
                self.canvas.coords(ptxt, x + TILE_W / 2, y + TILE_H - 9)
                self._paint_tile(r, c)
                return
            t = i / (steps - 1)
            ease = t * t
            cy = start_y + (y - start_y) * ease
            self.canvas.coords(rect, x, cy, x + TILE_W, cy + TILE_H)
            self.canvas.coords(ltxt, x + TILE_W / 2, cy + TILE_H / 2 - 6)
            self.canvas.coords(ptxt, x + TILE_W / 2, cy + TILE_H - 9)
            self.canvas.after(FALL_FRAME_MS, lambda: step(i + 1))

        self.canvas.itemconfigure(rect, fill=COL_TILE)
        step(0)

    def _draw_chain(self):
        """Draw the golden snake line through selected tiles, else hide it."""
        cv = self.canvas
        if len(self.selected_pos) >= 2:
            coords = []
            for r, c in self.selected_pos:
                cx, cy = self._tile_center(r, c)
                coords.extend((cx, cy))
            cv.coords(self.chain_item, *coords)
            cv.itemconfigure(self.chain_item, state="normal")
        else:
            cv.itemconfigure(self.chain_item, state="hidden")

    def _spawn_float(self, r, c, text, color=COL_SPAWN):
        """Pop a floating label that drifts up and disappears."""
        cx, cy = self._tile_center(r, c)
        item = self.canvas.create_text(
            cx, cy - 10, text=text,
            font=("Helvetica", 13, "bold"), fill=color,
            tags=("float",),
        )

        def rise(offset):
            if offset > 26:
                self.canvas.delete(item)
                return
            self.canvas.coords(item, cx, cy - 10 - offset)
            self.canvas.after(40, lambda: rise(offset + 4))

        rise(0)

    def _on_canvas_click(self, event):
        """Translate a canvas click into a tile click."""
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                x, y = self._tile_origin(r, c)
                if x <= event.x <= x + TILE_W and y <= event.y <= y + TILE_H:
                    self.on_tile_click(r, c)
                    return


    @staticmethod
    def is_adjacent(p1, p2):
        """Two positions are adjacent if they share a side or a corner."""
        r1, c1 = p1
        r2, c2 = p2
        return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1

    def on_tile_click(self, r, c):
        """Handle a click on the tile at (r, c)."""
        if self.game_over or self.animating:
            return

        pos = (r, c)

        # Clicking the tail of the chain deselects it
        if self.selected_pos and self.selected_pos[-1] == pos:
            self.selected_pos.pop()
            self._paint_tile(r, c)
            self._update_word_display()
            return

        # New clicks must be adjacent to the current tail
        if self.selected_pos:
            if not self.is_adjacent(self.selected_pos[-1], pos):
                return

        # A tile already in the chain cannot be re-selected
        if pos in self.selected_pos:
            return

        self.selected_pos.append(pos)
        self._paint_tile(r, c)
        self._update_word_display()

    def _update_word_display(self):
        word = "".join(self.grid_data[r][c] for r, c in self.selected_pos)
        self.hud_word.config(
            text=f"WORD: {word or '---'}",
            fg=COL_SCORE if word else COL_HUD_TEXT,
        )
        self._draw_chain()

    def clear_selection(self):
        for r, c in self.selected_pos:
            self._paint_tile(r, c)
        self.selected_pos = []
        self._update_word_display()

    def submit_word(self):
        """Validate the selected chain, score it, drop tiles, advance turns."""
        if self.game_over or self.animating:
            return

        word = "".join(self.grid_data[r][c] for r, c in self.selected_pos)

        # Too short – clear and nudge the player
        if len(word) < MIN_WORD_LEN:
            messagebox.showwarning(
                "Too Short",
                f"Words must be at least {MIN_WORD_LEN} letters long!"
            )
            self.clear_selection()
            return

        if word not in COMMON_WORDS:
            messagebox.showerror(
                "Invalid Word",
                f"'{word}' was not found in the dictionary."
            )
            self.clear_selection()
            return

        # Score: (sum of letter points + length bonus) scaled by level
        raw = sum(LETTER_SCORES[ch] for ch in word)
        length_bonus = max(0, len(word) - MIN_WORD_LEN) * WORD_LENGTH_BONUS
        gained = (raw + length_bonus) * self.level
        self.score += gained
        self.words_found += 1

        # Bump the level as the player scores more
        new_level = self.score // LEVEL_SCORE_STEP + 1
        if new_level > self.level:
            self.level = new_level
            self._flash_level()

        self._update_hud()

        # Pop a floating score label over the tail tile
        tail_r, tail_c = self.selected_pos[-1]
        self._spawn_float(tail_r, tail_c, f"+{gained}", COL_SPAWN)

        # Remember which columns were affected, then clear selection
        cleared_cols = set(c for _, c in self.selected_pos)
        self.clear_selection()
        self._apply_gravity_animated(cleared_cols)

        # Advance the turn counter and possibly ignite a burning tile
        self.turns_since_burn += 1
        if self.turns_since_burn >= BURNING_EVERY_N:
            self.turns_since_burn = 0
            self.ignite_burning_tile()

        # Keep the burning hazard ticking
        self._schedule_burning_tick()

    def _apply_gravity_animated(self, cols_to_update):
        """For each affected column, surviving tiles fall with an animation
        and new letters spawn at the top."""
        self.animating = True
        self.root.after(0, lambda: self._do_gravity(cols_to_update))

    def _do_gravity(self, cols_to_update):
        for c in cols_to_update:
            # Collect surviving letters bottom-to-top (skip selected & burning)
            surviving = [
                self.grid_data[r][c]
                for r in range(GRID_ROWS - 1, -1, -1)
                if (r, c) not in self.selected_pos
                and (r, c) not in self.burning_set
            ]
            n_fall = len(surviving)
            # Survivors keep their letters; spawn new letters for the gaps
            while len(surviving) < GRID_ROWS:
                surviving.append(self.get_random_letter())

            for r in range(GRID_ROWS - 1, -1, -1):
                letter = surviving.pop()
                self.grid_data[r][c] = letter
                # Topmost rows receive fresh spawns; lower rows just shift down
                if r >= n_fall:
                    self._render_tile(r, c, spawn=True, falling=True)
                else:
                    self._render_tile(r, c, falling=True)

        # Let the animations finish before re-enabling input
        self.root.after(
            FALL_FRAME_MS * (FALL_STEPS + 1),
            self._finish_gravity,
        )

    def _finish_gravity(self):
        self.animating = False

    # ------------------------------------------------------------------
    # Burning-tile hazard
    # ------------------------------------------------------------------
    def ignite_burning_tile(self):
        """Pick a random non-bottom-row tile and mark it as burning."""
        candidates = [
            (r, c)
            for r in range(GRID_ROWS - 1)
            for c in range(GRID_COLS)
            if (r, c) not in self.burning_set
        ]
        if not candidates:
            return
        tile = random.choice(candidates)
        self.burning_set.add(tile)
        self._paint_tile(*tile)
        self._update_hud()

    def _burning_tick(self):
        """Every BURNING_TICK_MS the burning tiles drop one row.
        If any reaches the bottom row the game is over."""
        if self.game_over:
            return

        new_set = set()
        for (r, c) in self.burning_set:
            new_r = r + 1
            if new_r >= GRID_ROWS:
                self._end_game()
                return
            new_set.add((new_r, c))

        self.burning_set = new_set
        for r, c in self.burning_set:
            self._paint_tile(r, c)
        self._update_hud()

        # Schedule the next tick
        self.burning_timer = self.root.after(
            BURNING_TICK_MS, self._burning_tick
        )

    def _schedule_burning_tick(self):
        """Ensure the burning tick loop is running (idempotent)."""
        if self.burning_timer is None and self.burning_set:
            self.burning_timer = self.root.after(
                BURNING_TICK_MS, self._burning_tick
            )

    # ------------------------------------------------------------------
    # Flame animation
    # ------------------------------------------------------------------
    def _start_flame_loop(self):
        """Run a recurring loop that cycles the flame look on burning tiles."""
        if self.flame_id is None:
            self._flame_step()

    def _flame_step(self):
        """Advance one flame-flicker frame."""
        self.flame_phase = (self.flame_phase + 1) % len(FLAME_HEIGHTS)
        for (r, c) in self.burning_set:
            ring = self.tile_items[(r, c)][3]
            if self.canvas.type(ring) == "rectangle":
                # Pulse the ring outline width for a flicker effect
                self.canvas.itemconfigure(ring, width=1 + (self.flame_phase % 3))
        self.flame_id = self.root.after(FLAME_FRAME_MS, self._flame_step)

    # ------------------------------------------------------------------
    # HUD & timers
    # ------------------------------------------------------------------
    def _start_clock(self):
        """Start the game timer that ticks the HUD clock every second."""
        if self.timer_id is None:
            self._tick_clock()

    def _tick_clock(self):
        if self.game_over:
            return
        self.elapsed_ms += 1000
        self._update_hud()
        self.timer_id = self.root.after(1000, self._tick_clock)

    def _update_hud(self):
        """Refresh every live HUD readout."""
        word = "".join(self.grid_data[r][c] for r, c in self.selected_pos)
        self.hud_word.config(
            text=f"WORD: {word or '---'}",
            fg=COL_SCORE if word else COL_HUD_TEXT,
        )
        self.hud_score.config(text=f"SCORE: {self.score}")
        self.hud_level.config(text=f"LVL {self.level}")

        secs = self.elapsed_ms // 1000
        self.hud_time.config(text=f"TIME {secs // 60}:{secs % 60:02d}")

        if self.burning_set:
            self.hud_burn.config(text="BURNING!", fg=COL_DANGER)
        else:
            self.hud_burn.config(text="CLEAR", fg=COL_HUD_TEXT)

    def _flash_level(self):
        """Briefly highlight the level box when the player levels up."""
        self.hud_level.config(fg="white")
        self.root.after(600, lambda: self.hud_level.config(fg=COL_LEVEL))


    # ------------------------------------------------------------------
    # Game over / restart
    # ------------------------------------------------------------------
    def _end_game(self):
        """Freeze the board, stop timers, and show the game-over dialog."""
        self.game_over = True
        self.animating = False
        if self.burning_timer is not None:
            self.root.after_cancel(self.burning_timer)
            self.burning_timer = None
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        if self.flame_id is not None:
            self.root.after_cancel(self.flame_id)
            self.flame_id = None

        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                rect = self.tile_items[(r, c)][0]
                self.canvas.itemconfigure(rect, fill="#3a3a4a", outline="#111122")

        # Big GAME OVER banner across the board
        self.canvas.create_text(
            GRID_W / 2, GRID_H / 2,
            text="GAME OVER", font=("Helvetica", 32, "bold"),
            fill=COL_DANGER, tags=("gameover",),
        )

        self._update_hud()
        self.root.after(
            GAME_OVER_DELAY,
            lambda: messagebox.showerror(
                "Game Over",
                f"A burning tile reached the bottom row!\n"
                f"Final score: {self.score}   Level {self.level}",
            ),
        )

    def restart_game(self):
        """Reset every piece of state and repopulate the board."""
        if self.burning_timer is not None:
            self.root.after_cancel(self.burning_timer)
            self.burning_timer = None
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        if self.flame_id is not None:
            self.root.after_cancel(self.flame_id)
            self.flame_id = None

        self.score = 0
        self.selected_pos = []
        self.burning_set = set()
        self.turns_since_burn = 0
        self.game_over = False
        self.level = 1
        self.words_found = 0
        self.elapsed_ms = 0
        self.animating = False

        # Clear the game-over banner and any leftover floating labels
        self.canvas.delete("gameover")
        for it in list(self.float_items):
            self.canvas.delete(it)
        self.float_items = []

        # Re-enable all tile rectangles
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                self._paint_tile(r, c)

        # Restart the recurring loops
        self._start_clock()
        self._start_flame_loop()
        self._update_hud()
        self.init_grid()

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------
    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    game = BookwormGame(root)
    game.run()


if __name__ == "__main__":
    main()
