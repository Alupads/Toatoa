# story.py

def get_story_node(node_id):
    story_data = {
        "intro": {
            "text": "You are a passenger on a long-haul flight.\nThe cabin is calm... too calm.\n\n*BEEP* *BEEP* SYSTEM FAILURE!\nMetal screams. The plane shakes violently. Everything goes silent.\n\nYou wake up in burning wreckage. You are the only survivor.\nIn the distance, an ancient temple rises above the forest.",
            "choices": [
                {"text": "Search wreckage", "next": "search_wreckage"},
                {"text": "Walk to temple", "next": "level_1"}
            ]
        },
        "search_wreckage": {
            "text": "You dig through the burning debris.\nYou find a Flare! This might save your life.\n\nThe forest looks dark and uninviting.",
            "give_item": "Flare",
            "choices": [
                {"text": "Head into the forest", "next": "level_1"}
            ]
        },
        "level_1": {
            "text": "LEVEL 1 - THE WATCHING FOREST\n\nThe forest is not silent. It is listening to your breathing. It is learning your rhythm.\nSomewhere behind you... the wreckage still burns.",
            "choices": [
                {"text": "Enter the temple", "next": "level_2"},
                {"text": "Hesitate in the forest", "next": "hesitate_forest"}
            ]
        },
        "hesitate_forest": {
            "text": "The forest bends toward you... like it heard you hesitate.\nShadows whip across your legs, draining your energy.",
            "damage": 30,
            "sanity_loss": 20,
            "choices": [
                {"text": "Run to the temple!", "next": "level_2"}
            ]
        },
        "level_2": {
            "text": "LEVEL 2 - TEMPLE ENTRANCE\n\nThe air changes the moment you step inside. It feels heavier.\nSuddenly, a massive shape moves in the darkness blocking your path!",
            "choices": [
                {"text": "Use Flare", "next": "use_flare", "requires": "Flare"},
                {"text": "Run blindly", "next": "run_blindly"}
            ]
        },
        "use_flare": {
            "text": "You ignite the flare. Light explodes into the shadows!\nThe creature retreats, shrieking in fear.\n\nTwo paths reveal themselves.",
            "remove_item": "Flare",
            "choices": [
                {"text": "Fire path (burning heat)", "next": "fire_path"},
                {"text": "Water path (cold silence)", "next": "water_path"}
            ]
        },
        "run_blindly": {
            "text": "You run blindly in the dark. The shape slashes at you before you escape into a nearby corridor!",
            "damage": 50,
            "sanity_loss": 40,
            "choices": [
                {"text": "Fire path (burning heat)", "next": "fire_path"},
                {"text": "Water path (cold silence)", "next": "water_path"}
            ]
        },
        "fire_path": {
            "text": "The heat consumes your strength. The temple rejects you.\nYou collapse into the ashes...",
            "damage": 100,
            "choices": []
        },
        "water_path": {
            "text": "You follow the cold path. The silence feels wrong, but you survive.\nYou enter the final chamber.",
            "choices": [
                {"text": "Enter the core", "next": "boss_room"}
            ]
        },
        "boss_room": {
            "text": "LEVEL 5 - FINAL CHAMBER\n\nAt the center, an artifact pulses like a heartbeat. A survivor stands before it in a trance.\n'I didn't just survive the crash...' they whisper. 'I caused it.'\n\nThe artifact controls them now.",
            "choices": [
                {"text": "Talk to them", "next": "boss_talk"},
                {"text": "Destroy Artifact", "next": "boss_destroy"}
            ]
        },
        "boss_talk": {
            "text": "You try to reason with them, but the artifact speaks louder.\nIt invades your mind, shattering your sanity.",
            "sanity_loss": 100,
            "choices": []
        },
        "boss_destroy": {
            "text": "You strike the artifact with everything you have!\nThe temple screams. The trance is broken.\nYou drag the survivor out as the temple collapses around you.",
            "flag_saved": True,
            "choices": [
                {"text": "See Ending", "next": "victory"}
            ]
        },
        "victory": {
            "text": "HERO ENDING\n\nYou escaped the temple and saved a soul from the silence.\nThe rescue choppers found you the next morning.",
            "choices": []
        }
    }
    return story_data.get(node_id, None)