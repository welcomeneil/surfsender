from cgitb import html
import ftplib
import wave
import requests
from base64 import urlsafe_b64decode
from urllib import response
from bs4 import BeautifulSoup

# 1. Choose a web framework: You need to choose a web framework that suits your project requirements. 
# Some of the popular web frameworks in Python are Flask, Django, Pyramid, and Bottle.

# 2. Refactor your code: You need to refactor your code to make it compatible with the chosen web framework. 
# You need to replace the input/output functions with HTTP requests and responses.

# 3. Create routes: You need to create routes for your web application. A route maps
# a URL to a specific function in your code.

# 4. Create templates: You need to create HTML templates for your web 
# pages. You can use a templating engine like Jinja2 to create dynamic templates.

# 5. Set up a database: If your command line script uses a database, you need to set up a database 
# for your web application. You can use a database ORM like SQLAlchemy to interact with the database.

# 6. Deploy your web application: You need to deploy your web application to a web server. 
# You can use a cloud platform like AWS, Azure, or Google Cloud Platform, or a web hosting provider like Heroku or DigitalOcean.

class SurfDailyBest:
    def __init__(self, date, time, ranking, wave_height) -> None:
        self.date = date
        self.time = time
        self.ranking = ranking
        self.wave_height = wave_height
    
    def __str__(self) -> str:
        string_representation = "On " + str(self.date) + "," + " the waves will be " + str(self.ranking) + " stars." + " The best time to surf will be at " + str(self.time) + " with a wave height of " + str(self.wave_height) + "."
        return string_representation

def html_retriever(url):
    page_content = requests.get(url).content
    soup_obj = BeautifulSoup(page_content, 'html.parser')
    return soup_obj

def extract_all_surf_data(soup_obj):
    wave_heights = get_wave_heights_at_times(soup_obj)
    wave_ranks = get_rankings_at_times(soup_obj)
    return create_surf_daily_bests_for_week(wave_heights, wave_ranks)


#Returns a list of SurfDailyBest objects with each daily best wave report and when to go.
def create_surf_daily_bests_for_week(filtered_wave_heights, filtered_star_ranks):
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    time_stamps = ['6am', '9am', '12pm', '3pm', '6pm']
    weekly_daily_bests = []

    #
    for date_index, rankings in enumerate(filtered_star_ranks):
        best_rankings = [index for index, height in enumerate(rankings) if height == max(rankings)]
        if (1 in best_rankings):
            weekly_daily_bests.append(SurfDailyBest(days_of_the_week[date_index], '9am', max(rankings), filtered_wave_heights[date_index][1]))
        else:
            weekly_daily_bests.append(SurfDailyBest(days_of_the_week[date_index], time_stamps[best_rankings[-1]], max(rankings), filtered_wave_heights[date_index][best_rankings[-1]]))

    return weekly_daily_bests

'''Returns a list of lists.
Each nested list represents a day of the week and contains five string values stating the expected wave height at a given timestamp.
Index 0 of the nested list represents the wave height at 6am, and each consecutive index represents a timestamp 3 hours ahead.
This means that index 1 represents the wave height at 9am, index 2 represents the wave height at 12pm, and so forth until 9pm.'''
def get_wave_heights_at_times(soup_obj):
    unfiltered_wave_heights_tags = soup_obj.find_all('span', class_='h3 font-sans-serif heavy nomargin text-white')
    
    #Populates a new list with the string values of each wave height (i.e '2-4ft').
    #The list will contain 56 values with every 8th element representing a day's surf report.
    #Why every 8th element?
    #This is because each day has 8 timestamps with expected wave heights from 12am - 9pm.
    unfiltered_wave_heights = []
    for i in unfiltered_wave_heights_tags:
        unfiltered_wave_heights.append(i.get_text())
    
    #Sifts through the unfiltered_wave_heights list and only retrieves the timestamps for 6am - 9pm.
    #Indices 0-1 contain the timestamps for 12am and 3am respectively. These times will never be used, so they are skipped over.
    #These timestamps are put into 7 nested lists, each list representing a day of the week.
    filtered_wave_heights = []
    for i in range(2, 56, 8):
        filtered_wave_heights.append(unfiltered_wave_heights[i:i+5])

    return filtered_wave_heights
    

'''Returns a list of lists.
Each nested list represents a day of the week and contains five, 'star rating', integer values representing the quality of the waves at a given time stamp out of 5.
Index 0 of the nested list represents the star rating at 6am, and each consecutive index represents a star rating 3 hours ahead.
This means that index 1 represents the star rating at 9am, index 2 represents the star rating at 12pm, and so forth until 9pm.'''
def get_rankings_at_times(soup_obj):
    star_ranking_tags = soup_obj.find_all('ul', class_='rating clearfix')

    unfiltered_star_rankings = [len(star_ranking_tags[i].find_all('li', class_='active')) for i in range(len(star_ranking_tags))]

    filtered_star_rankings = []
    for i in range(2, 56, 8):
        filtered_star_rankings.append(unfiltered_star_rankings[i:i+5])

    return filtered_star_rankings


'''Returns a list of lists.
Each nested list represents a day of the week and contains five tuple values stating the expected wave height at a given timestamp.
The first value of a tuple contains the wave height's lower bound and the second value represents the upper bound.
Index 0 of the nested list represents the wave height at 6am, and each consecutive index represents a timestamp 3 hours ahead.
This means that index 1 represents the wave height at 9am, index 2 represents the wave height at 12pm, and so forth until 9pm.'''
def get_wave_heights_at_times_as_tuples(soup_obj):
    unfiltered_wave_heights_tags = soup_obj.find_all('span', class_='h3 font-sans-serif heavy nomargin text-white')
    
    unfiltered_wave_heights = []
    for i in unfiltered_wave_heights_tags:
        split_numbers = i.get_text().split('-')
        split_numbers[-1] = split_numbers[-1][:-2]
        unfiltered_wave_heights.append(tuple(split_numbers))
    
    filtered_wave_heights = []
    for i in range(2, 56, 8):
        filtered_wave_heights.append(unfiltered_wave_heights[i:i+5])

    return filtered_wave_heights

# if __name__ == "__main__":
#     url = 'https://magicseaweed.com/Doheny-State-Beach-Surf-Report/2588/'
#     html = html_retriever(url)
#     print(get_rankings_at_times(html))