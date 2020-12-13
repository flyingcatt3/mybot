import time
from facebook_scraper import get_posts
def scraper(sort,target):
    s=[post[sort] for post in get_posts(target, pages=1)][-1]
    s='\n'.join(s)
    print(s)
scraper('images','gainwind')