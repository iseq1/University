import random
import csv
import re

random.seed(42)

LABEL_MAP = {
    "survival": "survival game",
    "fps": "first person shooter",
    "rpg": "role playing game",
    "strategy": "strategy game",
    "horror": "horror game",
    "sports": "sports game simulator",
    "simulation": "life simulation game",
    "sandbox": "free sandbox game",
}

GENRES = [
    "survival",
    "fps",
    "rpg",
    "strategy",
    "horror",
    "sports",
    "simulation",
    "sandbox",
]

GENRE_BLACKLIST = {
    "survival": ["survival", "survive", "zombies", "zombie"],
    "fps": ["shooter", "fps", "gun", "weapons", "shoot"],
    "rpg": ["rpg", "role playing", "quests", "magic"],
    "strategy": ["strategy", "tactics", "war"],
    "horror": ["horror", "scary", "fear", "dark"],
    "sports": ["football", "basketball", "sports", "racing"],
    "simulation": ["simulation", "simulator"],
    "sandbox": ["sandbox", "building", "creative", "crafting"],
}

TEMPLATES = {
    "survival": [
        "open world game in post apocalyptic environment with resource gathering",
        "harsh wilderness game where player must manage resources and stay alive",
        "exploration game in dangerous world with crafting system",
    ],
    "fps": [
        "fast paced competitive game with online multiplayer battles",
        "first person game with tactical combat and team based gameplay",
        "arena game focused on precision combat and multiplayer matches",
    ],
    "rpg": [
        "fantasy adventure game with character progression and quests",
        "story driven game with exploration and leveling system",
        "adventure game with skills, loot and narrative choices",
    ],
    "strategy": [
        "game focused on resource management and tactical decisions",
        "turn based game with armies and strategic planning",
        "real time game with base management and units control",
    ],
    "horror": [
        "game with dark atmosphere and psychological tension",
        "exploration game set in abandoned locations with survival elements",
        "narrative game with suspense and disturbing events",
    ],
    "sports": [
        "competitive game with teams and tournaments",
        "simulation of real world athletic competitions",
        "game focused on matches and scoring system",
    ],
    "simulation": [
        "realistic management game with economy and systems",
        "game simulating real world activities and control systems",
        "life management game with building mechanics",
    ],
    "sandbox": [
        "open environment game with creative freedom and physics",
        "game where player can build and modify world freely",
        "exploration based game with construction mechanics",
    ],
}


def clean_text(text, genre):
    blacklist = GENRE_BLACKLIST.get(genre, [])

    for word in blacklist:
        text = re.sub(rf"\b{word}\b", "", text, flags=re.IGNORECASE)

    # убрать двойные пробелы
    text = re.sub(r"\s+", " ", text).strip()

    return text


def generate_dataset(n=500):
    dataset = []

    for _ in range(n):
        genre = random.choice(GENRES)
        desc = random.choice(TEMPLATES[genre])

        # добавляем лёгкий шум (как Steam)
        if random.random() < 0.3:
            desc += " with multiplayer mode"
        if random.random() < 0.2:
            desc += " and exploration elements"

        desc = clean_text(desc, genre)

        dataset.append((desc, LABEL_MAP[genre]))

    return dataset


def save_csv(data, path="steam_dataset_clean.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["description", "genre"])
        writer.writerows(data)


if __name__ == "__main__":
    data = generate_dataset(500)

    save_csv(data)

    print("Dataset size:", len(data))
    print("\nSample:")
    for i in range(5):
        print(data[i])