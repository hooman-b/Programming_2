from crawler import Crawler



if __name__ == '__main__':
    crawler_obj = Crawler(url = "https://sport050.nl/sportaanbieders/alle-aanbieders/")

    iteration = zip(crawler_obj, range(5))


    for x, _ in iteration:
        print(x)
    #Result: five lines of data