from DrissionPage import ChromiumPage
import json
from pathlib import Path
import time
import random


class BossCrawler:
    def __init__(self):
        self.page = ChromiumPage(9222)
        self.page.set.window.max()
        self.page.set.user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        self.json_file = Path('BossData_raw.json')
        self._init_json_file()

    def _init_json_file(self):
        if not self.json_file.exists():
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
                
    def _random_scroll(self):
            scroll_times = random.randint(2, 5)
            for _ in range(scroll_times):
                self.page.scroll.down(random.randint(300, 800))
                time.sleep(random.uniform(0.5, 1.5))
            
    def crawl_java_jobs(self, max_pages=5, city_code='101010100'):
        self.page.listen.start('zhipin.com/wapi/zpgeek/search/joblist.json?')
        url = f'https://www.zhipin.com/web/geek/job?query=java&city={city_code}'
        self.page.get(url)
        current_city_jobs = []  
        for page_num in range(1, max_pages + 1):
            print(f"\n开始处理第 {page_num} 页")
            time.sleep(random.uniform(2, 5))
            self._random_scroll()
            resp = self.page.listen.wait(timeout=3)
            if not resp:
                print("到底了")
                break
            json_data = json.loads(resp.response.body) if isinstance(resp.response.body, str) else resp.response.body
            job_list = json_data.get('zpData', {}).get('jobList', [])
            current_city_jobs.extend(job_list)
            print(f"获取到 {len(job_list)} 条原始数据")
            time.sleep(random.uniform(2, 5))

        self.page.listen.stop()
        self._append_to_json(current_city_jobs)
        print(f"当前城市数据已追加到 {self.json_file}")

    def _append_to_json(self, new_jobs):
        """将新数据追加到JSON文件"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except:
            existing_data = []
        combined_data = existing_data + new_jobs
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)

