import schedule

import musinsa_crawler

schedule.every(24).hours.do(exec("musinsa_crawler.py"))