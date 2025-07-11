# پروژه ایجنت مسابقه دیوار

## معرفی پروژه
این پروژه برای شرکت در مسابقه Capture the Flag (CTF) دیوار طراحی شده است. هدف، ساخت یک ایجنت هوش مصنوعی است که بتواند با دریافت سوالات مختلف، پرچم (Flag) مربوط به هر ماموریت را پیدا کند و بازگرداند. ایجنت باید با استفاده از مدل GPT-4.1-mini و API متیس، به سوالات پاسخ دهد و وظایف مختلفی مانند پردازش داده‌های HTML، PDF، JSON و ... را انجام دهد.

## ساختار فایل‌ها
- `solution.py` : پیاده‌سازی اصلی کلاس `DivarContest` و متد `capture_the_flag` برای حل ماموریت‌ها
- `test.py` : نمونه تست برای اجرای ایجنت و بررسی خروجی
- `python_requirements.txt` : لیست وابستگی‌های مورد نیاز پروژه
- `Role.txt` : توضیحات و قوانین مسابقه و راهنمای استفاده از API
- `debug_divar.html` : نمونه داده HTML برای تست برخی ماموریت‌ها
- فایل‌های ZIP (مانند `divar.zip`, `P1.zip`, `P3.zip`, `ح3.zip`) : داده‌های نمونه یا خروجی‌های مورد نیاز
- `Sample.py` : نمونه ساده از ساختار اولیه ایجنت

## نصب و راه‌اندازی
1. **کلون یا دانلود پروژه**
2. نصب وابستگی‌ها:
   ```bash
   pip install -r python_requirements.txt
   ```
3. قرار دادن توکن API متیس (در کد یا به صورت متغیر محیطی)

## نحوه اجرا
برای تست ایجنت می‌توانید فایل `test.py` را اجرا کنید:
```bash
python test.py
```
یا مستقیماً از کلاس `DivarContest` در کد خود استفاده کنید:
```python
from solution import DivarContest
api_token = "توکن_خود_را_اینجا_قرار_دهید"
agent = DivarContest(api_token)
question = "متن سوال یا ماموریت"
result = agent.capture_the_flag(question)
print(result)
```

## ورودی و خروجی
- **ورودی:** رشته سوال (question) به زبان طبیعی یا فرمت ماموریت مسابقه
- **خروجی:** رشته حاوی پرچم (Flag) یا پاسخ مورد انتظار

## مثال اجرا
```python
from solution import DivarContest
api_token = "توکن_خود_را_اینجا_قرار_دهید"
agent = DivarContest(api_token)
question = "call {https://divar-contest.darkube.app/pending-ads/ad-public-931582.json} and fetch the pending ads, review the fetched ads and choose the correct tag for each one. It is guaranteed that only one of the issues exists in the ads."
result = agent.capture_the_flag(question)
print(result)
```

## وابستگی‌ها
محتوای `python_requirements.txt`:
```
requests
beautifulsoup4
PyPDF2
time
random
```

## نکات مهم مسابقه
- فقط از مدل `gpt-4.1-mini` و API متیس استفاده کنید.
- تابع اصلی باید `capture_the_flag` در کلاس `DivarContest` باشد.
- ورودی و خروجی تابع باید رشته (string) باشد.
- مقدار پارامتر `temperature` را ۰.۱ قرار دهید تا خروجی مدل تصادفی نباشد.
- اعتبار API محدود است؛ مصرف توکن را مدیریت کنید.
- برای ارسال به داوری، فقط فایل‌های `solution.py` و `python_requirements.txt` را در یک ZIP قرار دهید.

## راهنمای ارسال برای داوری
- فایل ZIP باید شامل `solution.py` و `python_requirements.txt` باشد.
- از قرار دادن اطلاعات حساس (مانند توکن شخصی) در فایل ارسالی خودداری کنید.
- مستندات و توضیحات بیشتر در فایل `Role.txt` موجود است.

---

**موفق باشید!** 