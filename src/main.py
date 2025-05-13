import sys
from pathlib import Path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))
from src.utils.load_city_code import load_city_code
from src.crawler.boss import BossCrawler
from src.cleaner.clean import process_boss_data

if __name__ == "__main__":
    city_dict = load_city_code()
    crawler = BossCrawler()
    for code,name in city_dict.items():
        crawler.crawl_java_jobs(
            max_pages = 30,
            city_code = code
        )
    process_boss_data()