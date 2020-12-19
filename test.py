from facebook_scraper import get_posts
def scraper(sort,target):
    s=[post[sort] for post in get_posts(target, pages=1)][-1]
    
scraper('post_url','gainwind')
scraper('text','gainwind')