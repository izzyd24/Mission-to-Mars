# update to integreate scraping code so Flask can use it
# 10.5.2 asks to refactor the scrapping.py to include functions and add try/error 

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# addition from 10.5.3
# function to initialize browser, create data dict, end webdriver
# return scraped data
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # tells us that news title, news para variables = marsnews function 
    # lets us pull the data
    news_title, news_paragraph = mars_news(browser)
    # adding from challenge d2
    hemisphere_image_urls=hemisphere(browser)

    # Run all scraping functions and store results in a dictionary
    # this dict does: 
    # 1. runs all functions 
    # 2. stores results
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        # add from challenge deliverable #2 
        # list of dicts with URL string + title of each hemisphere
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }

    # function is complete
    # closes broswer/stopwebdriver
    browser.quit()
     # returns data dict. 
    return data

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


### NEWS AND TITLE PARA 
# add the argument browser, to tell python to use browser var from above
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    # most common error in scraping is when webpage format has changed 
    # ... no longer matches our HTML called elements
    try:
        # tell python to look for these elements, and if error...
        # then cont. to run the remainder of code
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
    # if attribute error return nothing
        return None, None
    # do not print, but simply end the function by returning the newstitle and newsp
    return news_title, news_p
   
  
### JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

### Mars Facts
def mars_facts():
    # Add try/except for error handling
    # baseexception = when built ins are encountered, won't handle user-defined exceptions
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        # removed the print statements, and return none if base exception
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# final block tells flask that our script is complete
# prints the results of scraping to terminal 
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

# add 10.5.3 code--- update data stored in mongo each time its ran 
# script to establish link between scraped data and our database via mongodb
