import time, random

def slow(text):
    for c in text:
        print(c, end='')
        time.sleep(0.02)
    print()

def choose(prompt):
    return input(prompt)

class Player:
    def __init__(self):
        self._lives = 3
        self._flare = True
        self._saved_survivor = False
        self._ran_from_truth = False

    def lose_life(self, msg):
        slow(msg)
        self._lives -= 1
        print("Lives left:", self._lives, "\n")
        return self._lives > 0

    def reset(self):
        self._lives = 3
        self._flare = True
        self._saved_survivor = False
        self._ran_from_truth = False

    def has_flare(self):
        return self._flare

    def use_flare(self):
        self._flare = False

    def save_survivor(self):
        self._saved_survivor = True

    def run_from_truth(self):
        self._ran_from_truth = True

    def get_status(self):
        return self._saved_survivor, self._ran_from_truth, self._flare

class Level:
    def enter(self, player):
        pass

class Level1(Level):
    def enter(self, player):
        slow("\nLEVEL 1 - THE WATCHING FOREST\n")
        slow("The forest is not silent.")
        slow("It is listening to your breathing.")
        slow("And it is learning your rhythm.\n")

        slow("Somewhere behind you… the wreckage still burns.")
        slow("But nothing in this forest is warmer than the way it looks at you.\n")

        while True:
            c = choose("1 Enter the temple\n2 Stay in the forest\nChoose: ")

            if c == "1":
                slow("You step forward.")
                slow("The trees do not move… but something between them does.\n")
                return True

            elif c == "2":
                if not player.lose_life("The forest bends toward you… like it heard you hesitate."):
                    return False

class Level2(Level):
    def enter(self, player):
        slow("\nLEVEL 2 - TEMPLE ENTRANCE\n")
        slow("The air changes the moment you step inside.")
        slow("It feels... heavier.")
        slow("Like the temple remembers something about you.\n")

        if random.choice([True, False]):
            slow("A shape moves in the darkness...\n")

            c = choose(
                "1 Run\n"
                "2 Use flare\n"
                "Choose: "
            )

            if c == "2":
                if player.has_flare():
                    slow("You ignite the flare.")
                    slow("Light explodes into the shadows.")
                    slow("Something retreats... afraid.\n")
                    player.use_flare()
                else:
                    if not player.lose_life("You reach for the flare... but it's gone."):
                        return False
            elif c == "1":
                if not player.lose_life("You run blindly... but it is faster than you."):
                    return False

        slow("Two paths reveal themselves.\n")

        while True:
            c = choose(
                "1 Fire path (burning heat)\n"
                "2 Water path (cold silence)\n"
                "Choose: "
            )

            if c == "2":
                slow("You follow the cold path. The silence feels wrong.\n")
                return True
            elif c == "1":
                if not player.lose_life("The heat consumes your strength. The temple rejects you."):
                    return False


class Level3(Level):
    def enter(self, player):
        slow("\nLEVEL 3 - LIVING WALLS\n")
        slow("The walls pulse slightly...")
        slow("Not like stone. Like flesh.\n")

        slow("A voice whispers without sound:")
        slow("'You are being measured.'\n")

        while True:
            s1 = input("Left switch (yes/no): ").lower()
            s2 = input("Right switch (yes/no): ").lower()

            if s1 == "yes" and s2 == "yes":
                slow("A deep rumble echoes beneath you.")
                slow("The temple... allows you forward.\n")
                return True
            else:
                if not player.lose_life("The walls contract suddenly. You chose wrong."):
                    return False


class Level4(Level):
    def enter(self, player):
        slow("\nLEVEL 4 - SHIFTING CHAMBER\n")
        slow("The structure is unstable.")
        slow("Paths change when you are not looking.\n")

        slow("Symbols glow faintly on the walls.")
        slow("They feel like instructions... or warnings.\n")

        while True:
            c = choose(
                "1 Study symbols\n"
                "2 Rush forward\n"
                "Choose: "
            )

            if c == "1":
                slow("You take time to understand.")
                slow("The temple's logic reveals itself...\n")
                return True
            elif c == "2":
                if not player.lose_life("You rush forward. The floor disappears beneath you."):
                    return False


