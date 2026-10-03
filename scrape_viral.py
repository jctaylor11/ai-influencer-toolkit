import json
from datetime import datetime, timedelta, timezone

from apify_client import ApifyClient

HASHTAGS = ["aiinfluencer", "aiinfluencers", "virtualinfluencer", "aiavatar"]
RESULTS_PER_HASHTAG = 100
WINDOW_DAYS = 7
REF_VIDEOS_DIR = "ref_videos"
RAW_PATH = f"{REF_VIDEOS_DIR}/raw_posts.json"


def load_apify_token() -> str:
    with open(".env") as env_file:
        for line in env_file:
            key, _, value = line.partition("=")
            if key.strip() == "APIFY_KEY":
                return value.strip().strip('"')
    raise RuntimeError("APIFY_KEY not found in .env")


def scrape_tiktok(client: ApifyClient, cutoff: datetime) -> list[dict]:
    run_input = {
        "hashtags": HASHTAGS,
        "resultsPerPage": RESULTS_PER_HASHTAG,
        "oldestPostDateUnified": cutoff.strftime("%Y-%m-%d"),
        "shouldDownloadVideos": False,
    }
    run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
    items = client.dataset(run.default_dataset_id).list_items().items

    posts = []
    for item in items:
        created = datetime.fromtimestamp(item["createTime"], tz=timezone.utc)
        if created < cutoff:
            continue
        posts.append({
            "platform": "tiktok",
            "creator": item["authorMeta"]["name"],
            "views": item.get("playCount", 0),
            "likes": item.get("diggCount", 0),
            "comments": item.get("commentCount", 0),
            "url": item["webVideoUrl"],
            "posted_at": created.isoformat(),
        })
    return posts


def scrape_instagram(client: ApifyClient, cutoff: datetime) -> list[dict]:
    run_input = {
        "hashtags": HASHTAGS,
        "resultsType": "reels",
        "resultsLimit": RESULTS_PER_HASHTAG,
    }
    run = client.actor("apify/instagram-hashtag-scraper").call(run_input=run_input)
    items = client.dataset(run.default_dataset_id).list_items().items

    posts = []
    for item in items:
        views = item.get("videoPlayCount") or item.get("videoViewCount") or 0
        if item.get("type") != "Video" or views == 0:
            continue
        created = datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
        if created < cutoff:
            continue
        posts.append({
            "platform": "instagram",
            "creator": item["ownerUsername"],
            "views": views,
            "likes": max(item.get("likesCount", 0), 0),  # -1 when likes are hidden
            "comments": item.get("commentsCount", 0),
            "url": item["url"],
            "posted_at": created.isoformat(),
        })
    return posts


def main() -> None:
    client = ApifyClient(load_apify_token())
    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)

    tiktok_posts = scrape_tiktok(client, cutoff)
    print(f"tiktok: {len(tiktok_posts)} posts in window")
    instagram_posts = scrape_instagram(client, cutoff)
    print(f"instagram: {len(instagram_posts)} posts in window")

    with open(RAW_PATH, "w") as raw_file:
        json.dump(tiktok_posts + instagram_posts, raw_file)
    print(f"Saved to {RAW_PATH}")


if __name__ == "__main__":
    main()
