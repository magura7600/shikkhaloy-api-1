# পাইথনের অফিশিয়াল লাইটওয়েট ইমেজ ব্যবহার করা হচ্ছে
FROM python:3.10-slim

# কাজের জন্য একটি ডিরেক্টরি তৈরি
WORKDIR /app

# গিটহাব থেকে requirements.txt সার্ভারে কপি করা
COPY requirements.txt .

# প্রয়োজনীয় সব প্যাকেজ ইনস্টল করা
RUN pip install --no-cache-dir -r requirements.txt

# গিটহাবের বাকি সব কোড (main.py) সার্ভারে কপি করা
COPY . .

# Hugging Face-এর নিয়ম অনুযায়ী পোর্ট 7860 ওপেন রাখা
EXPOSE 7860

# Gunicorn দিয়ে ফ্লাস্ক সার্ভারটি চালু করা
CMD ["gunicorn", "-b", "0.0.0.0:7860", "main:app"]
