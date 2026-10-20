# AI Influencer Toolkit

Experimentation with AI-influencer content using Higgsfield.

## Scripts

- `scrape_viral.py`: Scrapes TikTok and Instagram for the past week's top videos based on provided keywords. Outputs a JSON file with video metrics and URL. 
- `download_videos.py`: Downloads an Instagram video to `assets/` given a URL.
- `genjutsu_motion_transfer.py`: Replaces a video's subject with a given character sheet, using Higgsfield's Genjutsu model. 

## Usage

```bash
pip install -r requirements.txt
cp .env.example .env    # fill in HF_KEY and APIFY_KEY
python scrape_viral.py
```
