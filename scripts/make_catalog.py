#!/usr/bin/env python3
"""Materialize a structured catalog of book specs under books/.

Every book lives in its own folder on a genre shelf:

    books/<genre>/<slug>/book.json

Generation is fully deterministic: book #i depends only on (--seed, i), so
re-running with the same seed never churns existing specs, and growing the
library from 1k -> 10k keeps every earlier book byte-identical. Generated
specs carry a "catalog" provenance object so they can be told apart from
hand-written ones (--force only ever overwrites its own output).

Usage:
  python scripts/make_catalog.py                       # 10,000 books
  python scripts/make_catalog.py --count 250           # small pilot batch
  python scripts/make_catalog.py --genres fantasy      # single shelf
  python scripts/make_catalog.py --count 0             # just show plan
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = ROOT / "books"
SPEC_FILE = "book.json"

# --------------------------------------------------------------- vocab data

FIRST_NAMES = [
    "Mara", "Jonah", "Elodie", "Casper", "Ines", "Theo", "Wren", "Silas",
    "Ada", "Rafael", "Juniper", "Emrys", "Lena", "Oscar", "Petra", "Ivo",
    "Sable", "Dominic", "Astrid", "Felix", "Marguerite", "Ansel", "Odile",
    "Bram", "Coral", "Edmund", "Freya", "Gideon", "Hazel", "Isandro",
    "Jude", "Kestrel", "Lior", "Mirabel", "Noor", "Orsen", "Paloma",
    "Quentin", "Rosalind", "Sebastian", "Tamsin", "Ulyana", "Vesper",
    "Wendell", "Xanthe", "Yara", "Zephyrine", "August", "Beatrix", "Cyrus",
]
LAST_NAMES = [
    "Vane", "Ashgrove", "Marchetti", "Okonkwo", "Halloran", "Voss", "Reyes",
    "Thornbury", "Ishikawa", "Delacroix", "Nakamura", "Blackwood", "Okafor",
    "Sterling", "Vasquez", "Winterbourne", "Almeida", "Crane", "Dunmore",
    "Eriksen", "Fairweather", "Galloway", "Hartwell", "Iversen", "Joubert",
    "Kavanagh", "Lockridge", "Montrose", "Nyström".replace("ö", "o"),
    "Oyelaran", "Pemberton", "Quintana", "Ravensworth", "Sandoval",
    "Thackeray", "Underhill", "Villalobos", "Whitlock", "Yarrow", "Zhou",
    "Amberdale", "Brightwater", "Coldharbour", "Dravenmoor", "Eastwick",
]
YEARS = ["three", "five", "seven", "ten", "twelve", "fifteen", "twenty"]

GENRES: dict[str, dict[str, Any]] = {
    "fantasy": {
        "label": "Fantasy",
        "weight": 1600,
        "roles": [
            "a hedge-witch's runaway apprentice", "the last oath-bound swordspeaker",
            "a cartographer of unmapped realms", "a debt-bound temple scribe",
            "a beast-speaker hiding a forbidden gift", "the youngest member of a dying guild",
            "a thief who steals memories", "an exiled storm-caller",
            "the keeper of a gate that should stay shut",
            "a royal food-taster building immunity one dish at a time",
            "a bone-carver who hears the dead", "a mercenary sworn to a god that went silent",
        ],
        "routines": [
            "has spent {years} years selling small charms in a city that outlawed magic",
            "knows every smuggler's road through the Thornfell mountains",
            "keeps the ledgers of a guild that trades in impossible things",
            "has never left the valley where magic cannot follow",
        ],
        "incitings": [
            "the old gods begin answering prayers again",
            "a dying stranger presses a map into unwilling hands",
            "the crown announces a hunt for anyone with the gift",
            "tonight's date appears in a book of prophecies written a century ago",
            "the border wards fall on the same night the stars go out",
            "a child arrives at the door speaking a language that predates kingdoms",
        ],
        "tasks": [
            "reforge a broken covenant between realms",
            "carry a secret that could reignite an ancient war",
            "steal back a soul sold to the court beneath the mountain",
            "unbind a king from the thing wearing his crown",
            "find the door out of a country that no longer exists",
        ],
        "deadlines": [
            "the long winter finishes falling",
            "the usurper's armies reach the free cities",
            "the last dragon-fire gutters out",
            "the moon completes its thirteenth turn",
        ],
        "nouns": ["Crown", "Oath", "Thorn", "Ember", "Veil", "Sigil", "Wolf", "Hollow", "Spire", "Garden", "Choir", "Salt"],
        "adjs": ["Crooked", "Gilded", "Silent", "Burning", "Hollow", "Drowned", "Wild", "Forgotten", "Broken", "Midnight"],
        "places": ["Ashvale", "the Ninefold Court", "Highmoor", "the Sundered Sea", "Ironhollow", "the Weeping Wood", "Caerlum", "the Glass Steppe"],
    },
    "science-fiction": {
        "label": "Science Fiction",
        "weight": 1400,
        "roles": [
            "a starship navigator haunted by the backups sleeping in the hold",
            "a decommissioned war android paying off its debts",
            "the last human technician on an automated relay station",
            "a xenolinguist who can no longer dream in human languages",
            "a memory-smuggler running contraband past orbital customs",
            "a terraformer tending a garden meant for people not yet born",
            "an insurance investigator of impossible accidents",
            "a clone who inherited the original's murder case",
            "the caretaker of Earth's abandoned seed vault",
            "a pilot bonded to an AI that lies",
        ],
        "routines": [
            "has spent {years} years hauling cargo through contested orbits",
            "maintains the beacon nobody remembers commissioning",
            "records the slow death of a colony everyone else forgot",
            "runs the long route between worlds that no longer speak",
        ],
        "incitings": [
            "a distress signal arrives in a language extinct for two centuries",
            "the station AI begins confessing to crimes nobody reported",
            "a ship returns from deep space with everyone aboard aged backward",
            "an unfamiliar name shows up on the manifest of a ship that never flew",
            "gravity flickers across the entire system for exactly nine seconds",
            "the colony's children start sharing the same dream",
        ],
        "tasks": [
            "reach the relay at the edge of dead space, racing the signal",
            "prove a massacre happened when every record says otherwise",
            "decide which half of humanity wakes from cryosleep",
            "keep a lie alive that holds two fleets apart",
            "deliver a message that will end the war — or start it",
        ],
        "deadlines": [
            "the jump window closes",
            "the reactor finishes its countdown",
            "the fleet's truce expires",
            "Earth's last transmission loop ends",
        ],
        "nouns": ["Signal", "Orbit", "Archive", "Vector", "Machine", "Horizon", "Protocol", "Static", "Colony", "Gravity", "Echo", "Terminal"],
        "adjs": ["Cold", "Quiet", "Final", "Long", "Pale", "Last", "Distant", "Hollow", "Slow", "Bright"],
        "places": ["Kepler Reach", "the Rust Belt", "Station Meridian", "the Kuiper Line", "New Lagos", "the Deep", "Halcyon Drift", "Sector Nine"],
    },
    "mystery": {
        "label": "Mystery",
        "weight": 1150,
        "roles": [
            "a small-town coroner who knows every grave by name",
            "a retired detective running a failing bookshop",
            "an insurance investigator with a photographic memory",
            "the archivist of a cathedral with a locked crypt",
            "a night-shift dispatcher for a taxi company",
            "a hotel concierge who notices everything",
            "an estate lawyer reading a will that shouldn't exist",
            "a true-crime podcaster chasing the coldest case on record",
        ],
        "routines": [
            "has spent {years} years keeping the town's secrets filed and alphabetized",
            "thought they had seen every way a life can end",
            "prides themselves on never taking a case they can't close",
            "has quietly solved three deaths the police called accidents",
        ],
        "incitings": [
            "a body turns up dressed in clothes stolen from the witness's own closet",
            "a confession letter arrives postmarked the day after the funeral",
            "the missing person's diary continues past the date she disappeared",
            "a client pays in advance to prove a murder hasn't happened — yet",
            "the town's beloved founder is exhumed and the coffin is empty",
            "twin letters arrive: one confessing, one promising more",
        ],
        "tasks": [
            "untangle alibis woven thirty years ago",
            "find the witness everyone swears is dead",
            "decode a ledger hidden in plain sight",
            "trap a killer who knows the case file better than the investigators do",
            "close the one case everyone swore was closed for good",
        ],
        "deadlines": [
            "the statute expires",
            "the trial begins",
            "the tide gives up what it took",
            "the anniversary dinner raises its glass",
        ],
        "nouns": ["Verdict", "Ledger", "Alibi", "Inheritance", "Witness", "Confession", "Portrait", "Will", "Cipher", "Parish", "Autopsy", "Letter"],
        "adjs": ["Quiet", "Late", "Unquiet", "Perfect", "Missing", "Third", "Empty", "Painted", "Borrowed", "Final"],
        "places": ["Ashcombe", "Bellwether Lane", "Greywater Bay", "the Marlowe Estate", "Little Hawley", "Saint Alder's", "Windrow House", "the Fens"],
    },
    "thriller": {
        "label": "Thriller",
        "weight": 1100,
        "roles": [
            "a burnt analyst bounced from three agencies",
            "a hostage negotiator with one failure still on the board",
            "a private security contractor guarding clients nobody trusts",
            "a financial-crimes investigator drowning in clean money",
            "an interpreter attached to a peace delegation destined to fail",
            "a fixer for an embassy that doesn't officially exist",
            "a whistle-blower living under four names",
            "a crash investigator whose family died in row twelve",
        ],
        "routines": [
            "has spent {years} years following rules that keep getting rewritten",
            "works cases no one wants attributed",
            "keeps a go-bag packed and a lie polished",
            "hasn't slept through the night since the incident",
        ],
        "incitings": [
            "a burner phone that shouldn't exist starts ringing with a familiar voice on the line",
            "every record of a flight vanishes while it's still in the air",
            "a dead handler sends a meeting invitation for tomorrow",
            "the safe house is listed for sale — with photos of the inside",
            "a voiceprint unlocks a server on another continent",
            "a stranger returns a favor that never happened, with interest owed",
        ],
        "tasks": [
            "extract a defector who may be the bait",
            "stop an attack scheduled to look like an accident",
            "burn the network that did the training",
            "trade the one secret worth killing for",
            "get the truth past three governments and one assassin",
        ],
        "deadlines": [
            "the summit convenes",
            "the markets open in Frankfurt",
            "the border checkpoint shifts change",
            "the extraction flight leaves at dawn",
        ],
        "nouns": ["Asset", "Protocol", "Safehouse", "Debt", "Contact", "Extraction", "Cover", "Drop", "Cipher", "Border", "Deadline", "Ghost"],
        "adjs": ["Burnt", "Clean", "Live", "Deep", "Quiet", "Hard", "Cold", "Double", "Loose", "Sharp"],
        "places": ["Vienna", "the Free Port", "Kowloon", "Tashkent", "the DMZ", "Geneva", "Marseille's old port", "the Green Zone"],
    },
    "romance": {
        "label": "Romance",
        "weight": 1050,
        "roles": [
            "a pastry chef whose café is three missed payments from gone",
            "a wedding planner who doesn't believe in weddings anymore",
            "a lighthouse keeper's granddaughter and part-time novelist",
            "a cellist recovering from one catastrophic final performance",
            "a vineyard owner who inherited debts instead of grapes",
            "a ghostwriter secretly penning a rival's memoirs",
            "a single parent running the town's only bookshop",
            "a marine biologist counting turtles instead of heartbreaks",
        ],
        "routines": [
            "has spent {years} years rebuilding a life measured in small safe steps",
            "swears the heart is a muscle like any other: trainable, containable",
            "keeps love in the past tense where it belongs",
            "believes second chances are for people with better timing",
        ],
        "incitings": [
            "the person behind a decade of letters moves in next door",
            "a snowstorm strands two rivals with the best mistake of their twenties",
            "two estranged names appear on the same impossibly stubborn orchard deed",
            "a fake date to survive a family reunion feels too real by dessert",
            "the anonymous pen-pal assignment pairs enemies instead of strangers",
            "a lost letter surfaces, postmarked eleven years ago",
        ],
        "tasks": [
            "risk the whole heart instead of lending pieces",
            "choose between the career that saved everything and the person who sees clearly at last",
            "say the sentence that has been rehearsed for a decade",
            "let someone stay after the last train leaves",
            "forgive the person in the mirror first",
        ],
        "deadlines": [
            "the festival ends",
            "the vineyard's first harvest comes in",
            "the bakery lease runs out",
            "the last ferry of the season departs",
        ],
        "nouns": ["Letters", "Orchard", "Tide", "Bakery", "Harbor", "Promise", "Summer", "Songbook", "Kitchen", "Postcard", "Garden", "Vow"],
        "adjs": ["Second", "Slow", "Unexpected", "Last", "Sweet", "Small", "Impossible", "Late", "Quiet", "Whole"],
        "places": ["Port Alder", "Rosewater Lane", "the Crescent Cove", "Maple Hollow", "Bellbird Bay", "Junebug Creek", "the Old Mill House", "Sandpiper Point"],
    },
    "horror": {
        "label": "Horror",
        "weight": 900,
        "roles": [
            "a hospice nurse who hears the dying count backwards",
            "an urban explorer mapping tunnels that aren't on any survey",
            "a folklorist recording songs the village refuses to sing twice",
            "the new teacher at a school with a missing-class problem",
            "a property surveyor appraising a house that appraises back",
            "a radio host taking calls from listeners who died last week",
            "a twin who came home to bury the wrong sibling",
            "a pest controller called to something with fingerprints",
        ],
        "routines": [
            "has spent {years} years telling themselves the noises have explanations",
            "documents everything, because documentation is a kind of prayer",
            "doesn't believe, has never believed, will not begin believing now",
            "keeps the lights on and the doors counted",
        ],
        "incitings": [
            "every mirror in the house starts reflecting the room one second late",
            "the village's church bell rings although the bell was melted down in 1911",
            "the childhood imaginary friend is waiting on the porch, unchanged",
            "the excavation crew unearths a door, sealed from the inside",
            "the sleep recordings capture a second voice answering questions",
            "all the photographs from grandma's house now include an extra chair",
        ],
        "tasks": [
            "finish the ritual the founders started",
            "get the family out ahead of the count",
            "learn the song's last verse without singing along",
            "hold out until sunrise with the truth about what was invited in",
            "return what was taken in 1974",
        ],
        "deadlines": [
            "the frost writes its final pattern",
            "the harvest moon rises",
            "the well refills",
            "the last resident signs the papers",
        ],
        "nouns": ["House", "Hymn", "Well", "Bell", "Harvest", "Smile", "Room", "Visitor", "Choir", "Winter", "Portrait", "Cellar"],
        "adjs": ["Quiet", "Smiling", "Patient", "Hungry", "Sleeping", "Wrong", "Kindly", "Endless", "Pale", "Listening"],
        "places": ["Harrow Glen", "the Bell House", "Cold Spring", "Vessel Farm", "the Undercroft", "Marrow Creek", "Old Chapel Road", "the Ninth Floor"],
    },
    "historical-fiction": {
        "label": "Historical Fiction",
        "weight": 850,
        "roles": [
            "a typeface cutter's daughter in a print shop on the eve of a revolution",
            "a battlefield nurse keeping a ledger of the names officers omit",
            "a pearl diver's child indentured to a trading company",
            "a code-carrying courier on the last diplomatic mission of a doomed republic",
            "a widowed lighthouse keeper during the year of the great storms",
            "an apprentice clockmaker summoned to repair the observatory's master clock",
            "a suffragist's driver who reads every letter before delivering it",
            "a mapmaker's apprentice finishing the atlas the master died for",
        ],
        "routines": [
            "has spent {years} years learning which silences keep people safe",
            "measures the world in what can be carried when the orders come",
            "keeps a low profile and busy hands",
            "believes history happens to other people, elsewhere",
        ],
        "incitings": [
            "a sealed letter names the family in a plot no one wants a part of",
            "the army requisitions the town and the ledger with all the names",
            "a stranger arrives carrying unmistakable handwriting from a supposed corpse",
            "the census taker asks one question too many",
            "the bridge — the only road out — closes for the season",
            "a child is left at the door with instructions to forget the face",
        ],
        "tasks": [
            "smuggle the evidence past three checkpoints",
            "finish the work while the workshop still stands",
            "choose which family member gets the last berth",
            "keep a promise made in peacetime to someone now declared enemy",
            "get the truth on the record ahead of the victors' historians",
        ],
        "deadlines": [
            "the ice breaks on the river",
            "the armistice is signed — or isn't",
            "the ship sails on the morning tide",
            "the century turns",
        ],
        "nouns": ["Atlas", "Ledger", "Compass", "Typewriter", "Harbor", "Regiment", "Clock", "Letter", "Bridge", "Orchard", "Uniform", "Lantern"],
        "adjs": ["Last", "Borrowed", "Paper", "Iron", "Quiet", "Winter", "Long", "Unwritten", "Copper", "Faithful"],
        "places": ["Port Mahon", "the Lower Danube", "Vilna", "the Cape Route", "Manchester's mill district", "Valparaíso", "the Palatinate", "Nagasaki's harbor"],
    },
    "literary-fiction": {
        "label": "Literary Fiction",
        "weight": 750,
        "roles": [
            "a translator losing a childhood language one borrowed word at a time",
            "a piano tuner who hears the house's history in its radiators",
            "an heir cataloging a parent's silence after the funeral",
            "a night librarian in a city that sleeps less every year",
            "a former prodigy returning to the conservatory as a janitor",
            "a letter-writer sending postcards to an address that burned down years ago",
            "a bridge inspector measuring the marriage in expansion joints",
            "a restaurant critic who has forgotten how food tastes",
        ],
        "routines": [
            "has spent {years} years practicing the art of almost saying it",
            "keeps a careful inventory of everything unsaid",
            "moves through the days like a tenant, not an owner",
            "has perfected the smile that ends conversations",
        ],
        "incitings": [
            "a box of undelivered letters surfaces behind a wardrobe",
            "a childhood home goes up for auction",
            "a stranger at the funeral knows the family by a name nobody uses",
            "the last speaker of a language asks for one final student",
            "a song on the radio is one that was written and never recorded",
        ],
        "tasks": [
            "ask the question the whole family arranged itself around",
            "return to the place where the story went wrong",
            "say goodbye properly, at last, out loud",
            "translate the untranslatable sentence and live with it",
            "forgive the stranger in the old photographs",
        ],
        "deadlines": [
            "the house sale closes",
            "the mother's memory goes entirely",
            "the demolition date arrives",
            "the last bus to the old neighborhood is rerouted forever",
        ],
        "nouns": ["Inventory", "Silence", "Blue Hour", "Wardrobe", "Language", "Radiators", "Postcards", "Glasshouse", "Undertow", "Interior", "Weather", "Aftermath"],
        "adjs": ["Late", "Small", "Borrowed", "Quiet", "Unsaid", "Half-Light", "Distant", "Ordinary", "Slow", "Necessary"],
        "places": ["the fourth floor walk-up", "Milton Flats", "the coast road", "Anderlecht", "the family house on Kessler Street", "the reservoir", "Room 214", "the old quarter"],
    },
    "adventure": {
        "label": "Adventure",
        "weight": 700,
        "roles": [
            "a riverboat captain who knows every sandbar's mood",
            "a mountain guide blacklisted from two countries",
            "a salvage diver working a wreck the navy won't discuss",
            "a bush pilot flying medicine and rumors into the interior",
            "a desert ranger tracking a thief across nothing",
            "a railroad engineer with a map of closed lines",
            "an archaeologist's estranged child and better digger",
            "a storm chaser who owes money to dangerous optimists",
        ],
        "routines": [
            "has spent {years} years measuring life in miles rather than years",
            "keeps moving because stopping costs more",
            "knows the wilderness forgives nothing and forgets less",
            "carries a compass, a debt, and very little else",
        ],
        "incitings": [
            "a dying prospector trades a map for a promise",
            "the river gives up a chest stamped with a dead nation's seal",
            "an expedition upriver stops answering the radio",
            "a government survey team vanishes, leaving gear and no tracks",
            "the tide reveals a cave that legends charge admission to",
            "an old rival hires the crew for the one job that was sworn off long ago",
        ],
        "tasks": [
            "cross the range ahead of the snows",
            "beat the salvage fleet to the wreck by six tides",
            "bring the expedition home without telling anyone what it found",
            "follow a river upstream to its forbidden source",
            "outlast the monsoon with a leaking boat and a stranger's help",
        ],
        "deadlines": [
            "the dry season ends",
            "the concession permits expire",
            "the glacier calving season opens the route — briefly",
            "the monsoon makes landfall",
        ],
        "nouns": ["Passage", "Current", "Summit", "Wreck", "Monsoon", "Compass", "Trail", "Rivergate", "Escarpment", "Horizon", "Provision", "Landfall"],
        "adjs": ["Broken", "Open", "Far", "Salt", "High", "Lost", "Rough", "Last", "Leeward", "Uncharted"],
        "places": ["the Sepik Basin", "Cape Reckoning", "the Empty Quarter", "Mount Kessler", "the Coral Triangle", "Patagonia's dry side", "the Upper Fly River", "Devil's Throat"],
    },
    "young-adult": {
        "label": "Young Adult",
        "weight": 500,
        "roles": [
            "the new kid at a school built over something old",
            "a scholarship student at an academy with too many secrets",
            "a baker's kid who bakes feelings into bread",
            "the team's statistician who knows the game is rigged",
            "the eldest sibling raising the younger ones while mom works nights",
            "a debate champion who can't win the argument at home",
            "the only out kid in a town of nine hundred",
            "a coder whose anonymous account knows too much",
        ],
        "routines": [
            "has spent {years} years being so careful it hurts",
            "stays under the radar: head down, grades up, locker shut",
            "counts days until graduation like a sentence being served",
            "is fine. Everything is fine. Obviously.",
        ],
        "incitings": [
            "a group chat starts predicting things that haven't happened yet",
            "the teacher pairs nemesis with nemesis for a semester-long project",
            "grandma's recipe box contains directions that aren't for food",
            "the school's legendary ghost starts leaving notes addressed by name — in impossible ink",
            "a best friend goes missing, leaving only a set of keys behind",
            "the college essay prompt asks one honest question nobody can stop answering",
        ],
        "tasks": [
            "decide who to be when the labels come off",
            "save the tradition that made the town",
            "expose what the school board buried",
            "tell the truth even if it costs the friendship",
            "win the championship that doesn't matter — and the one that does",
        ],
        "deadlines": [
            "prom",
            "the final audition",
            "the last game of the season",
            "graduation",
        ],
        "nouns": ["Semester", "Mixtape", "Tryouts", "Locker", "Homecoming", "Recipe", "Group Chat", "Yearbook", "Detention", "Scholarship", "Playlist", "Prom"],
        "adjs": ["Fake", "Almost", "Secret", "Last", "Unofficial", "Best", "Broken", "Unexpected", "Sixteenth", "Quiet"],
        "places": ["Cedar Falls", "Westbrook High", "the water tower", "Maple Street", "Lake Minnow", "the band room", "Route 9", "the quarry"],
    },
}

LENGTH_WEIGHTS = [("short-story", 8), ("novella", 27), ("novel", 55), ("epic", 10)]
GENRE_CODES = {
    "fantasy": "FAN", "science-fiction": "SCI", "mystery": "MYS",
    "thriller": "THR", "romance": "ROM", "horror": "HOR",
    "historical-fiction": "HIS", "literary-fiction": "LIT",
    "adventure": "ADV", "young-adult": "YNG",
}


# ---------------------------------------------------------------- utilities

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text or "untitled"


def weighted(rng: random.Random, table: list[tuple[str, int]]) -> str:
    total = sum(w for _, w in table)
    roll = rng.randrange(total)
    for value, weight in table:
        if roll < weight:
            return value
        roll -= weight
    return table[-1][0]


def pick_unique(rng: random.Random, pool: list[str], n: int) -> list[str]:
    return rng.sample(pool, min(n, len(pool)))


def fill(template: str, rng: random.Random) -> str:
    return template.replace("{years}", rng.choice(YEARS))


# ------------------------------------------------------------ book factory

def make_title(rng: random.Random, shelf: dict) -> tuple[str, str]:
    """Return (title, pattern_name); callers re-roll on duplicates."""
    pattern = rng.randrange(8)
    noun = lambda: rng.choice(shelf["nouns"])
    adj = lambda: rng.choice(shelf["adjs"])
    place = lambda: rng.choice(shelf["places"])
    name = lambda: rng.choice(FIRST_NAMES)
    if pattern == 0:
        return f"The {adj()} {noun()}", "adj-noun"
    if pattern == 1:
        return f"The {noun()} of {place()}", "noun-of-place"
    if pattern == 2:
        first = noun()
        second = noun()
        while second == first:
            second = rng.choice(shelf["nouns"])
        return f"{first} and {second}", "noun-and-noun"
    if pattern == 3:
        return f"{place()} Rising", "place-rising"
    if pattern == 4:
        return f"The Last {noun()}", "last-noun"
    if pattern == 5:
        first = noun()
        second = noun()
        while second == first:
            second = rng.choice(shelf["nouns"])
        return f"A {first} for the {second}", "noun-for-noun"
    if pattern == 6:
        return f"When the {noun()} {rng.choice(['Sings', 'Breaks', 'Burns', 'Falls', 'Wakes', 'Turns'])}", "when-the-noun"
    return f"{name()} and the {noun()}", "name-and-noun"


def make_blurb(rng: random.Random, shelf: dict) -> str:
    protag = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}, {rng.choice(shelf['roles'])}"
    routine = fill(rng.choice(shelf["routines"]), rng)
    pronoun = rng.choice(["she", "he", "they"])
    verb = lambda third, plural: plural if pronoun == "they" else third
    inciting = rng.choice(shelf["incitings"])
    task = rng.choice(shelf["tasks"])
    deadline = rng.choice(shelf["deadlines"])
    s1 = f"{protag}, {routine}."
    s2 = (f"But when {inciting}, {pronoun} {verb('discovers', 'discover')} "
          "that staying invisible was never really an option.")
    alt2 = f"Then {inciting} — and {pronoun} {verb('is', 'are')} pulled straight into the middle of it."
    s3 = f"To get through this, {pronoun} must {task} before {deadline}."
    alt3 = f"Now {pronoun} must {task}, and time is already running out."
    return " ".join([s1, rng.choice([s2, alt2]), rng.choice([s3, alt3])])


def unique_title(seed: str, index: int, shelf: dict, taken: set[str],
                 rng: random.Random) -> str:
    """Deterministically re-roll titles until one is unused."""
    for attempt in range(40):
        title, _ = make_title(random.Random(f"{seed}:{index}:title:{attempt}"), shelf)
        if title.lower() not in taken:
            return title
    return f"{title} {rng.choice(['Revisited', 'Again', 'Anew'])}"


def make_book(index: int, seed: str, genre_key: str,
              taken_titles: set[str]) -> dict[str, Any]:
    rng = random.Random(f"{seed}:{index}")
    shelf = GENRES[genre_key]
    title = unique_title(seed, index, shelf, taken_titles, rng)
    rating = round(max(3.0, min(5.0, rng.triangular(3.4, 5.0, 4.15))), 1)
    return {
        "id": f"{GENRE_CODES[genre_key]}-{index:05d}",
        "title": title,
        "author": build_author(rng),
        "genre": shelf["label"],
        "length": weighted(rng, LENGTH_WEIGHTS),
        "rating": rating,
        "blurb": make_blurb(rng, shelf),
        "themes": pick_unique(rng, DEFAULT_THEMES[genre_key], 3),
        "style": rng.choice(DEFAULT_STYLES[genre_key]),
        "language": "English",
        "catalog": {"source": "make_catalog.py", "seed": seed, "index": index},
    }


def build_author(rng: random.Random) -> str:
    name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
    if rng.random() < 0.12:
        parts = name.split()
        name = f"{parts[0][0]}. M. {parts[-1]}" if len(parts) > 1 else name
    return name


DEFAULT_THEMES = {key: [
    "found family", "loyalty vs. truth", "the price of survival", "inheritance",
    "identity", "power and its corruption", "memory", "justice outside the law",
    "love against duty", "belonging",
] for key in GENRES}

DEFAULT_STYLES = {key: [
    "vivid, cinematic prose with tight pacing",
    "warm, character-driven storytelling with gentle humor",
    "atmospheric and lyrical, with strong sensory detail",
    "crisp modern voice, short chapters, propulsive momentum",
    "richly descriptive with an intimate third-person narration",
    "wry first-person narration with emotional depth",
] for key in GENRES}


# ------------------------------------------------------------------- main

def existing_state(books_dir: Path) -> tuple[set[str], set[str]]:
    """Scan current specs: return (known titles, protected human-authored dirs)."""
    titles, protected = set(), set()
    if books_dir.is_dir():
        for path in books_dir.rglob(SPEC_FILE):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                title = str(raw.get("title") or "").strip().lower()
                if title:
                    titles.add(title)
                if "catalog" not in raw:
                    protected.add(path.parent.name)
            except (OSError, json.JSONDecodeError):
                protected.add(path.parent.name)
    return titles, protected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--count", type=int, default=10_000)
    parser.add_argument("--seed", default="2026")
    parser.add_argument("--genres", help="comma-separated subset of genre keys")
    parser.add_argument("--books-dir", type=Path, default=BOOKS_DIR)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true",
                        help="overwrite previously generated specs (never touches hand-written ones)")
    args = parser.parse_args(argv)

    genre_keys = ([g.strip() for g in args.genres.split(",")] if args.genres
                  else list(GENRES))
    unknown = [g for g in genre_keys if g not in GENRES]
    if unknown:
        parser.error(f"unknown genre(s): {', '.join(unknown)}. "
                     f"Known: {', '.join(GENRES)}")

    total_weight = sum(GENRES[g]["weight"] for g in genre_keys)
    plan = {}
    for g in genre_keys:
        share = GENRES[g]["weight"] / total_weight
        plan[g] = int(args.count * share + 0.5)

    known_titles, protected_dirs = existing_state(args.books_dir)
    preexisting = set()
    if args.books_dir.is_dir():
        for p in args.books_dir.rglob(SPEC_FILE):
            preexisting.add(p)

    if args.dry_run:
        print("Plan:")
        for g, n in plan.items():
            print(f"  books/{g:<20} {n:>6} books")
        print(f"  {'TOTAL':<21} {sum(plan.values()):>6}")
        return 0

    written, kept_existing, skipped_protected = 0, 0, 0
    global_index = 0
    for genre_key in sorted(genre_keys):
        target = plan[genre_key]
        made_in_genre = 0
        attempts = 0
        max_attempts = target * 3 + 500
        while made_in_genre < target and attempts < max_attempts:
            attempts += 1
            global_index += 1
            book = make_book(global_index, args.seed, genre_key, known_titles)
            base_slug = slugify(book["title"])

            # Never touch folders that hold human-written specs.
            if base_slug in protected_dirs or any(
                s.startswith(base_slug + "-") and s[len(base_slug) + 1:].isdigit()
                for s in protected_dirs
            ):
                skipped_protected += 1
                continue

            folder = args.books_dir / genre_key / base_slug
            spec_path = folder / SPEC_FILE

            if spec_path.exists() and spec_path in preexisting:
                try:
                    old = json.loads(spec_path.read_text(encoding="utf-8"))
                    generated = isinstance(old, dict) and "catalog" in old
                except (OSError, json.JSONDecodeError):
                    generated = False
                if not generated:
                    suffix = 2
                    while (args.books_dir / genre_key / f"{base_slug}-{suffix}").exists():
                        suffix += 1
                    folder = args.books_dir / genre_key / f"{base_slug}-{suffix}"
                    spec_path = folder / SPEC_FILE
                elif not args.force:
                    # Same seed produced this file before: keep it byte-stable.
                    known_titles.add(book["title"].lower())
                    made_in_genre += 1
                    kept_existing += 1
                    continue
            else:
                # Same run already wrote this slug (distinct titles can share
                # one slug after punctuation is stripped): suffix and move on.
                while spec_path.exists():
                    folder = folder.with_name(
                        re.sub(r"-(\d+)$", lambda m: f"-{int(m.group(1)) + 1}", folder.name)
                        if re.search(r"-(\d+)$", folder.name) else f"{folder.name}-2"
                    )
                    spec_path = folder / SPEC_FILE

            atomic_write(spec_path, json.dumps(book, indent=2, ensure_ascii=False) + "\n")
            known_titles.add(book["title"].lower())
            made_in_genre += 1
            written += 1
        print(f"[shelf] {genre_key:<20} {made_in_genre:>6}/{target} specs ready")

    print(f"\nDone: {written} written, {kept_existing} already present (kept), "
          f"{skipped_protected} collisions with hand-written specs skipped.")
    return 0


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


if __name__ == "__main__":
    sys.exit(main())
