COMMON_NEWS_WORDS = {
    "news", "daily", "today", "evening", "morning",
    "bulletin", "samachar", "sandhya", "dainik",
    "weekly", "national", "bharat", "india"
}

def extract_anchors(title):
    words = title.split()
    return {
        w for w in words
        if w not in COMMON_NEWS_WORDS and len(w) > 3
    }

def has_anchor_overlap(title, existing_title):
    return bool(
        extract_anchors(title)
        & extract_anchors(existing_title)
    )
