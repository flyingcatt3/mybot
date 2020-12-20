
from facebook_scraper import get_posts
def scraper(sort,target):
    return [post[sort] for post in get_posts(target, pages=1)][-1]

print(scraper('images','LearningEnglishAmericanWay'))

