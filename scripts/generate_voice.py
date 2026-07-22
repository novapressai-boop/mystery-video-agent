import re
import edge_tts
import asyncio

VOICE = "bn-BD-PradeepNeural"
RATE = "-10%"

async def generate_voice(text, output_file="output_audio.mp3"):
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(output_file)

if __name__ == "__main__":
    with open("output_script.txt", "r", encoding="utf-8") as f:
        script_text = f.read()
    lines = script_text.split("\n", 2)
    narration = lines[2] if len(lines) > 2 else script_text
    # [Hook], [পটভূমি] ইত্যাদি label সরিয়ে ফেলা
    narration = re.sub(r"\[.*?\]", "", narration)
    narration = re.sub(r"\n{2,}", "\n\n", narration).strip()
    asyncio.run(generate_voice(narration))
    print("Voice generated!")
