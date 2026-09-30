import argparse

import yt_dlp

OUTPUT_FOLDER = 'assets'


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Download a video from a URL')
    parser.add_argument('url')
    parser.add_argument('--name', default='%(id)s', help='Output file name without extension (default: post ID)')
    args = parser.parse_args()
    return args


def main() -> None:
    args = parse_arguments()

    options = {'outtmpl': f'{OUTPUT_FOLDER}/{args.name}.%(ext)s'}
    with yt_dlp.YoutubeDL(options) as downloader:
        downloader.download([args.url])


if __name__ == '__main__':
    main()
