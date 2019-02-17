import os

_LAUNCHDIR = os.path.abspath(os.path.dirname(__file__))

SAVED_IMAGES_DIR = os.path.join(_LAUNCHDIR, 'saved_wisdom_images')
if not os.path.isdir(SAVED_IMAGES_DIR):
    os.makedirs(SAVED_IMAGES_DIR)

PREFS_FILE_NAME = "wisdom_prefs.json"
PREFS_FILE_PATH = os.path.join(_LAUNCHDIR, PREFS_FILE_NAME)
DEFAULT_PREFS = {
    "geo": [50, 70, 1600, 980],
    "font": {
        "family": "Stay Wildy Personal Use Only",
        "size": 84
    }
}

FONT_SIZES = [36, 42, 48, 60, 72, 84, 100, 120]

PHRASES = [
    "A {0} in the hand is worth two in the {1}",
    "Your future is created by what you do {0}",
    "The secret to {0} is to acknowledge the world is {1}",
    "A person with no imagination has no {1}",
    "Find the courage to let go of what you can't {1}",
    "I'm gonna make the rest of my {0} the best of my {0}",
    "It's the {0}'s that will {1} you",
    "Fall in love with someone who doesn't make you think love is {0}",
    "Anything that costs you your {0} is too expensive",
    "You are the everlasting {0} in the realm of {1}",
    "Don't worry about {0}, worry about the chances you miss when you don't even {1}",
    "When it rains look for {0}, when it's dark look for {1}",
    "Life is not about waiting for the {0} to pass but learning to {1} in the rain",
    "Let your {0} change the world but don't let the world change your {0}",
    "You never realise how {0} you are until being {0} is the only choice you have",
    "You can never cross the {0} unless you have the courage to lose sight of the {1}",
    "It always seems {0} until it's {1}"
]

SUB_0 = [
    "bird",
    "rock",
    "faith",
    "rabbit",
    "fork",
    "life",
    "hard",
    "peace",
    "sun",
    "balls",
    "time",
    "coffee",
    "storm",
    "failure",
    "rainbows",
    "smile",
    "impossible",
    "old",
    "ocean",
    "road",
    "pasta sauce",
    "hovercraft"
]

SUB_1 = [
    "bush",
    "today",
    "face",
    "shit",
    "best",
    "kill",
    "shadows",
    "uranus",
    "ear",
    "bahamas",
    "eye",
    "shore",
    "stars",
    "chicken",
    "eels",
    "pudding"
]

SUB_VFX = [
    "render",
    "pixel aspect",
    "vertex",
    "samples",
    "boolean",
    "scatter",
    "occlusion",
    "bake",
    "wedge",
    "dailies",
    "voronoi",
    "flop",
    "gamma",
    "matte",
    "ghosting",
    "lanczos",
    "parallax",
    "pipeline",
    "farm",
    "seed",
    "deep",
    "skinning",
    "final",
]
