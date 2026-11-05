"""
BOOKWORM: ENCHANTED LIBRARY
A polished single-file word puzzle arcade game.
Python 3.8+ | Standard library only (Tkinter)
Run: python bookworm_game.py

Optional: place a plain-text dictionary named words.txt beside this file.
One word per line. The built-in word list is used as a fallback.
"""

import random
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

ROWS, COLS = 8, 8
TILE, GAP, PAD = 62, 7, 14
BOARD_W = COLS * TILE + (COLS - 1) * GAP + PAD * 2
BOARD_H = ROWS * TILE + (ROWS - 1) * GAP + PAD * 2
MIN_WORD = 3
BURN_EVERY = 4
BURN_TICK_MS = 1450
ANIM_MS = 16

BG = "#101525"
PANEL = "#19233a"
PANEL_2 = "#202e49"
GOLD = "#ffd166"
CREAM = "#fff4d6"
MUTED = "#9eacc7"
TEAL = "#48c9b0"
RED = "#ff5d67"
PURPLE = "#a78bfa"
TILE_COLORS = ["#e6a23c", "#d98736", "#c77d32"]

WORDS = set("""
ACE ACT ADD AGE AGO AIR ALL AND ANT ANY APE ARC ARE ARM ART ASK ATE BAD BAG
BAR BAT BAY BED BEE BEG BET BIG BIN BIT BOW BOX BOY BUS BUT BUY CAB CAN CAP
CAR CAT COP COT COW CUB CUP CUT DAY DEN DID DIE DIG DIM DIP DOG DOT DRY DUE
EAR EAT EGG EGO ELF END ERA EVE EYE FAN FAR FAT FED FEE FEW FIG FIN FIT FIX
FLY FOG FOR FOX FUN GAP GAS GEL GEM GET GIG GOD GOT GUM GUN GUY GYM HAD
HAM HAS HAT HEN HER HID HIM HIP HIS HIT HOG HOP HOT HOW HUB HUG HUT ICE
ICY ILL INK INN ION ITS JAM JAR JAW JAY JET JOB JOG JOY KEY KID KIT LAB
LAD LAG LAP LAW LAY LED LEG LET LID LIE LIP LIT LOG LOT LOW MAD MAN MAP
MAT MAY MEN MET MIX MOB MOM MOP MUD MUG NAG NAP NET NEW NOD NOR NOT NOW
NUN NUT OAK OAR OAT ODD OFF OIL OLD ONE OPT OUR OUT OWE OWN PAD PAL PAN
PAT PAW PAY PEA PEG PEN PET PIE PIG PIN PIT POD POP POT PRO PUB PUG PUN
PUP PUT RAG RAM RAN RAP RAT RAW RAY RED RID RIG RIP ROB ROD ROT ROW RUB
RUG RUM RUN SAD SAG SAP SAT SAW SAY SEA SEE SET SEW SHE SHY SIN SIP SIR
SIT SIX SKI SKY SLY SOB SOD SON SOP SOW SOY SPA SPY SUB SUE SUM SUN
TAB TAG TAN TAP TAR TAX TEA TEN THE TIE TIN TIP TOE TON TOO TOP TOY TRY
TUB TUG TWO USE VAN VAT VET VEX VIA VIE VOW WAR WAS WAY WEB WED WET WHO
WHY WIN WIT WOK WON WOW YAK YAM YAP YES YET YOU ZAP ZEN ZIP ZOO
ABLE ACID ACRE AGED ALSO AREA ARMY AWAY BABY BACK BALL BAND BANK BASE
BATH BEAM BEAN BEAR BEAT BEEN BELL BELT BEST BILL BIRD BLOW BLUE BOAT BODY
BOLD BONE BOOK BOOT BORN BOWL BURN BUSY CALL CALM CAME CAMP CARD CARE
CART CASE CASH CAST CAVE CELL CENT CHAT CHEF CHIP CITY CLAY CLUB COAL COAT
CODE COLD COME COOK COOL COPY CORD CORE COST COVE CROP CURE DARK DATA DATE
DAWN DAYS DEAD DEAL DEAR DEBT DECK DEEP DEER DESK DIAL DIET DIRT DISH
DOOR DOWN DRAW DROP DRUM DUAL DUCK DUST EACH EARN EAST EASY EDGE ELSE
EVEN EVER EVIL EXIT FACE FACT FAIR FALL FAME FARM FAST FATE FEAR FEED
FEEL FILE FILL FILM FIND FINE FIRE FIRM FISH FIVE FLAG FLAT FLOW FOOD
FOOT FORM FORT FOUR FREE FROG FROM FUEL FULL FUND GAIN GAME GATE GAVE
GEAR GIFT GIRL GIVE GLAD GOAL GOAT GOES GOLD GOLF GONE GOOD GRAB GRAY
GREW GRID GROW GULF HAIR HALF HALL HAND HANG HARD HARM HATE HAVE HEAD
HEAL HEAR HEAT HEAVY HELD HELP HERE HERO HIGH HILL HINT HIRE HOLD HOLE
HOME HOPE HOST HOUR HUGE HUNT HURT IDEA INTO IRON ITEM JACK JAIL JOIN
JOKE JUMP JUNE JUST KEEN KEEP KICK KIND KING KITE KNEW KNOW LACK LADY
LAKE LAMB LAMP LAND LANE LAST LATE LEAD LEAF LEAN LEFT LEND LENS LESS
LIFE LIFT LIKE LINE LINK LION LIST LIVE LOAD LOAN LOCK LOGO LONG LOOK
LORD LOSE LOSS LOST LOVE LUCK MADE MAIL MAIN MAKE MALE MANY MARK MASK
MASS MATE MATH MEAL MEAN MEAT MEET MELT MENU MILE MILK MIND MINE MISS
MODE MOOD MOON MORE MOST MOVE MUCH MUST MYTH NAME NEAR NEAT NECK NEED
NEST NEWS NEXT NICE NINE NODE NOON NOTE ONCE ONLY OPEN OVER PACK PAGE
PAID PAIN PAIR PALM PANE PARK PART PASS PAST PATH PEAK PICK PILE PINK
PIPE PLAN PLAY PLOT PLUG PLUS POEM POET POLE POOL POOR PORT POST PULL
PURE PUSH RACE RACK RAGE RAIN RANK RATE READ REAL REAR REED REST RICE
RICH RIDE RING RISE RISK ROAD ROCK ROLE ROOF ROOM ROOT ROSE RULE SAFE
SAGE SAID SAIL SALE SAME SAND SAVE SEAL SEAT SEED SEEK SEEM SEEN SELF
SELL SEND SENT SHIP SHOE SHOP SHOT SHOW SHUT SIDE SIGN SILK SING SINK
SITE SIZE SKIN SLAM SLIP SLOW SNOW SOFT SOIL SOLD SOME SONG SOON SORT
SOUL SPIN SPOT STAR STAY STEP STOP SUCH SUIT SURE TAKE TALE TALK TALL
TANK TAPE TASK TEAM TEAR TELL TEND TERM TEST TEXT THAN THAT THEM THEN
THEY THIN THIS THUS TICK TIDE TIED TIER TILE TIME TINY TOLD TOLL TONE
TOOK TOOL TOUR TOWN TREE TRIP TRUE TUNE TURN TYPE UNIT UPON USED USER
VAST VERY VIEW VINE VOID WAGE WAIT WAKE WALK WALL WANT WARM WASH WAVE
WAYS WEAK WEAR WEEK WELL WENT WERE WEST WHAT WHEN WIDE WIFE WILD WILL
WIND WINE WING WISE WISH WITH WOOD WORD WORK WORM WORN WRAP YEAR YOUR
YARD YARN YAWN YELL YOGA
ABOUT ABOVE ACTOR ACUTE ADMIT ADOPT ADULT AFTER AGAIN AGENT AGREE AHEAD
ALARM ALBUM ALERT ALIVE ALLOW ALONE ALONG ALTER AMONG ANGEL ANGER ANGLE
ANGRY APART APPLE APPLY ARENA ARGUE ARISE ARMOR AROUND ARRAY ASIDE AUDIO
AVOID AWARE BADGE BASIC BEACH BEGIN BEING BELOW BENCH BIRTH BLACK BLAME
BLANK BLAST BLAZE BLEND BLIND BLOCK BLOOD BOARD BRAIN BRAND BREAD BREAK
BRICK BRIDE BRIEF BRING BROAD BROKE BROWN BUILD BUILT CABLE CANDY CARRY
CATCH CAUSE CHAIN CHAIR CHARM CHART CHEAP CHECK CHEST CHIEF CHILD CHINA
CHOIR CHOSE CIVIL CLAIM CLASS CLEAN CLEAR CLERK CLICK CLIMB CLOCK CLOSE
CLOUD COACH COAST COLOR COMET COMIC COUNT COURT COVER CRAFT CRASH CREAM
CRIME CROSS CROWD CROWN CURVE CYCLE DAILY DANCE DATED DEALT DEATH DECAY
DELAY DEPTH DEVIL DIARY DIRTY DOUBT DOZEN DRAFT DRAMA DREAM DRESS DRINK
DRIVE EARLY EARTH EIGHT ELDER ELECT EMPTY ENEMY ENJOY ENTER ENTRY EQUAL
ERROR EVENT EVERY EXACT EXIST EXTRA FAITH FALSE FAULT FIBER FIELD FIFTH
FIFTY FIGHT FINAL FIRST FIXED FLAME FLASH FLEET FLOOR FOCUS FORCE FRAME
FRESH FRONT FRUIT FUNNY GIANT GIVEN GLASS GLOBE GOING GRACE GRADE GRAIN
GRAND GRANT GRASS GREAT GREEN GROUP GROWN GUARD GUESS GUEST GUIDE HABIT
HAPPY HEART HEARD HEAVY HELLO HONEY HORSE HOTEL HOUSE HUMAN HURRY IMAGE
INDEX INNER INPUT ISSUE JEWEL JOINT JUDGE KNIFE KNOWN LABEL LARGE LATER
LAUGH LAYER LEARN LEAST LEAVE LEGAL LEMON LEVEL LIGHT LIMIT LOCAL LOOSE
LOWER LUCKY LUNCH MAGIC MAJOR MAKER MARCH MATCH MAYBE MAYOR MEDIA METAL
MIGHT MINOR MINUS MODEL MONEY MONTH MORAL MOTOR MOUNT MOUSE MOUTH MOVIE
MUSIC NEVER NIGHT NOISE NORTH NOVEL NURSE OCCUR OFFER OFTEN ORDER OTHER
PAINT PANEL PAPER PARTY PEACE PHASE PHONE PHOTO PIECE PILOT PITCH PLACE
PLAIN PLANE PLANT PLATE POINT POWER PRESS PRICE PRIDE PRIME PRINT PRIOR
PRIZE PROOF PROUD QUEEN QUICK QUIET QUITE RADIO RAISE RANGE RAPID RATIO
REACH REACT READY REFER RIGHT RIVER ROBOT ROUND ROUTE ROYAL RURAL SCALE
SCENE SCOPE SCORE SENSE SERVE SEVEN SHALL SHAPE SHARE SHARP SHEET SHELF
SHELL SHIFT SHINE SHIRT SHOCK SHORT SHOWN SIGHT SINCE SKILL SLEEP SLICE
SMALL SMART SMILE SMOKE SOLAR SOLID SOLVE SORRY SOUND SOUTH SPACE SPARE
SPEAK SPEED SPEND SPENT SPICE SPITE SPLIT SPOKE SPORT SPRING SQUAD STAFF
STAGE STAKE STAND START STATE STEAM STEEL STEEP STICK STILL STOCK STONE
STORE STORM STORY STRIP STUDY STUFF STYLE SUGAR SUITE SUPER SWEET TABLE
TAKEN TASTE TEACH THANK THEIR THEME THERE THESE THICK THING THINK THIRD
THOSE THREE THREW THROW TIGHT TIRED TITLE TODAY TOTAL TOUCH TOUGH TOWER
TRACK TRADE TRAIN TREAT TREND TRIAL TRIBE TRICK TRIED TRUST TRUTH TWICE
UNDER UNION UNITY UNTIL UPPER UPSET URBAN USAGE USUAL VALID VALUE VIDEO
VISIT VITAL VOICE WASTE WATCH WATER WEIGH WHERE WHICH WHILE WHITE WHOLE
WHOSE WOMAN WORLD WORRY WORSE WORST WORTH WOULD WRITE WRONG YOUNG
""".split())

