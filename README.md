# ai-influencer-toolkit

Experiments with AI-influencer content: finding what's performing this week, then using it for the motion component with custom character sheet with Genjutsu. 

## Scripts

| Script | What it does |
|---|---|
| `scrape_viral.py` | Pulls the past week's top AI-influencer posts from TikTok and Instagram via Apify, based on provided keyword (keyword search for TikTok sorted by most liked, hashtags for Instagram). Outputs a normalised JSON file with views, likes and comments. |
| `download_videos.py` | Downloads a reference video from a post URL (yt-dlp). This is what is used for motion content - after identifying which to use from the scraper |
| `genjutsu_motion_transfer.py` | Uses Higgsfield's Genjutsu model to replace the asset in a reference video with my own character sheet, keeping the original motion, camera and timing. Saves the output locally. |

## Setup

```bash
pip install apify-client higgsfield-client yt-dlp python-dotenv requests
cp .env.example .env    # then fill in HF_KEY and APIFY_KEY
python scrape_viral.py
```

## Usage note

Only use reference videos you have the rights to, and follow each platform's terms.
