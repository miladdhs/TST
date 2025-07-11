import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import ast

class DivarContest:
    def __init__(self, api_token):
        self.api_token = api_token
        self.model = "gpt-4.1-mini"
        self.client = OpenAI(api_key=self.api_token, base_url="https://api.metisai.ir/openai/v1")

    def capture_the_flag(self, question):
        # Task 1: Find and sort laptops by time
        if "Find all the 'لپ‌تاپ'" in question and "divar_sample.html" in question and "ordered from the oldest" in question:
            return str(self._task1_laptops_sorted())
        # Task 2: Find laptops and calculate average price
        if "Calculate the average price" in question and "divar_sample.html" in question:
            return str(self._task2_laptops_avg_price())
        # Task 3: Answer from Divar news
        if "divar.news" in question:
            return str(self._task3_divar_news(question))
        # Task 4: Find fake facts in PDF
        if ".pdf" in question and "fake facts" in question:
            return self._ensure_json_list(self._task4_fake_facts())
        # Task 5: Find owner of fake ads
        if "fake ads" in question and "starting ad is" in question:
            return str(self._task5_fake_ads_owner(question))
        # Task 6: Best root category
        if "identify the best root category" in question:
            return str(self._task6_best_category(question))
        # Task 7: Pending ads tag
        if "pending ads" in question and ".json" in question:
            return self._ensure_json_list(self._task7_pending_ads(question))
        # Task 8: Reported chats tag
        if "reported chats" in question and ".json" in question:
            return self._ensure_json_list(self._task8_reported_chats(question))
        return "Not implemented yet."

    def _task1_laptops_sorted(self):
        url = "https://divar-contest.darkube.app/divar_sample.html"
        resp = requests.get(url, verify=False)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = []
        ad_divs = soup.find_all('div', class_='bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 border border-gray-200')
        for ad in ad_divs:
            title_tag = ad.find('h3')
            if title_tag and 'لپ‌تاپ' in title_tag.text:
                # Find all p tags with class 'text-sm text-gray-500'
                p_tags = ad.find_all('p', class_='text-sm text-gray-500')
                if p_tags:
                    time_text = p_tags[-1].text.strip()
                    minutes = self._parse_time_to_minutes(time_text)
                    items.append((minutes, title_tag.text.strip()))
        # Sort by minutes descending (oldest first)
        items.sort(reverse=True)
        result = ', '.join([title for _, title in items])
        return result

    def _task2_laptops_avg_price(self):
        url = "https://divar-contest.darkube.app/divar_sample.html"
        resp = requests.get(url, verify=False)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        prices = []
        ad_divs = soup.find_all('div', class_='bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 border border-gray-200')
        for ad in ad_divs:
            title_tag = ad.find('h3')
            if title_tag and 'لپ‌تاپ' in title_tag.text:
                price_tag = ad.find('p', class_='text-gray-600 mb-2 font-bold text-lg')
                if price_tag:
                    price_text = price_tag.text.strip().replace('قیمت:', '').replace('تومان', '').replace(',', '').replace(' ', '')
                    price = self._parse_price(price_text)
                    if price:
                        prices.append(price)
        if prices:
            avg = int(sum(prices) / len(prices))
            return str(avg)
        return "0"

    def _parse_time_to_minutes(self, time_text):
        # Examples: '۳۰ دقیقه پیش', '۲ ساعت پیش', '۱ روز پیش'
        num_map = {'۰':0,'۱':1,'۲':2,'۳':3,'۴':4,'۵':5,'۶':6,'۷':7,'۸':8,'۹':9}
        def fa2en(s):
            return int(''.join(str(num_map.get(ch, ch)) for ch in s if ch.isdigit() or ch in num_map))
        if 'دقیقه' in time_text:
            n = fa2en(time_text)
            return n
        if 'ساعت' in time_text:
            n = fa2en(time_text)
            return n * 60
        if 'روز' in time_text:
            n = fa2en(time_text)
            return n * 1440
        return 0

    def _parse_price(self, price_text):
        # Example: '۴۳٬۷۰۰٬۰۰۰ تومان'
        price_text = re.sub(r'[^۰-۹0-9]', '', price_text)
        if not price_text:
            return None
        num_map = {'۰':0,'۱':1,'۲':2,'۳':3,'۴':4,'۵':5,'۶':6,'۷':7,'۸':8,'۹':9}
        en_price = int(''.join(str(num_map.get(ch, ch)) for ch in price_text))
        return en_price

    def _task3_divar_news(self, question):
        # Use OpenAI to answer based on divar.news
        prompt = f"You are an expert on Divar's history. Use only information from https://divar.news/. {question}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def _task4_fake_facts(self):
        import io
        import requests
        import PyPDF2
        url = "https://divar-contest.darkube.app/facts-va32bma-public.pdf"
        resp = requests.get(url, verify=False)
        pdf = PyPDF2.PdfReader(io.BytesIO(resp.content))
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        # Use OpenAI to find fake facts
        prompt = f"Find the fake facts in the following text (return as a Python list):\n{text}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def _task5_fake_ads_owner(self, question):
        # Use OpenAI to reason about the owner
        prompt = f"{question}\nFind the owner of all fake ads. Return only the owner's name or the flag."
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def _task6_best_category(self, question):
        # Extract title
        import re
        m = re.search(r'title is \{(.+?)\}', question)
        title = m.group(1) if m else question
        # Explicit root categories
        root_categories = [
            "املاک",
            "وسایل نقلیه",
            "کالای دیجیتال",
            "خانه و آشپزخانه",
            "خدمات",
            "وسایل شخصی",
            "سرگرمی و فراغت",
            "اجتماعی",
            "استخدام و کاریابی"
        ]
        prompt = (
            f"Given the following root categories of Divar: {', '.join(root_categories)}. "
            f"What is the best root category for this ad title?\nTitle: {title}\n"
            f"Return ONLY one of the above root categories, nothing else."
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def _task7_pending_ads(self, question):
        import re
        import requests
        m = re.search(r'call \{(.+?\.json)\}', question)
        url = m.group(1) if m else None
        if not url:
            return "[]"
        resp = requests.get(url, verify=False)
        ads = resp.json()
        allowed_tags = ["OK", "IRRELEVANT_PICTURE", "IRRELEVANT_DESCRIPTION", "IRRELEVANT_CATEGORY"]
        prompt = (
            f"Review these pending ads and choose the correct tag for each one. "
            f"Allowed tags: {allowed_tags}. "
            f"Return as a Python list, using ONLY these tags and nothing else.\n{ads}"
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def _task8_reported_chats(self, question):
        import re
        import requests
        m = re.search(r'call \{(.+?\.json)\}', question)
        url = m.group(1) if m else None
        if not url:
            return "[]"
        resp = requests.get(url, verify=False)
        chats = resp.json()
        # Use OpenAI to tag
        prompt = f"Review these reported chats and choose the correct tag for each one. Return as a Python list.\n{chats}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def _ensure_json_list(self, output):
        try:
            # Try to parse as Python list
            if isinstance(output, list):
                return json.dumps(output, ensure_ascii=False)
            # Try to eval if string
            parsed = ast.literal_eval(output)
            if isinstance(parsed, list):
                return json.dumps(parsed, ensure_ascii=False)
        except Exception:
            pass
        # Fallback: return as string
        return str(output)
