import os
import re
import json
import subprocess
import requests

IMAGES_DIR = "images"
OUTPUT_VIDEO = "output_video.mp4"
AUDIO_FILE = "output_audio.mp3"
SCRIPT_FILE = "output_script.txt"


def get_audio_duration(audio_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", audio_path],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def split_into_scenes(narration, target_scenes=8):
    # Split narration into sentences, then group into `target_scenes` chunks
    sentences = re.split(r'(?<=[।.!?])\s+', narration.strip())
    sentences = [s for s in sentences if s.strip()]
    if not sentences:
        return [narration]

    chunk_size = max(1, len(sentences) // target_scenes)
    scenes = []
    for i in range(0, len(sentences), chunk_size):
        scenes.append(" ".join(sentences[i:i + chunk_size]))
    return scenes


def generate_image_prompt(scene_text, topic):
    # Keep prompt short and visual, English works best for image models
    return f"cinematic dark moody photo, mystery horror atmosphere, {topic}, related to: {scene_text[:120]}, highly detailed, dramatic lighting"


def download_image(prompt, output_path):
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1024&height=1820&nologo=true"
    r = requests.get(url, timeout=60)
    if r.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(r.content)
        return True
    return False


def build_video(image_paths, scene_duration, audio_path, output_path):
    list_file = "images_list.txt"
    with open(list_file, "w") as f:
        for img in image_paths:
            f.write(f"file '{img}'\n")
            f.write(f"duration {scene_duration}\n")
        # repeat last image (ffmpeg concat quirk: last entry needs no duration after it, so repeat it)
        f.write(f"file '{image_paths[-1]}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", list_file,
        "-i", audio_path,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest",
        output_path
    ], check=True)


if __name__ == "__main__":
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        script_text = f.read()

    lines = script_text.split("\n", 2)
    topic = lines[0].replace("TOPIC:", "").strip() if lines else "mystery"
    narration = lines[2] if len(lines) > 2 else script_text
    narration = re.sub(r"\[.*?\]", "", narration)
    narration = re.sub(r"\n{2,}", "\n", narration).strip()

    os.makedirs(IMAGES_DIR, exist_ok=True)

    scenes = split_into_scenes(narration, target_scenes=8)
    print(f"Split into {len(scenes)} scenes")

    image_paths = []
    for i, scene in enumerate(scenes):
        prompt = generate_image_prompt(scene, topic)
        img_path = os.path.join(IMAGES_DIR, f"scene_{i}.jpg")
        print(f"Generating image {i+1}/{len(scenes)}...")
        success = download_image(prompt, img_path)
        if success:
            image_paths.append(img_path)
        else:
            print(f"Failed to generate image {i}, skipping")

    if not image_paths:
        raise RuntimeError("No images generated, cannot build video")

    audio_duration = get_audio_duration(AUDIO_FILE)
    scene_duration = audio_duration / len(image_paths)
    print(f"Audio duration: {audio_duration:.1f}s, scene duration: {scene_duration:.1f}s each")

    build_video(image_paths, scene_duration, AUDIO_FILE, OUTPUT_VIDEO)
    print("Video generated: output_video.mp4")