LETTER_POINTS = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4,
    "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3,
    "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8,
    "Y": 4, "Z": 10
}
LETTER_BAG = (
    "A"*9 + "B"*2 + "C"*2 + "D"*4 + "E"*12 + "F"*2 + "G"*3 + "H"*2 +
    "I"*9 + "J" + "K" + "L"*4 + "M"*2 + "N"*6 + "O"*8 + "P"*2 + "Q" +
    "R"*6 + "S"*4 + "T"*6 + "U"*4 + "V"*2 + "W"*2 + "X" + "Y"*2 + "Z"
)

def load_dictionary():
    words = set(WORDS)
    path = Path(__file__).with_name("words.txt")
    try:
        words.update(line.strip().upper() for line in path.read_text(encoding="utf-8").splitlines()
                     if line.strip().isalpha() and len(line.strip()) >= MIN_WORD)
    except OSError:
        pass
    return words

class BookwormGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookworm: Enchanted Library")
        self.root.geometry("1120x790")
        self.root.minsize(1000, 740)
        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self.close_game)

        self.dictionary = load_dictionary()
        self.sound_on = True
        self.screen = "menu"
        self.paused = False
        self.particles = []
        self.particle_job = None
        self.clock_job = None
        self.burn_job = None
        self.animating = False
        self.reset_state()
        self.show_menu()
        self.animate_atmosphere()

    def reset_state(self):
        self.score = 0
        self.level = 1
        self.words_found = 0
        self.elapsed = 0
        self.combo = 0
        self.best_combo = 0
        self.turns = 0
        self.selected = []
        self.burning = set()
        self.grid = [[self.random_letter() for _ in range(COLS)] for _ in range(ROWS)]
        self.game_over = False
        self.paused = False
        self.animating = False
        self.last_word = ""
        self.message = "Connect neighboring letters to create a word."
        self.message_color = MUTED

    def random_letter(self):
        return random.choice(LETTER_BAG)

    def clear_root(self):
        for child in self.root.winfo_children():
            child.destroy()

    def make_button(self, parent, text, command, color=TEAL, width=18):
        return tk.Button(parent, text=text, command=command, width=width,
                         bg=color, fg="#101525", activebackground=CREAM,
                         activeforeground=BG, relief="flat", bd=0,
                         font=("Segoe UI", 11, "bold"), cursor="hand2",
                         padx=12, pady=10)

    def show_menu(self):
        self.screen = "menu"
        self.stop_timers()
        self.clear_root()
        shell = tk.Frame(self.root, bg=BG)
        shell.pack(fill="both", expand=True)
        tk.Label(shell, text="✦  THE ENCHANTED LIBRARY  ✦", bg=BG, fg=GOLD,
                 font=("Georgia", 14, "bold")).pack(pady=(78, 16))
        tk.Label(shell, text="BOOKWORM", bg=BG, fg=CREAM,
                 font=("Georgia", 48, "bold")).pack()
        tk.Label(shell, text="A WORD-SPELLING ARCADE ADVENTURE", bg=BG, fg=TEAL,
                 font=("Segoe UI", 12, "bold")).pack(pady=(8, 26))
        art = tk.Canvas(shell, width=520, height=155, bg=BG, highlightthickness=0)
        art.pack(pady=8)
        for i, letter in enumerate("WORD MAGIC"):
            x = 38 + i * 48
            if letter != " ":
                self.draw_tile_art(art, x, 36, letter, 39)
        tk.Label(shell, text="The library is alive. Make words, build combos, and keep the flames away.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 11)).pack(pady=18)
        self.make_button(shell, "▶  PLAY", self.start_game, TEAL, 24).pack(pady=7)
        self.make_button(shell, "⚔  WORM ARENA", self.open_worm_arena, RED, 24).pack(pady=7)
        self.make_button(shell, "HOW TO PLAY", self.show_instructions, GOLD, 24).pack(pady=7)
        self.make_button(shell, "SETTINGS  •  SOUND " + ("ON" if self.sound_on else "OFF"),
                         self.toggle_sound_menu, PURPLE, 24).pack(pady=7)
        tk.Label(shell, text="PYTHON EDITION  •  BUILD YOUR WORD LEGEND",
                 bg=BG, fg="#65728e", font=("Segoe UI", 9, "bold")).pack(side="bottom", pady=24)

    def open_worm_arena(self):
        """Launch the optional word-powered pixel combat mode."""
        self.worm_arena = WormArena(self)

    def draw_tile_art(self, canvas, x, y, letter, size):
        canvas.create_rectangle(x+3, y+5, x+size+3, y+size+5, fill="#080d18", outline="")
        canvas.create_rectangle(x, y, x+size, y+size, fill="#d98b37", outline="#ffcf83", width=2)
        canvas.create_text(x+size/2, y+size/2-2, text=letter, fill="white",
                           font=("Georgia", int(size*.52), "bold"))

    def toggle_sound_menu(self):
        self.sound_on = not self.sound_on
        self.show_menu()

    def show_instructions(self):
        self.screen = "instructions"
        self.stop_timers()
        self.clear_root()
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True, padx=90, pady=55)
        tk.Label(frame, text="HOW TO PLAY", bg=BG, fg=GOLD,
                 font=("Georgia", 30, "bold")).pack(pady=(8, 25))
        instructions = [
            ("1  CONNECT", "Click letters that touch horizontally, vertically, or diagonally."),
            ("2  SPELL", "Create a word with at least three letters, then press SUBMIT or Enter."),
            ("3  SCORE", "Longer words earn bigger bonuses. Consecutive valid words build a combo."),
            ("4  WATCH THE FLAMES", "A burning tile moves downward over time. Clear its column before it reaches the bottom."),
            ("5  LEVEL UP", "Earn points to increase your level. Higher levels make the library more dangerous."),
            ("KEYBOARD", "Enter = submit   •   Backspace = undo last letter   •   Escape = pause")
        ]
        for title, body in instructions:
            block = tk.Frame(frame, bg=PANEL, padx=18, pady=12)
            block.pack(fill="x", pady=6)
            tk.Label(block, text=title, bg=PANEL, fg=TEAL,
                     font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(block, text=body, bg=PANEL, fg=CREAM,
                     font=("Segoe UI", 10), wraplength=760, justify="left").pack(anchor="w", pady=(4, 0))
        self.make_button(frame, "← BACK TO MENU", self.show_menu, GOLD, 22).pack(pady=22)

    def start_game(self):
        self.reset_state()
        self.screen = "game"
        self.clear_root()
        self.build_game_ui()
        self.render_all()
        self.update_hud()
        self.schedule_clock()
        self.schedule_burn()
        self.root.bind("<Return>", lambda e: self.submit_word())
        self.root.bind("<BackSpace>", lambda e: self.undo_selection())
        self.root.bind("<Escape>", lambda e: self.toggle_pause())
        self.root.bind("<space>", lambda e: self.submit_word())

    def build_game_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=22, pady=(15, 8))
        tk.Label(header, text="BOOKWORM", bg=BG, fg=GOLD,
                 font=("Georgia", 21, "bold")).pack(side="left")
        tk.Label(header, text="THE ENCHANTED LIBRARY", bg=BG, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=15, pady=(8, 0))
        self.make_button(header, "Ⅱ  PAUSE", self.toggle_pause, PURPLE, 10).pack(side="right")
        self.make_button(header, "MENU", self.confirm_menu, PANEL_2, 8).pack(side="right", padx=8)

        self.hud = tk.Frame(self.root, bg=PANEL, padx=12, pady=10)
        self.hud.pack(fill="x", padx=22, pady=5)
        self.hud_labels = {}
        for key, label, color in [
            ("score", "SCORE", GOLD), ("level", "LEVEL", PURPLE),
            ("combo", "COMBO", TEAL), ("words", "WORDS", CREAM),
            ("time", "TIME", CREAM), ("danger", "FIRE", RED)
        ]:
            cell = tk.Frame(self.hud, bg=PANEL)
            cell.pack(side="left", expand=True, fill="x")
            tk.Label(cell, text=label, bg=PANEL, fg=MUTED,
                     font=("Segoe UI", 8, "bold")).pack()
            value = tk.Label(cell, text="0", bg=PANEL, fg=color,
                             font=("Segoe UI", 16, "bold"))
            value.pack()
            self.hud_labels[key] = value

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=22, pady=10)
        board_shell = tk.Frame(body, bg="#273650", padx=10, pady=10)
        board_shell.pack(side="left", anchor="n")
        self.canvas = tk.Canvas(board_shell, width=BOARD_W, height=BOARD_H,
                                bg="#172239", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_board_click)

        side = tk.Frame(body, bg=BG, width=285)
        side.pack(side="left", fill="both", expand=True, padx=(18, 0))
        side.pack_propagate(False)
        self.card(side, "SPELL IN PROGRESS", TEAL)
        self.word_label = tk.Label(side, text="—", bg=PANEL, fg=CREAM,
                                   font=("Georgia", 25, "bold"), pady=16)
        self.word_label.pack(fill="x", pady=(0, 12))
        self.word_hint = tk.Label(side, text="Select neighboring letters",
                                  bg=BG, fg=MUTED, font=("Segoe UI", 9))
        self.word_hint.pack(anchor="w", pady=(0, 12))
        self.make_button(side, "✦  SUBMIT WORD", self.submit_word, TEAL, 22).pack(fill="x", pady=4)
        self.make_button(side, "↶  UNDO LAST TILE", self.undo_selection, GOLD, 22).pack(fill="x", pady=4)
        self.make_button(side, "CLEAR SELECTION", self.clear_selection, PANEL_2, 22).pack(fill="x", pady=4)
        self.card(side, "LIBRARY MESSAGE", GOLD)
        self.message_label = tk.Label(side, text=self.message, bg=PANEL, fg=MUTED,
                                      font=("Segoe UI", 10), wraplength=245,
                                      justify="left", padx=14, pady=15, height=4)
        self.message_label.pack(fill="x", pady=(0, 12))
        self.card(side, "HOW TO PLAY")
        tk.Label(side, text="Connect adjacent letters. Find longer words for bigger scores. Clear burning tiles before they reach the bottom row.",
                 bg=BG, fg=MUTED, wraplength=255, justify="left",
                 font=("Segoe UI", 9)).pack(anchor="w", pady=7)
        self.progress_label = tk.Label(side, text="NEXT LEVEL: 500 PTS",
                                       bg=BG, fg=PURPLE, font=("Segoe UI", 9, "bold"))
        self.progress_label.pack(anchor="w", pady=8)
        self.progress = tk.Canvas(side, height=10, bg=PANEL_2, highlightthickness=0)
        self.progress.pack(fill="x", pady=(0, 10))
        self.progress.create_rectangle(0, 0, 2, 10, fill=GOLD, outline="", tags="bar")

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=24, pady=(0, 13))
        tk.Label(footer, text="ENTER: SUBMIT     BACKSPACE: UNDO     ESC: PAUSE",
                 bg=BG, fg="#697895", font=("Segoe UI", 8, "bold")).pack(side="left")
        tk.Label(footer, text="✦ WORDS ARE YOUR MAGIC ✦",
                 bg=BG, fg="#697895", font=("Segoe UI", 8, "bold")).pack(side="right")

    def card(self, parent, title, color=GOLD):
        tk.Label(parent, text=title, bg=BG, fg=color,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(8, 5))

    def render_all(self):
        self.canvas.delete("all")
        self.tile_items = {}
        # Subtle board frame and inset lines
        self.canvas.create_rectangle(2, 2, BOARD_W-2, BOARD_H-2,
                                     outline="#40516f", width=2)
        for r in range(ROWS):
            for c in range(COLS):
                self.draw_tile(r, c)

    def tile_xy(self, r, c):
        return PAD + c * (TILE + GAP), PAD + r * (TILE + GAP)

    def draw_tile(self, r, c):
        x, y = self.tile_xy(r, c)
        letter = self.grid[r][c]
        selected = (r, c) in self.selected
        burning = (r, c) in self.burning
        base = "#397e9b" if selected else ("#a94343" if burning else TILE_COLORS[(r+c) % 3])
        outline = GOLD if selected else ("#ff9a62" if burning else "#f6c477")
        # Shadow, tile body, top highlight, letter and point value
        shadow = self.canvas.create_rectangle(x+4, y+5, x+TILE+4, y+TILE+5,
                                              fill="#0a1020", outline="")
        rect = self.canvas.create_rectangle(x, y, x+TILE, y+TILE,
                                            fill=base, outline=outline, width=3 if selected or burning else 2)
        self.canvas.create_line(x+7, y+6, x+TILE-7, y+6, fill="#ffe0a3", width=2)
        self.canvas.create_text(x+TILE/2, y+TILE/2-4, text=letter,
                                fill="white", font=("Georgia", 24, "bold"))
        self.canvas.create_text(x+TILE-9, y+TILE-9,
                                text=str(LETTER_POINTS[letter]), fill="#fff0c9",
                                font=("Segoe UI", 8, "bold"))
        if burning:
            self.canvas.create_text(x+TILE/2, y+8, text="✦",
                                    fill="#ffe17b", font=("Segoe UI", 13, "bold"))
            self.canvas.create_rectangle(x-3, y-3, x+TILE+3, y+TILE+3,
                                         outline=RED, width=2)
        if selected:
            self.canvas.create_oval(x+TILE/2-4, y+TILE/2-4,
                                    x+TILE/2+4, y+TILE/2+4,
                                    fill=GOLD, outline="")
        self.tile_items[(r, c)] = (shadow, rect)

    def redraw_positions(self, positions=None):
        if positions is None:
            self.render_all()
            return
        for r, c in positions:
            x, y = self.tile_xy(r, c)
            self.canvas.delete(f"cell_{r}_{c}")
            # Redraw all tiles to keep layering correct.
        self.render_all()

    def on_board_click(self, event):
        if self.paused or self.game_over or self.animating:
            return
        c = (event.x - PAD) // (TILE + GAP)
        r = (event.y - PAD) // (TILE + GAP)
        if not (0 <= r < ROWS and 0 <= c < COLS):
            return
        x, y = self.tile_xy(r, c)
        if event.x > x+TILE or event.y > y+TILE:
            return
        pos = (r, c)
        if self.selected and self.selected[-1] == pos:
            self.undo_selection()
            return
        if pos in self.selected:
            return
        if self.selected and not self.adjacent(self.selected[-1], pos):
            self.set_message("Choose a tile touching the end of your word.", GOLD)
            self.beep()
            return
        self.selected.append(pos)
        self.draw_selection_line()
        self.render_all()
        self.update_word_preview()

    @staticmethod
    def adjacent(a, b):
        return max(abs(a[0]-b[0]), abs(a[1]-b[1])) == 1

    def draw_selection_line(self):
        self.canvas.delete("selection_line")
        if len(self.selected) > 1:
            points = []
            for r, c in self.selected:
                x, y = self.tile_xy(r, c)
                points.extend((x+TILE/2, y+TILE/2))
            self.canvas.create_line(*points, fill=GOLD, width=5,
                                    capstyle="round", joinstyle="round",
                                    smooth=True, tags="selection_line")
            self.canvas.tag_lower("selection_line")

    def current_word(self):
        return "".join(self.grid[r][c] for r, c in self.selected)

    def update_word_preview(self):
        word = self.current_word()
        self.word_label.config(text=word or "—", fg=GOLD if word else CREAM)
        points = sum(LETTER_POINTS[ch] for ch in word)
        self.word_hint.config(text=f"{len(word)} letters  •  {points} base points" if word else "Select neighboring letters")

    def undo_selection(self):
        if self.selected and not self.paused and not self.animating:
            self.selected.pop()
            self.render_all()
            self.draw_selection_line()
            self.update_word_preview()

    def clear_selection(self):
        if self.selected:
            self.selected = []
            self.render_all()
            self.update_word_preview()

    def submit_word(self):
        if self.paused or self.game_over or self.animating:
            return
        word = self.current_word()
        if len(word) < MIN_WORD:
            self.set_message("Your word needs at least three letters. Keep exploring!", GOLD)
            self.beep()
            self.clear_selection()
            return
        if word not in self.dictionary:
            self.combo = 0
            self.update_hud()
            self.set_message(f"“{word}” isn't in the library dictionary. Try another word!", RED)
            self.beep()
            self.clear_selection()
            return

        self.combo += 1
        self.best_combo = max(self.best_combo, self.combo)
        self.words_found += 1
        self.turns += 1
        raw = sum(LETTER_POINTS[ch] for ch in word)
        length_bonus = max(0, len(word)-3) * 12
        combo_bonus = min(self.combo-1, 8) * 5
        gained = (raw + length_bonus + combo_bonus) * self.level
        self.score += gained
        self.last_word = word
        cleared = set(self.selected)
        affected_cols = {c for _, c in cleared}
        self.selected = []
        self.set_message(f"BRILLIANT! {word} earned +{gained} points.", TEAL)
        self.beep(2)
        self.level = self.score // 500 + 1
        self.update_hud()
        self.render_all()
        self.show_score_burst(gained)
        self.animate_clear_and_drop(cleared, affected_cols)
        if self.turns % BURN_EVERY == 0:
            self.ignite_burning()
        self.update_word_preview()

    def animate_clear_and_drop(self, cleared, columns):
        self.animating = True
        # Brief flash on removed tiles before gravity resolves.
        for r, c in cleared:
            x, y = self.tile_xy(r, c)
            self.canvas.create_rectangle(x-2, y-2, x+TILE+2, y+TILE+2,
                                         outline=GOLD, width=4, tags="clear_flash")
        self.root.after(130, lambda: self.resolve_gravity(cleared, columns))

    def resolve_gravity(self, cleared, columns):
        for c in columns:
            survivors = []
            for r in range(ROWS-1, -1, -1):
                if (r, c) in cleared:
                    continue
                survivors.append((self.grid[r][c], (r, c) in self.burning))
            while len(survivors) < ROWS:
                survivors.append((self.random_letter(), False))
            new_burning = set()
            for r in range(ROWS-1, -1, -1):
                letter, is_burning = survivors[ROWS-1-r]
                self.grid[r][c] = letter
                if is_burning:
                    new_burning.add((r, c))
            self.burning = {p for p in self.burning if p[1] != c} | new_burning
        self.render_all()
        self.animating = False
        self.update_hud()

    def ignite_burning(self):
        candidates = [(r, c) for r in range(ROWS-1) for c in range(COLS)
                      if (r, c) not in self.burning]
        if not candidates:
            return
        pos = random.choice(candidates)
        self.burning.add(pos)
        self.render_all()
        self.set_message("A flame has awakened! Clear its column before it reaches the bottom.", RED)
        self.update_hud()

    def tick_burning(self):
        if self.game_over or self.paused or self.screen != "game":
            return
        moved = set()
        for r, c in self.burning:
            if r + 1 >= ROWS:
                self.end_game()
                return
            moved.add((r+1, c))
        self.burning = moved
        self.render_all()
        self.update_hud()
        self.burn_job = self.root.after(max(650, BURN_TICK_MS-(self.level-1)*45), self.tick_burning)

    def schedule_burn(self):
        if self.burn_job:
            self.root.after_cancel(self.burn_job)
        self.burn_job = self.root.after(BURN_TICK_MS, self.tick_burning)

    def schedule_clock(self):
        if self.clock_job:
            self.root.after_cancel(self.clock_job)
        self.clock_job = self.root.after(1000, self.tick_clock)

    def tick_clock(self):
        if self.game_over or self.paused or self.screen != "game":
            return
        self.elapsed += 1
        self.update_hud()
        self.schedule_clock()

    def update_hud(self):
        if not hasattr(self, "hud_labels"):
            return
        self.hud_labels["score"].config(text=f"{self.score:,}")
        self.hud_labels["level"].config(text=str(self.level))
        self.hud_labels["combo"].config(text=f"x{self.combo}")
        self.hud_labels["words"].config(text=str(self.words_found))
        self.hud_labels["time"].config(text=f"{self.elapsed//60}:{self.elapsed%60:02d}")
        self.hud_labels["danger"].config(text=f"{len(self.burning)} 🔥" if self.burning else "SAFE")
        if hasattr(self, "progress"):
            target = self.level * 500
            previous = (self.level-1) * 500
            ratio = max(0, min(1, (self.score-previous)/500))
            width = max(2, int(self.progress.winfo_width()*ratio))
            self.progress.delete("bar")
            self.progress.create_rectangle(0, 0, width, 10, fill=GOLD, outline="", tags="bar")
            self.progress_label.config(text=f"NEXT LEVEL: {target:,} PTS")

    def set_message(self, text, color=MUTED):
        self.message = text
        self.message_color = color
        if hasattr(self, "message_label") and self.message_label.winfo_exists():
            self.message_label.config(text=text, fg=color)

    def show_score_burst(self, points):
        if not self.selected and hasattr(self, "canvas"):
            self.canvas.create_text(BOARD_W/2, 20, text=f"+{points}  ✦",
                                    fill=GOLD, font=("Georgia", 18, "bold"),
                                    tags="score_burst")
            self.root.after(750, lambda: self.canvas.delete("score_burst"))

    def beep(self, count=1):
        if self.sound_on:
            for _ in range(count):
                self.root.bell()

    def toggle_pause(self):
        if self.screen != "game" or self.game_over:
            return
        self.paused = not self.paused
        if self.paused:
            self.stop_timers()
            self.canvas.create_rectangle(0, 0, BOARD_W, BOARD_H,
                                         fill="#080d18", stipple="gray50",
                                         outline="", tags="pause_overlay")
            self.canvas.create_text(BOARD_W/2, BOARD_H/2-12, text="PAUSED",
                                    fill=CREAM, font=("Georgia", 34, "bold"),
                                    tags="pause_overlay")
            self.canvas.create_text(BOARD_W/2, BOARD_H/2+30,
                                    text="Press ESC or click RESUME",
                                    fill=GOLD, font=("Segoe UI", 12, "bold"),
                                    tags="pause_overlay")
            self.pause_button = self.make_button(self.root, "▶  RESUME", self.toggle_pause, TEAL, 14)
            self.pause_button.place(relx=.5, rely=.94, anchor="center")
        else:
            self.canvas.delete("pause_overlay")
            if hasattr(self, "pause_button"):
                self.pause_button.destroy()
            self.schedule_clock()
            self.schedule_burn()

    def stop_timers(self):
        for name in ("clock_job", "burn_job"):
            job = getattr(self, name, None)
            if job:
                try:
                    self.root.after_cancel(job)
                except tk.TclError:
                    pass
                setattr(self, name, None)

    def end_game(self):
        self.game_over = True
        self.stop_timers()
        self.canvas.create_rectangle(0, 0, BOARD_W, BOARD_H,
                                     fill="#080d18", stipple="gray50",
                                     outline="", tags="gameover")
        self.canvas.create_text(BOARD_W/2, BOARD_H/2-48, text="THE FLAMES WON",
                                fill=RED, font=("Georgia", 29, "bold"), tags="gameover")
        self.canvas.create_text(BOARD_W/2, BOARD_H/2+2,
                                text=f"FINAL SCORE  {self.score:,}",
                                fill=GOLD, font=("Segoe UI", 18, "bold"), tags="gameover")
        self.canvas.create_text(BOARD_W/2, BOARD_H/2+40,
                                text=f"Level {self.level}   •   {self.words_found} words   •   Best combo x{self.best_combo}",
                                fill=CREAM, font=("Segoe UI", 11), tags="gameover")
        self.set_message("The flames reached the bottom. Your next run can beat this score!", RED)
        self.make_button(self.root, "↻  PLAY AGAIN", self.start_game, TEAL, 18).place(relx=.5, rely=.94, anchor="center")
        self.beep(3)

    def confirm_menu(self):
        if messagebox.askyesno("Return to menu", "Leave this game and return to the main menu?"):
            self.show_menu()

    def toggle_sound(self):
        self.sound_on = not self.sound_on

    def animate_atmosphere(self):
        # Soft drifting sparkles in the unused background margins.
        if self.screen in ("menu", "instructions"):
            if random.random() < .55:
                x = random.randint(10, max(20, self.root.winfo_width()-10))
                y = random.randint(10, max(20, self.root.winfo_height()-10))
                dot = tk.Label(self.root, text="✦", bg=BG, fg=random.choice([GOLD, TEAL, PURPLE]),
                               font=("Segoe UI", random.randint(7, 12)))
                dot.place(x=x, y=y)
                self.root.after(900, dot.destroy)
        self.particle_job = self.root.after(450, self.animate_atmosphere)

    def close_game(self):
        self.stop_timers()
        if self.particle_job:
            try:
                self.root.after_cancel(self.particle_job)
            except tk.TclError:
                pass
        self.root.destroy()



