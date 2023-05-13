import time


from yelp import Yelp

start_time = time.time()

search = "Web Design"
location = "United Kingdom"



#url = "https://api.yelp.com/v3/businesses/search"

if "__main__" == __name__:
    start_time = time.time()
    print("-----------setting up...-----------")
    business = Yelp(search, location)
    business.get_page(search, location)
    output = business.get_businesses()
    
    business.save_csv(output)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"completed in {elapsed_time} seconds")