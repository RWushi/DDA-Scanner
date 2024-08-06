import re, json

def load_keywords(filename="Keywords.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

keywords = load_keywords()

def message_filter(message):
    def contains_any(group):
        return any(re.search(rf'\b{pattern}\b', message, flags=re.IGNORECASE) for pattern in group)

    if contains_any(keywords['minus']):
        return False

    if (contains_any(keywords['1_1']) and contains_any(keywords['2_1'])) or \
            (contains_any(keywords['1_2']) and contains_any(keywords['2_2'])) or \
            (contains_any(keywords['1_3_1']) and contains_any(keywords['1_3_2']) and contains_any(keywords['2_1'])):
        return True

    return False
