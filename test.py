from facebook_scraper import get_posts
def scraper(sort,target):
    print([post[sort] for post in get_posts(target, pages=1)][-1])
#scraper('text','LearningEnglishAmericanWay')
#scraper('post_url','LearningEnglishAmericanWay')
#scraper('time','LearningEnglishAmericanWay')
#scraper('text','gainwind')
#scraper('post_url','gainwind')
#scraper('time','gainwind')