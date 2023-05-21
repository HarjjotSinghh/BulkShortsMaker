import asyncio
import os
import json
import random
from moviepy.editor import VideoFileClip, TextClip, AudioFileClip, CompositeVideoClip
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


async def make_short(title : str, content: str, social_media_handle: str):
    """
    Makes the short and saves it locally.

    Args:
        title (str): The title of the Shorts/Reel
        content (str): The content of the Shorts/Reel
        social_media_handle (str): The social media handle of the account

    Returns:
        path (str): Path of the Short/Reel generated
    """
    
    video = VideoFileClip(await get_stock_video()).resize(height=1280, width=720)
    video = video.without_audio()
    video_duration = 1
    video = video.subclip(0, video_duration)
    audio = AudioFileClip("./background_audio.mp3")
    video = video.set_audio(audio)
    video.set_duration(video_duration)
    video.resize(height=1280, width=720)
    # print(video.size)
    video_width, video_hieght = video.size
    margin = 100
    
    heading_text = \
                TextClip(f"Did You Know?",
                            method="caption",
                            size = (video_width, video_hieght),
                            fontsize=85, 
                            font="./fonts/Geomatrix Bold.ttf", 
                            color="white", 
                            stroke_color="black", 
                            stroke_width=2,
                            align="North"
                        ).set_position(("center", 350))
    heading_text.set_duration(video_duration)
    
    main_text = \
                TextClip(f"The concept of time, although universally experienced, can be subjective and varies across different cultures, influenced by social, historical, and geographical factors.",
                            method="caption",
                            size = (video_width, video_hieght),
                            fontsize=40,
                            font="./fonts/Geomatrix Medium.ttf",
                            color="white",
                            stroke_color="black",
                            stroke_width=1,
                            align="center"
                        )
    main_text.set_duration(video_duration)

    social_media_hande_text = \
                TextClip(f"Follow for more\n@factfinityy",
                            method="caption",
                            size = (video_width, video_hieght),
                            fontsize=30,
                            font="./fonts/Geomatrix Medium.ttf", 
                            color="white", 
                            stroke_color="black", 
                            stroke_width=1,
                            align="South",
                        )\
                .set_position(("center", -350))
    social_media_hande_text.set_duration(video_duration)

    video_with_text = CompositeVideoClip([video,
                                          heading_text,
                                          main_text,
                                          social_media_hande_text
                                        ])
    video_with_text = video_with_text.set_duration(video_duration) \
                                     .set_audio(audio) \
                                     .resize(height=1280, width=720)

    
    video_with_text.write_videofile("shorts_video.mp4", codec="libx264", audio=True, bitrate='20000k')
    
    shorts_vid = ""
    return shorts_vid


if __name__ == "__main__":
    asyncio.run(make_short())
    
