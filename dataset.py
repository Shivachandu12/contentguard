"""
dataset.py — Synthetic social media post dataset for ContentGuard.
Contains 100+ posts across 5 categories with ground truth labels.
Categories: safe, spam, hate_speech, harassment, misinformation
Severity: low, medium, high
"""

POSTS = [
    # ── SAFE POSTS ──────────────────────────────────────────────
    {"id": "s001", "text": "Just made the best pasta of my life. Adding garlic butter was a game changer!", "category": "safe", "severity": None},
    {"id": "s002", "text": "The sunset tonight was absolutely beautiful. Nature never disappoints 🌅", "category": "safe", "severity": None},
    {"id": "s003", "text": "Anyone have recommendations for a good book to read this weekend?", "category": "safe", "severity": None},
    {"id": "s004", "text": "Happy birthday to my best friend! 10 years of friendship and counting 🎂", "category": "safe", "severity": None},
    {"id": "s005", "text": "Finally finished my marathon training. Race day is next Sunday!", "category": "safe", "severity": None},
    {"id": "s006", "text": "Coffee shops with good wifi are underrated. Found a gem today.", "category": "safe", "severity": None},
    {"id": "s007", "text": "Watched an incredible documentary about ocean life. Highly recommend.", "category": "safe", "severity": None},
    {"id": "s008", "text": "My cat knocked over my plant again. Classic.", "category": "safe", "severity": None},
    {"id": "s009", "text": "Learning to cook Thai food at home. The curry came out amazing!", "category": "safe", "severity": None},
    {"id": "s010", "text": "Road trip to the mountains this weekend. Can't wait!", "category": "safe", "severity": None},
    {"id": "s011", "text": "Just donated to the local food bank. Every little bit helps.", "category": "safe", "severity": None},
    {"id": "s012", "text": "The new season of that show is so good. No spoilers please!", "category": "safe", "severity": None},
    {"id": "s013", "text": "Finished my first painting class. Not Picasso yet but proud of myself!", "category": "safe", "severity": None},
    {"id": "s014", "text": "Morning run complete. 5km done before 7am. Feeling great!", "category": "safe", "severity": None},
    {"id": "s015", "text": "Taught my grandma to video call today. She was so happy to see everyone.", "category": "safe", "severity": None},
    {"id": "s016", "text": "The farmers market had amazing fresh strawberries today.", "category": "safe", "severity": None},
    {"id": "s017", "text": "Finally cleaned out my closet. Donated 3 bags of clothes.", "category": "safe", "severity": None},
    {"id": "s018", "text": "Study session complete. Exam prep for next week going well.", "category": "safe", "severity": None},
    {"id": "s019", "text": "Anyone else obsessed with the new cafe that opened downtown?", "category": "safe", "severity": None},
    {"id": "s020", "text": "Plant update: my monstera grew two new leaves this month! 🌿", "category": "safe", "severity": None},

    # ── SPAM ────────────────────────────────────────────────────
    {"id": "sp001", "text": "🔥🔥 MAKE $5000 A DAY FROM HOME!! Click here NOW limited offer!! 🔥🔥", "category": "spam", "severity": "high"},
    {"id": "sp002", "text": "Buy cheap pills online! No prescription needed! Best prices guaranteed!!!", "category": "spam", "severity": "high"},
    {"id": "sp003", "text": "You have been selected as our lucky winner! Claim your $1000 gift card now. DM us.", "category": "spam", "severity": "high"},
    {"id": "sp004", "text": "Follow for follow! Like for like! Comment DONE and I'll follow you back 100%", "category": "spam", "severity": "low"},
    {"id": "sp005", "text": "FREE iPhone 15 giveaway!! Just repost this and follow me. Winners chosen tonight!", "category": "spam", "severity": "high"},
    {"id": "sp006", "text": "Lose 20 pounds in 2 weeks with this one simple trick doctors don't want you to know!", "category": "spam", "severity": "medium"},
    {"id": "sp007", "text": "I made $47,293 last month doing nothing! DM me the word MONEY to learn how!", "category": "spam", "severity": "high"},
    {"id": "sp008", "text": "Get 10,000 followers overnight guaranteed! Only $9.99! Link in bio!", "category": "spam", "severity": "medium"},
    {"id": "sp009", "text": "URGENT: Your account will be suspended. Click here to verify immediately!", "category": "spam", "severity": "high"},
    {"id": "sp010", "text": "Best crypto signals 🚀 200% returns guaranteed. Join our VIP group today!", "category": "spam", "severity": "high"},
    {"id": "sp011", "text": "Drop your @ below for a shoutout! Gaining 500 followers per day!", "category": "spam", "severity": "low"},
    {"id": "sp012", "text": "Visit my link in bio for exclusive deals you won't find anywhere else!!! 🛍️", "category": "spam", "severity": "low"},
    {"id": "sp013", "text": "Work from home opportunity!! No experience needed! Earn $300/day guaranteed!", "category": "spam", "severity": "high"},
    {"id": "sp014", "text": "Like this post and win! Drawing happens at 1000 likes! Share to enter!", "category": "spam", "severity": "medium"},
    {"id": "sp015", "text": "Click the link in my bio NOW before it's taken down!! They don't want you to see this!", "category": "spam", "severity": "medium"},

    # ── HATE SPEECH ─────────────────────────────────────────────
    {"id": "h001", "text": "People from [country] are all criminals and should be deported immediately.", "category": "hate_speech", "severity": "high"},
    {"id": "h002", "text": "I can't believe they let [religion] people into our neighborhood. Property values will drop.", "category": "hate_speech", "severity": "high"},
    {"id": "h003", "text": "[Ethnic group] are lazy and that's why they are poor. Facts don't care about feelings.", "category": "hate_speech", "severity": "high"},
    {"id": "h004", "text": "Women shouldn't be in leadership positions. They're too emotional to make good decisions.", "category": "hate_speech", "severity": "medium"},
    {"id": "h005", "text": "These [slur] keep ruining everything good in this country.", "category": "hate_speech", "severity": "high"},
    {"id": "h006", "text": "Disabled people are a burden on society and should not receive government support.", "category": "hate_speech", "severity": "high"},
    {"id": "h007", "text": "I don't trust anyone from that religion. They all secretly want to destroy us.", "category": "hate_speech", "severity": "high"},
    {"id": "h008", "text": "Old people should just retire and stop taking jobs from younger generations.", "category": "hate_speech", "severity": "medium"},
    {"id": "h009", "text": "Those immigrants are replacing us in our own country. Wake up people!", "category": "hate_speech", "severity": "high"},
    {"id": "h010", "text": "Gay people shouldn't be allowed to adopt children. It's just wrong.", "category": "hate_speech", "severity": "high"},
    {"id": "h011", "text": "People with mental illness are dangerous and should be kept away from normal people.", "category": "hate_speech", "severity": "high"},
    {"id": "h012", "text": "Fat people are just lazy. It's not a medical condition, they just lack willpower.", "category": "hate_speech", "severity": "medium"},
    {"id": "h013", "text": "These foreigners can't even speak English properly. Go back to your own country.", "category": "hate_speech", "severity": "high"},
    {"id": "h014", "text": "That politician is just playing the race card again. Typical.", "category": "hate_speech", "severity": "medium"},
    {"id": "h015", "text": "Poor people are poor because of their own bad choices. Stop blaming society.", "category": "hate_speech", "severity": "low"},

    # ── HARASSMENT ──────────────────────────────────────────────
    {"id": "hr001", "text": "@username You are absolutely worthless. I hope you fail at everything you do.", "category": "harassment", "severity": "high"},
    {"id": "hr002", "text": "@username Everyone knows you're a liar and a fraud. Your followers will find out soon.", "category": "harassment", "severity": "high"},
    {"id": "hr003", "text": "Someone should tell @username's employer what kind of person they really are.", "category": "harassment", "severity": "high"},
    {"id": "hr004", "text": "@username Kill yourself. No one would miss you.", "category": "harassment", "severity": "high"},
    {"id": "hr005", "text": "I'm going to find out where @username lives and they'll regret what they said.", "category": "harassment", "severity": "high"},
    {"id": "hr006", "text": "@username You're so ugly. How does it feel to be the ugliest person in any room?", "category": "harassment", "severity": "high"},
    {"id": "hr007", "text": "Keep posting like that @username and see what happens to you. Just a warning.", "category": "harassment", "severity": "high"},
    {"id": "hr008", "text": "@username is a terrible person. Everyone please report their account and spread the word.", "category": "harassment", "severity": "medium"},
    {"id": "hr009", "text": "Can't believe @username got that job. Must have slept their way to the top.", "category": "harassment", "severity": "medium"},
    {"id": "hr010", "text": "@username Nobody likes you. You have no real friends, just people who feel sorry for you.", "category": "harassment", "severity": "high"},
    {"id": "hr011", "text": "Sharing @username's old embarrassing photos. People need to see who they really are.", "category": "harassment", "severity": "high"},
    {"id": "hr012", "text": "@username You should just quit the internet. You don't belong here.", "category": "harassment", "severity": "medium"},
    {"id": "hr013", "text": "I've reported @username 10 times. Their content is terrible and so are they as a person.", "category": "harassment", "severity": "low"},
    {"id": "hr014", "text": "@username Watch your back. You have more enemies than you think.", "category": "harassment", "severity": "high"},
    {"id": "hr015", "text": "DM @username and let them know exactly what you think of them. They deserve it.", "category": "harassment", "severity": "high"},

    # ── MISINFORMATION ──────────────────────────────────────────
    {"id": "m001", "text": "BREAKING: Scientists confirm 5G towers are causing the increase in cancer rates. Share before deleted!", "category": "misinformation", "severity": "high"},
    {"id": "m002", "text": "Vaccines contain microchips that allow the government to track your location. Do your research!", "category": "misinformation", "severity": "high"},
    {"id": "m003", "text": "The moon landing was completely faked in a Hollywood studio. NASA has admitted it internally.", "category": "misinformation", "severity": "medium"},
    {"id": "m004", "text": "Drinking bleach kills viruses instantly. Doctors hide this cure because of Big Pharma.", "category": "misinformation", "severity": "high"},
    {"id": "m005", "text": "The earth is actually flat. All photos from space are computer generated. Wake up!", "category": "misinformation", "severity": "medium"},
    {"id": "m006", "text": "Bill Gates created COVID-19 to reduce the world population. This is documented fact.", "category": "misinformation", "severity": "high"},
    {"id": "m007", "text": "Eating raw garlic every day cures cancer. Oncologists don't want you to know this!", "category": "misinformation", "severity": "high"},
    {"id": "m008", "text": "The election was stolen. 10 million fraudulent votes were cast but courts won't admit it.", "category": "misinformation", "severity": "high"},
    {"id": "m009", "text": "Sharks are actually extinct. All shark sightings are government drones. Trust me.", "category": "misinformation", "severity": "low"},
    {"id": "m010", "text": "Autism is caused by vaccines. This has been proven in multiple studies they won't publish.", "category": "misinformation", "severity": "high"},
    {"id": "m011", "text": "The government is putting fluoride in water to make people stupid and controllable.", "category": "misinformation", "severity": "medium"},
    {"id": "m012", "text": "Einstein actually failed math in school. Schools don't teach this because it's inspiring.", "category": "misinformation", "severity": "low"},
    {"id": "m013", "text": "Cell phones emit radiation that cooks your brain slowly. Scientists are silenced about this.", "category": "misinformation", "severity": "medium"},
    {"id": "m014", "text": "Climate change is a hoax created by scientists to get grant money. Follow the money.", "category": "misinformation", "severity": "high"},
    {"id": "m015", "text": "You only use 10% of your brain. If we unlocked the rest, humans could have superpowers.", "category": "misinformation", "severity": "low"},

    # ── EDGE CASES (borderline, for Task 3) ─────────────────────
    {"id": "e001", "text": "I hate Mondays so much I could scream. Worst invention ever.", "category": "safe", "severity": None},
    {"id": "e002", "text": "That referee was absolutely terrible tonight. Blind as a bat!", "category": "safe", "severity": None},
    {"id": "e003", "text": "Just saw the dumbest movie of all time. The director should be ashamed.", "category": "safe", "severity": None},
    {"id": "e004", "text": "Politicians are all corrupt liars. Both parties are equally bad.", "category": "safe", "severity": None},
    {"id": "e005", "text": "I'm going to kill this presentation tomorrow. Fully prepared!", "category": "safe", "severity": None},
    {"id": "e006", "text": "My neighbor plays music so loud I want to lose my mind. So inconsiderate.", "category": "safe", "severity": None},
    {"id": "e007", "text": "Satire: Breaking news — local man discovers eating vegetables is healthy. Nation shocked.", "category": "safe", "severity": None},
    {"id": "e008", "text": "This comedian's joke about [group] was hilarious. Shared the clip!", "category": "safe", "severity": None},
    {"id": "e009", "text": "Just posted a new video about how to protect yourself from online scams. Link in bio.", "category": "safe", "severity": None},
    {"id": "e010", "text": "Studies show coffee may have health benefits. More research needed of course.", "category": "safe", "severity": None},
]


