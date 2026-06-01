"""
MICASA team data — fetched from micasa-design.com/team
Used during onboarding to match the new user's name.
"""

TEAM_BASE_URL = "https://micasa-design.com/team/img/"

TEAM_MEMBERS = [
    {"name": "Iskandar Mukhamedov",   "role": "Founder",                      "photo": "sohib.jpg"},
    {"name": "Yousef Husain Yousef",  "role": "UAE CEO",                      "photo": "yousef.jpg"},
    {"name": "Oybek Nazirov",         "role": "Russian Federation CEO",        "photo": "micasa-oybek.jpg"},
    {"name": "Aziza Mukhamedova",     "role": "International Manager",         "photo": "aziza.jpg"},
    {"name": "Aybek Jumanazarov",     "role": "Project Manager",              "photo": "micasa-oybekh.jpg"},
    {"name": "Badriddin Ashrapov",    "role": "Senior Technical Designer",     "photo": "micasa-badriddin.jpg"},
    {"name": "Asalya Azizova",        "role": "Interior Designer",             "photo": "micasa-asalia.jpg"},
    {"name": "Anvar Mukhibov",        "role": "Interior & Exterior Designer",  "photo": "micasa-anvar.jpg"},
    {"name": "Zafer Kamalov",         "role": "Interior & Exterior Designer",  "photo": "micasa-zefer.jpg"},
    {"name": "Tatyana Kasimova",      "role": "Interior Designer",             "photo": "micasa-tanya.jpg"},
    {"name": "Doniyor Makhmudov",     "role": "Interior Designer",             "photo": "micasa-doniyor.jpg"},
    {"name": "Alisher Sadikov",       "role": "Interior Designer",             "photo": "micasa-alisher.jpg"},
    {"name": "Kamila Kasimova",       "role": "Interior Designer",             "photo": "micasa-logo.jpg"},
    {"name": "Zakir Zakirov",         "role": "Interior & Exterior Designer",  "photo": "micasa-zakir.jpg"},
    {"name": "Abduqodir Mirdadaev",   "role": "Senior Architect",              "photo": "micasa-abduqodir.jpg"},
    {"name": "Bohodir Ibraimov",      "role": "Supply Manager",               "photo": "micasa-boho.jpg"},
    {"name": "Murod Shavkatov",       "role": "Senior Architect",              "photo": "micasa-murod.jpg"},
    {"name": "Ramziddin Shorustamov", "role": "Architect",                     "photo": "micasa-ramziddin.jpg"},
    {"name": "Emir-Abdul Sayfutdinov","role": "Architect",                     "photo": "micasa-emir.jpg"},
    {"name": "Jasur",                 "role": "Architect",                     "photo": "micasa-jasur.jpg"},
    {"name": "Omon Kasimov",          "role": "Architect",                     "photo": "micasa-omon.jpg"},
    {"name": "Eldor Nuraliyev",       "role": "Architect",                     "photo": "micasa-e.jpg"},
]

TEAM_PAGE_URL = "https://micasa-design.com/team/index.html"


def find_team_member(full_name: str) -> dict | None:
    """
    Case-insensitive fuzzy match against team member names.
    Returns the member dict or None.
    """
    name_lower = full_name.strip().lower()
    for member in TEAM_MEMBERS:
        member_lower = member["name"].lower()
        # Exact match
        if name_lower == member_lower:
            return member
        # Both words present (handles different word order)
        parts = name_lower.split()
        if all(p in member_lower for p in parts if len(p) > 2):
            return member
    return None
