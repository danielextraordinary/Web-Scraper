#Importing required libraries
import pandas as pd
import config
from urllib import parse
import requests
import re
from bs4 import BeautifulSoup as bs

#Authentication
api_key = config.api_key



class Yelp:
    def __init__(self, search, location):
        self.search = search
        self.location = location
        self.url = config.api_url


#This function calls the API from Yelp and returns a list of dictionaries that contain business details
    def get_page(self, search, location):
        header = {"Authorization": "Bearer "+ api_key}
        param = {
            
            "term": f"{search}",
            "location": f"{location}"
        }

        try:
                
            response = requests.get(self.url, headers=header, params=param)
            if response.status_code == 200:
                raw_businesses_list = response.json()["businesses"]
                print(f"The API Call completed with the status code: <{response.status_code}>")
                return raw_businesses_list
                
            else:
                print(f"ERROR!, {self.url} could not finish due to error <{response.status_code}>")
        except requests.exceptions.HTTPError as http_err:
            print(f"The page is not found. {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"The page is not found. {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"The page is not found. {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"The page is not found. {req_err}")
        

#This function takes in a Yelp URL (string) and returns scraped URL of the business
    def url_finder(url):

        response = requests.get(url)

        # if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        for link in soup.find_all("a", href = True):
            if "biz_redir" in link["href"]:
                extracted_link = parse.unquote(link["href"][15:].split("&cachebuster")[0])
                return str(extracted_link)
                break


    def get_businesses(self):
        to_save = []
        raw_list = self.get_page(self.search, self.location)
        for x in range(len(raw_list)):
            to_save.append({"name": raw_list[x]["name"], "location": " ".join(raw_list[x]["location"]["display_address"]), "url":Yelp.url_finder(raw_list[x]["url"]), "phone":raw_list[x]["phone"]})
        
        return to_save
    
    

    def save_csv(self, input):
        
        # header = ["name", "location", "url", "phone"]
        # with open("dataFile.csv", "w") as file:
        #     writer = csv.DictWriter(file, fieldnames = header, lineterminator="\n")
        #     writer.writerows(input)

        # file.to_csv("gfg2.csv", header=headerList, index=False)

        df = pd.DataFrame(input)
        df.to_csv("yelp_businesses.csv", header = True, lineterminator="\n")
        # display modified csv file
        # file2 = pd.read_csv("gfg2.csv")
        # print('\nModified file:')
        # print(file2)

