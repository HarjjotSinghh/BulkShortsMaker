import asyncio
import os
import json
import random
from moviepy.editor import VideoFileClip, TextClip, AudioFileClip
import aiohttp


config = json.load(open("./config.json", "r"))


async def get_stock_video():
    """
        Generates and downloads a random 9:16 stock video locally using the Pexels API.
    """
    
    headers = {"Authorization": config["PEXELS_API_KEY"]}
    params = {"query": "sunset",
              "orientation": "portrait", 
              "per_page": 50,
              "size" : "medium"
              }
    video_duration_threshold = 9
       
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.pexels.com/videos/search", headers=headers, params=params) as response:
                data = await response.json()
                videos = data["videos"]
                random_video = random.choice(videos)
                video_url = random_video["video_files"][0]["link"]
                if random_video["duration"] >= video_duration_threshold:
                    async with session.get(video_url) as video_response:
                        with open("background_video.mp4", "wb") as video_file:
                            while True:
                                chunk = await video_response.content.read(1024)
                                if not chunk:
                                    break
                                video_file.write(chunk)
                    break
                else:
                    continue
    return "background_video.mp4"


async def make_short(vid : str, text : str, social_media_hande: str):
    """
    Makes the short and saves it locally.

    Args:
        vid (str): Path of the video file
        text (str): Text to be put in the short
        social_media_handle (str): Social media @ to be put in the short

    Returns:
        str: Path of the Short generated
    """
    
    video = VideoFileClip(await get_stock_video())
    font = "Codec Pro"
    video = video.without_audio()
    video_duration = 9
    video = video.subclip(0, video_duration)
    audio = AudioFileClip("./background_audio.mp3")
    video = video.set_audio(audio)
    heading_text = TextClip("Did You Know?", font=font, color="white", stroke_color="black", stroke_width=1)
    heading_text.set_duration(0)
    main_text = TextClip()
    main_text.set_duration(7)
    social_media_hande_text = TextClip("@factfinityy", font=font, color="white", stroke_color="black", stroke_width=1)
    social_media_hande_text.set_duration(0)
    
    shorts_vid = ""
    return shorts_vid


if __name__ == "__main__":
    asyncio.run(get_stock_video())
    
