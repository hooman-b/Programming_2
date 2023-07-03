from crawler import Crawler



if __name__ == '__main__':
    crawler_obj = Crawler(url = "https://sport050.nl/sportaanbieders/alle-aanbieders/")
    z = crawler_obj.crawl_site() 
    for x in range(5):
        print (str(next(z)))
    #Result: five lines of data