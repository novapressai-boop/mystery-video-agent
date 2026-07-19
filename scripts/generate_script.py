import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

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

Tone: গম্ভীর, ধীর, suspenseful। মোট length এমন হবে যাতে ৫+ মিনিট narration হয় (কমপক্ষে ৮০০-১০০০ শব্দ)।
"""
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    topic = "The Mary Celeste Mystery"
    script = generate_script(topic)
    with open("output_script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    print("Script generated and saved!")
