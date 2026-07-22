import os
import random
import requests
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])
HEADERS = {"User-Agent": "MysteryVideoAgent/1.0 (contact: example@example.com)"}

REAL_MYSTERIES = [
    "Mary Celeste",
    "Dyatlov Pass incident",
    "Bermuda Triangle",
    "Roanoke Colony",
    "Flannan Isles Lighthouse mystery",
    "Voynich manuscript",
    "Somerton man",
    "Taos hum",
    "Max Headroom broadcast signal intrusion",
    "Amelia Earhart disappearance",
    "Zodiac Killer",
    "Isdal woman",
    "Sodder children disappearance",
    "Lead masks case",
    "Hinterkaifeck murders",
]

def fetch_wikipedia_summary(title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code == 200:
        try:
            return r.json().get("extract", "")
        except Exception:
            return ""
    return ""

def fetch_wikipedia_full(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json",
    }
    r = requests.get(url, params=params, headers=HEADERS, timeout=15)
    try:
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            return page.get("extract", "")[:6000]
    except Exception:
        return ""
    return ""

def generate_script(topic, source_text):
    prompt = f"""
তুমি একজন অভিজ্ঞ horror/mystery YouTube script writer, যে স্বাভাবিক, প্রাণবন্ত ভাষায় গল্প বলে — কোনো বাক্য বা বাক্যাংশ বারবার repeat করে না।

নিচের real তথ্য/উৎস পড়ে, তার ভিত্তিতে বাংলায় একটি ভয়ানক, suspenseful narration script লেখো। শুধু নিজের কল্পনা থেকে না লিখে, নিচের তথ্যের সব গুরুত্বপূর্ণ অংশ ব্যবহার করো।

Topic: {topic}

উৎস তথ্য:
\"\"\"
{source_text}
\"\"\"

Format:
[Hook] - প্রথম ৩০ সেকেন্ড, চমকপ্রদ ও ভয়ানক শুরু
[পটভূমি] - ঘটনার background
[মূল ঘটনা] - বিস্তারিত রহস্যময় ঘটনা, উৎস তথ্যের সব গুরুত্বপূর্ণ detail সহ
[তত্ত্ব ও রহস্য] - বিভিন্ন theory, অতিপ্রাকৃত angle সহ
[উপসংহার] - রহস্যময়, খোলা প্রশ্ন রেখে শেষ করো (একটাই শক্তিশালী বাক্যে শেষ করো)

গুরুত্বপূর্ণ নিয়ম:
- একই বাক্য, বাক্যাংশ বা ধারণা কখনো দুইবার বলবে না
- উৎস তথ্যে যত বেশি detail আছে, script তত বড় হবে; কম থাকলে ছোট হবে — জোর করে লম্বা করবে না
- সাধারণ কথ্য, স্বাভাবিক বাংলায় লিখবে, অতিরিক্ত formal ভাষা এড়িয়ে চলবে
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    topic = random.choice(REAL_MYSTERIES)
    source_text = fetch_wikipedia_full(topic)
    if not source_text:
        source_text = fetch_wikipedia_summary(topic)
    if not source_text:
        source_text = f"({topic} সম্পর্কে বিস্তারিত তথ্য পাওয়া যায়নি, সাধারণ জ্ঞান থেকে লেখো)"
    script = generate_script(topic, source_text)
    with open("output_script.txt", "w", encoding="utf-8") as f:
        f.write(f"TOPIC: {topic}\n\n{script}")
    print(f"Script generated for topic: {topic}")