# ---------------------------------------------------------------------------
# WORM ARENA: optional word-powered combat mode
# ---------------------------------------------------------------------------

class WormArena:
    """A small Tkinter pixel-art battle mode that reuses the game's dictionary."""

    ENEMIES = [
        ("MOSS SLIME", "#67c96b", 42),
        ("EMBER IMP", "#ff7048", 50),
        ("SHADOW BAT", "#8b78d6", 46),
        ("MUSHROOM BEAST", "#df647d", 58),
    ]

    def __init__(self, game):
        self.game = game
        self.window = tk.Toplevel(game.root)
        self.window.title("Bookworm: Worm Arena")
        self.window.geometry("940x690")
        self.window.minsize(820, 620)
        self.window.configure(bg=BG)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.player_hp = 100
        self.level = 1
        self.wins = 0
        self.combo = 0
        self.enemy_hp = 0
        self.enemy_max_hp = 0
        self.enemy_name = ""
        self.enemy_color = "#67c96b"
        self.enemy_turn = 0
        self.busy = False
        self.closed = False

        top = tk.Frame(self.window, bg=BG)
        top.pack(fill="x", padx=18, pady=(14, 8))
        tk.Label(top, text="WORM ARENA", bg=BG, fg=GOLD,
                 font=("Georgia", 25, "bold")).pack(side="left")
        self.level_label = tk.Label(top, text="LEVEL 1", bg=BG, fg=TEAL,
                                    font=("Segoe UI", 12, "bold"))
        self.level_label.pack(side="right")

        self.canvas = tk.Canvas(self.window, width=900, height=420,
                                bg="#111a2b", highlightthickness=0)
        self.canvas.pack(padx=18, pady=8, fill="both", expand=True)

        status = tk.Frame(self.window, bg=PANEL, padx=14, pady=12)
        status.pack(fill="x", padx=18, pady=8)
        self.player_label = tk.Label(status, text="", bg=PANEL, fg=TEAL,
                                     font=("Segoe UI", 10, "bold"))
        self.player_label.pack(anchor="w")
        self.enemy_label = tk.Label(status, text="", bg=PANEL, fg=RED,
                                    font=("Segoe UI", 10, "bold"))
        self.enemy_label.pack(anchor="w", pady=(4, 0))
        self.message = tk.Label(status, text="Type a word to cast an attack!",
                                bg=PANEL, fg=CREAM, font=("Segoe UI", 10))
        self.message.pack(anchor="w", pady=(7, 0))

        controls = tk.Frame(self.window, bg=BG)
        controls.pack(fill="x", padx=18, pady=(4, 14))
        self.word_entry = tk.Entry(controls, font=("Consolas", 17, "bold"),
                                   bg="#263653", fg=CREAM, insertbackground=CREAM,
                                   relief="flat", justify="center")
        self.word_entry.pack(side="left", fill="x", expand=True, ipady=9)
        self.word_entry.bind("<Return>", lambda event: self.attack())
        self.attack_button = tk.Button(
            controls, text="CAST WORD  [ENTER]", command=self.attack,
            bg=TEAL, fg=BG, activebackground=GOLD, relief="flat",
            font=("Segoe UI", 10, "bold"), padx=18, pady=12, cursor="hand2")
        self.attack_button.pack(side="left", padx=(9, 0))
        tk.Button(controls, text="BACK TO GAME", command=self.close,
                  bg="#34425c", fg=CREAM, relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=12, pady=12).pack(side="left", padx=(8, 0))

        self.spawn_enemy()
        self.word_entry.focus_set()

    def draw_pixel(self, x, y, color, scale=8):
        self.canvas.create_rectangle(x, y, x + scale, y + scale,
                                     fill=color, outline=color)

    def draw_worm(self, x, y, hurt=False):
        # Chunky segmented worm hero, with a distinct face and tiny feet.
        shades = ["#42d6b5", "#31b99f", "#279b89", "#217c78"]
        for i in range(5):
            px = x - i * 24
            py = y + (4 if i % 2 else 0)
            self.canvas.create_rectangle(px, py, px + 23, py + 21,
                                         fill=shades[i % len(shades)],
                                         outline="#102b36", width=2)
            self.canvas.create_rectangle(px + 4, py + 17, px + 9, py + 25,
                                         fill="#163d46", outline="")
            self.canvas.create_rectangle(px + 15, py + 17, px + 20, py + 25,
                                         fill="#163d46", outline="")
        face = "#ffb3a7" if hurt else "#eafff5"
        self.canvas.create_rectangle(x + 11, y + 5, x + 16, y + 10,
                                     fill=face, outline="")
        self.canvas.create_rectangle(x + 20, y + 5, x + 25, y + 10,
                                     fill=face, outline="")
        self.canvas.create_rectangle(x + 17, y + 14, x + 24, y + 17,
                                     fill="#123a3b", outline="")

    def draw_enemy(self, x, y):
        c = self.enemy_color
        self.canvas.create_rectangle(x, y + 18, x + 100, y + 88,
                                     fill=c, outline="#080d18", width=3)
        self.canvas.create_rectangle(x + 12, y + 2, x + 88, y + 35,
                                     fill=c, outline="#080d18", width=3)
        self.canvas.create_rectangle(x + 19, y + 28, x + 32, y + 43,
                                     fill="#fff4d6", outline="")
        self.canvas.create_rectangle(x + 67, y + 28, x + 80, y + 43,
                                     fill="#fff4d6", outline="")
        self.canvas.create_rectangle(x + 24, y + 32, x + 29, y + 42,
                                     fill="#101525", outline="")
        self.canvas.create_rectangle(x + 72, y + 32, x + 77, y + 42,
                                     fill="#101525", outline="")
        self.canvas.create_rectangle(x + 39, y + 61, x + 62, y + 69,
                                     fill="#401f35", outline="")
        self.canvas.create_rectangle(x + 15, y + 83, x + 34, y + 99,
                                     fill="#27304a", outline="")
        self.canvas.create_rectangle(x + 67, y + 83, x + 86, y + 99,
                                     fill="#27304a", outline="")

    def draw_scene(self, effect=None):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 900, 420, fill="#111a2b", outline="")
        # Distant library silhouettes and floor tiles.
        for i in range(8):
            bx = i * 120 + 10
            self.canvas.create_rectangle(bx, 95, bx + 72, 230,
                                         fill="#1a2942", outline="#263a58", width=2)
            for j in range(3):
                self.canvas.create_rectangle(bx + 8, 112 + j * 34,
                                             bx + 64, 137 + j * 34,
                                             fill="#263653", outline="")
        self.canvas.create_rectangle(0, 300, 900, 420, fill="#202c3e", outline="")
        for i in range(0, 900, 60):
            self.canvas.create_line(i, 300, i - 25, 420, fill="#2b3b50")
        self.draw_worm(245, 250, hurt=(effect == "hurt"))
        self.draw_enemy(635, 198)
        if effect == "attack":
            for i in range(5):
                self.canvas.create_rectangle(365 + i * 32, 240 - (i % 2) * 20,
                                             380 + i * 32, 255 - (i % 2) * 20,
                                             fill=GOLD, outline="")
            self.canvas.create_text(475, 190, text="WORD BLAST!",
                                    fill=GOLD, font=("Consolas", 18, "bold"))
        elif effect == "hurt":
            self.canvas.create_text(440, 180, text="OUCH!",
                                    fill=RED, font=("Consolas", 20, "bold"))
        self.canvas.create_text(450, 28, text="THE ENCHANTED LIBRARY • BATTLE FLOOR",
                                fill="#7184a5", font=("Segoe UI", 10, "bold"))

    def update_status(self):
        self.level_label.config(text=f"LEVEL {self.level}  •  WINS {self.wins}")
        self.player_label.config(
            text=f"WORM HP  {self.player_hp}/100  " + "█" * (self.player_hp // 10)
        )
        self.enemy_label.config(
            text=f"{self.enemy_name}  HP  {self.enemy_hp}/{self.enemy_max_hp}  " +
                 "█" * max(0, self.enemy_hp // 5)
        )

    def spawn_enemy(self):
        self.busy = False
        self.enemy_name, self.enemy_color, base_hp = random.choice(self.ENEMIES)
        self.enemy_max_hp = base_hp + (self.level - 1) * 9
        self.enemy_hp = self.enemy_max_hp
        self.enemy_turn = 0
        self.draw_scene()
        self.update_status()
        self.message.config(text=f"A {self.enemy_name} appears! Spell a valid word (3+ letters).",
                            fg=CREAM)
        self.attack_button.config(state="normal")
        self.word_entry.config(state="normal")
        self.word_entry.delete(0, "end")
        self.word_entry.focus_set()

    def attack(self):
        if self.busy or self.player_hp <= 0:
            return
        word = self.word_entry.get().strip().upper()
        if len(word) < 3 or not word.isalpha() or word not in self.game.dictionary:
            self.combo = 0
            self.message.config(text="That word isn't in the spellbook. Try a valid 3+ letter word.",
                                fg=RED)
            self.word_entry.selection_range(0, "end")
            return

        self.combo += 1
        base = len(word) * 4
        bonus = max(0, len(word) - 5) * 3
        critical = random.random() < min(.35, .08 + len(word) * .025)
        damage = base + bonus + (12 if critical else 0) + min(12, self.combo * 2)
        self.enemy_hp = max(0, self.enemy_hp - damage)
        self.busy = True
        self.draw_scene("attack")
        self.update_status()
        tag = " CRITICAL!" if critical else ""
        self.message.config(text=f"{word}: {damage} damage! Combo x{self.combo}.{tag}",
                            fg=GOLD if critical else TEAL)
        self.word_entry.delete(0, "end")
        self.attack_button.config(state="disabled")
        self.word_entry.config(state="disabled")
        self.window.after(650, self.after_player_attack)

    def after_player_attack(self):
        if self.closed:
            return
        if self.enemy_hp <= 0:
            self.wins += 1
            self.level += 1
            self.player_hp = min(100, self.player_hp + 12)
            self.update_status()
            self.message.config(text="Enemy defeated! +12 HP. A stronger foe approaches...",
                                fg=GOLD)
            self.draw_scene()
            self.window.after(1000, self.spawn_enemy)
        else:
            self.enemy_attack()

    def enemy_attack(self):
        if self.closed:
            return
        self.enemy_turn += 1
        damage = random.randint(5, 9) + self.level // 2
        self.player_hp = max(0, self.player_hp - damage)
        self.combo = 0
        self.draw_scene("hurt")
        self.update_status()
        self.message.config(text=f"{self.enemy_name} strikes back for {damage} damage!",
                            fg=RED)
        if self.player_hp <= 0:
            self.message.config(text=f"Your worm needs a rest. You defeated {self.wins} enemies.",
                                fg=RED)
            self.attack_button.config(state="disabled")
            self.word_entry.config(state="disabled")
            self.window.after(900, self.show_game_over)
        else:
            self.window.after(500, self.enable_input)

    def enable_input(self):
        if self.closed:
            return
        self.busy = False
        self.attack_button.config(state="normal")
        self.word_entry.config(state="normal")
        self.word_entry.focus_set()

    def show_game_over(self):
        if self.closed:
            return
        self.canvas.create_rectangle(170, 120, 730, 310, fill="#080d18",
                                     outline=RED, width=3)
        self.canvas.create_text(450, 170, text="BATTLE OVER", fill=RED,
                                font=("Georgia", 28, "bold"))
        self.canvas.create_text(450, 225, text=f"Enemies defeated: {self.wins}",
                                fill=CREAM, font=("Segoe UI", 15, "bold"))
        self.canvas.create_text(450, 260, text="Close this window to return to Bookworm.",
                                fill=MUTED, font=("Segoe UI", 10))

    def close(self):
        if self.closed:
            return
        self.closed = True
        try:
            self.window.destroy()
        except tk.TclError:
            pass


def main():
    root = tk.Tk()
    BookwormGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
