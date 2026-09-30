import higgsfield_client
import requests
from dotenv import load_dotenv
from higgsfield_client.exceptions import HiggsfieldClientError

VIDEO_PATH = 'assets/test_1.mp4'
CHAR_IMAGE_PATH = 'assets/char_sheet_2.png'
BACKGROUND_IMAGE_PATH = 'assets/background.png'
PROMPT = 'Replace the person in the video with the character in the first image. Use the location in the second image as a reference for the background. Keep the original motion, camera and timing. Make sure the final character is fully clothed as in the character image to ensure it is safe for work.'
RESOLUTION = '480p'  # Cheap while testing; 720p/1080p for final
OUTPUT_PATH = 'results/output.mp4'

last_status_name = ''


def print_request_id(request_id: str) -> None:
    print(f'Submitted. Request ID: {request_id}')  # Handy for finding the job in the console


def print_status_update(status: higgsfield_client.Status) -> None:
    global last_status_name
    status_name = type(status).__name__
    if status_name == last_status_name:  # The SDK polls twice a second; only print changes
        return
    last_status_name = status_name
    print(f'Status: {status_name}')


def main() -> None:
    load_dotenv()  # Puts HF_KEY from .env into the environment for the client

    print('Uploading video...')
    video_url = higgsfield_client.upload_file(VIDEO_PATH)
    print('Uploading character image...')
    char_image_url = higgsfield_client.upload_file(CHAR_IMAGE_PATH)
    print('Uploading background image...')
    background_image_url = higgsfield_client.upload_file(BACKGROUND_IMAGE_PATH)

    arguments = {
        'prompt': PROMPT,
        'video_url': video_url,
        'image_urls': [char_image_url, background_image_url],
        'resolution': RESOLUTION,
    }
    try:
        result = higgsfield_client.subscribe(
            'higgsfield/genjutsu/motion-transfer/v1.0',
            arguments=arguments,
            on_enqueue=print_request_id,
            on_queue_update=print_status_update,
        )
    except HiggsfieldClientError as error:
        print(f'Higgsfield rejected the request: {error}')  # e.g. bad video/image, no credits
        raise

    if 'video' not in result:  # subscribe() doesn't raise if the job failed or was flagged NSFW
        print(f'Generation did not produce a video. Full result: {result}')
        raise RuntimeError('No video in result')

    video = result['video']
    output_url = video['url']

    print('Downloading video...')
    response = requests.get(output_url)  # Output URLs expire after ~7 days, so save locally
    response.raise_for_status()
    with open(OUTPUT_PATH, 'wb') as output_file:
        output_file.write(response.content)

    print(f'Saved to {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
