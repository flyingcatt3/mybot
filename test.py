import time,traceback
from facebook_scraper import get_posts
def scraper(sort,target):
    s=[post[sort] for post in get_posts(target, pages=1)][-1]
    print(s)
#while 1:
    #scraper('time','LearningEnglishAmericanWay')
    #scraper('text','LearningEnglishAmericanWay')
try:
    a=1/0
except:
    print(':x:**[ERROR]**\n'+traceback.format_exc())