class Level5(Level):
    def enter(self, player):
        slow("\nLEVEL 5 - FINAL CHAMBER\n")

        slow("The temple no longer feels like a place.")
        slow("It feels like a living mind.\n")

        slow("At the center... an artifact pulses.")
        slow("Like a heartbeat.\n")

        slow("A survivor stands before it.\n")

        slow("At first, relief.")
        slow("Then fear.\n")

        slow("Their voice trembles:")
        slow("'I didn't just survive the crash...'\n")
        slow("'I caused it.'\n")

        slow("They continue:")
        slow("'I was desperate... I needed a miracle.'")
        slow("'The artifact answered... but not how I expected.'\n")

        slow("FLASHBACK:")
        slow("The plane... shaking.")
        slow("Not failure.")
        slow("Interference.\n")

        slow("The artifact pulled the plane down.\n")

        slow("Now it controls them.\n")

        slow("*BOSS: THE TRANCE SURVIVOR*\n")

        while True:
            c = choose(
                "1 Talk\n"
                "2 Use flare\n"
                "3 Run\n"
                "4 Destroy artifact\n"
                "Choose: "
            )

            if c == "1":
                if not player.lose_life("You try to reach them... but the artifact speaks louder."):
                    return False

            elif c == "2":
                if player.has_flare():
                    slow("You ignite the flare one last time.")
                    slow("Light clashes with the artifact.\n")
                    slow("The control shatters.\n")
                    slow("The survivor collapses... free.\n")
                    player.use_flare()
                    player.save_survivor()
                    return True
                else:
                    if not player.lose_life("You have no flare left."):
                        return False

            elif c == "3":
                slow("You turn away from the truth.")
                slow("Some things are easier left unknown.\n")
                player.run_from_truth()
                return True

            elif c == "4":
                slow("You strike the artifact.")
                slow("The temple screams.\n")
                slow("Everything begins to collapse.\n")
                slow("You don't know if you'll survive...\n")
                player.save_survivor()
                return True

class Game:
    def __init__(self):
        self.player = Player()
        self.levels = [Level1(), Level2(), Level3(), Level4(), Level5()]

    def tutorial(self):
        print("\n==== TUTORIAL ====\n")
        slow("This is a choice-based survival game.")
        slow("You will be given options during gameplay.")
        slow("Type the number of your chosen action.\n")

        slow("You start with 3 lives.")
        slow("Wrong decisions reduce your lives.")
        slow("When lives reach zero, the game ends.\n")

        slow("Some choices may require special items.")
        slow("You may receive or lose them depending on your decisions.\n")

        slow("There is no undo button.")
        slow("Once you choose, the outcome is final.\n")

        slow("Pay attention. Some choices are not what they seem.\n")

        while input("Type 'start' to begin: ").lower() != "start":
            print("Waiting...\n")

    def intro(self):

        slow("You are a passenger on a long-haul flight.")
        slow("The cabin is calm... too calm.\n")

        slow("*BEEP* *BEEP* *BEEP*")
        slow("SYSTEM FAILURE!\n")

        slow("Metal screams above you.")
        slow("The plane begins to shake violently.\n")

        slow("*BOOM*\n")

        slow("Everything goes silent.\n")

        slow("You wake up in burning wreckage.")
        slow("No voices respond.\n")
        slow("You are the only sole survivor... or so you thought.\n")

        slow("You search through the wreckage...\n")
        slow("A flare.\n")
        slow("You take it.\n")

        slow("In the distance, a massive ancient temple rises above the forest.")

        slow("It is the highest point you can see.\n")

        slow("Your thoughts become clear:\n")
        slow("'If I reach the top of that temple, I can signal for rescue.'\n")
    def ending(self):
        slow("\nFINAL OUTCOME\n")
        saved, ran, flare = self.player.get_status()

        if saved and flare:
            slow("HERO ENDING — Something was saved from the silence.")
        elif saved:
            slow("SACRIFICE ENDING — You saved a soul, but not yourself.")
        elif ran and flare:
            slow("ESCAPE ENDING — You survived, but the truth followed you.")
        elif not flare:
            slow("LOST ENDING — The temple finished what it started.")
        else:
            slow("NEUTRAL ENDING — You are still inside… somewhere.")

    def play(self):
        self.player.reset()
        self.tutorial()
        self.intro()

        for level in self.levels:
            if not level.enter(self.player):
                print("Game Over\n")
                return

        self.ending()

def start():
    game = Game()
    while True:
        print("\n==== TEMPLE ESCAPE ====\n")
        print("1 New Game")
        print("2 Quit")
        c = choose("Choose: ")
        if c == "1":
            game.play()
        else:
            break

start()