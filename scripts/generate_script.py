import os
import random
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

TOPICS = [
    # Real unsolved mysteries
    "The Mary Celeste Mystery",
    "The Dyatlov Pass Incident",
    "The Bermuda Triangle Disappearances",
    "The Roanoke Colony Vanishing",
    "The Flannan Isles Lighthouse Mystery",
    "The Voynich Manuscript",
    "The Somerton Man Mystery",
    "The Taos Hum",
    "The Max Headroom Broadcast Incident",
    "The Disappearance of Amelia Earhart",
    "The Zodiac Killer's Unsolved Ciphers",
    "The Isdal Woman Mystery",
    "The Sodder Children Disappearance",
    "The Lead Masks Case",
    "The Hinterkaifeck Murders",

    # Classic public-domain mystery/horror fiction
    "The Murders in the Rue Morgue (Edgar Allan Poe)",
    "The Tell-Tale Heart (Edgar Allan Poe)",
    "The Fall of the House of Usher (Edgar Allan Poe)",
    "The Red-Headed League (Arthur Conan Doyle)",
    "The Speckled Band (Arthur Conan Doyle)",
    "The Hound of the Baskervilles (Arthur Conan Doyle)",
    "A Jury of Her Peers (Susan Glaspell)",
    "The Monkey's Paw (W.W. Jacobs)",
    "The Turn of the Screw (Henry James)",
    "The Yellow Wallpaper (Charlotte Perkins Gilman)",
    "Dracula's Guest (Bram Stoker)",
    "The Legend of Sleepy Hollow (Washington Irving)",
]

def generate_script(topic):
    prompt = f"""
তুমি একজন horror/mystery YouTube script writer।
নিচের topic নিয়ে বাংলায় একটি ভয়ানক, suspenseful narration script লেখো।
Topic: {topic}

Format:
[Hook] - প্রথম ৩০ সেকেন্ড, চমকপ্রদ ও ভয়ানক শুরু
[পটভূমি] - ঘটনার background
[মূল ঘটনা] - বিস্তারিত রহস্যময় ঘটনা
[তত্ত্ব ও রহস্য] - বিভিন্ন theory, অতিপ্রাকৃত angle সহ
[উপসংহার] - রহস্যময়, খোলা প্রশ্ন রেখে শেষ করো

Tone: গম্ভীর, ধীর, suspenseful। Topic-এ যতটা তথ্য/রহস্য আছে তার উপর ভিত্তি করে script-এর length নিজে থেকে ঠিক করো — সাধারণত ৪-১০ মিনিট narration (৬০০-১৫০০ শব্দ)-এর মধ্যে, তবে টেনে লম্বা করার দরকার নেই যদি topic-এ যথেষ্ট material না থাকে।
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    topic = random.choice(TOPICS)
    script = generate_script(topic)
    with open("output_script.txt", "w", encoding="utf-8") as f:
        f.write(f"TOPIC: {topic}\n\n{script}")
    print(f"Script generated for topic: {topic}")