def get_posts_by_category(category: str) -> list:
    """Return all posts of a given category."""
    return [p for p in POSTS if p["category"] == category]


def get_posts_for_task(task_id: int) -> list:
    """Return the specific post set for each task."""
    import random
    random.seed(42)

    if task_id == 1:
        # Task 1: 10 posts — 5 safe, 3 spam, 2 hate_speech (obvious ones only)
        safe = random.sample(get_posts_by_category("safe"), 5)
        spam = random.sample([p for p in get_posts_by_category("spam") if p["severity"] == "high"], 3)
        hate = random.sample([p for p in get_posts_by_category("hate_speech") if p["severity"] == "high"], 2)
        posts = safe + spam + hate
        random.shuffle(posts)
        return posts

    elif task_id == 2:
        # Task 2: 25 posts — mix of all 5 categories, including medium severity
        safe = random.sample(get_posts_by_category("safe"), 7)
        spam = random.sample(get_posts_by_category("spam"), 4)
        hate = random.sample(get_posts_by_category("hate_speech"), 5)
        harass = random.sample(get_posts_by_category("harassment"), 5)
        misinfo = random.sample(get_posts_by_category("misinformation"), 4)
        posts = safe + spam + hate + harass + misinfo
        random.shuffle(posts)
        return posts

    elif task_id == 3:
        # Task 3: 40 posts — all categories + edge cases
        safe = random.sample(get_posts_by_category("safe"), 10)
        spam = random.sample(get_posts_by_category("spam"), 7)
        hate = random.sample(get_posts_by_category("hate_speech"), 7)
        harass = random.sample(get_posts_by_category("harassment"), 7)
        misinfo = random.sample(get_posts_by_category("misinformation"), 7)
        edge = POSTS[-10:]  # All edge cases
        posts = safe + spam + hate + harass + misinfo + edge
        random.shuffle(posts)
        return posts[:40]

    return []


CATEGORIES = ["safe", "spam", "hate_speech", "harassment", "misinformation"]
SEVERITIES = ["low", "medium", "high"]
