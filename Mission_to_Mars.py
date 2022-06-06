#!/usr/bin/env python
# coding: utf-8

# In[19]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
# this helps us search for elements for a div tag and attribute list text
# tells browswer to wait before searching for componenets 
# delays help if webpage is image heavy
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# set up the html parser
html = browser.html
news_soup = soup(html, 'html.parser')
# slide elem is the parent element, to look for the div tag
# we will use this as reference to filter search results
# div.list text pinpoints <div/> tag on list text class
slide_elem = news_soup.select_one('div.list_text')

# select1_one helps first matching element return be <li/>


# In[6]:


# want to collect recent news article with summary para
# use the html attribute of: 
# class = "content_title"
# adjusted with .get_text to show only text
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[9]:


# now take the previous code and add the paragraph summary
news_para = slide_elem.find('div', class_='article_teaser_body').get_text()
news_para


# ### Featured Images

# In[10]:


# always want the full size version of the featured images
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# found that the <button> element has 2 classes: 
# first class = btn 
# second class = btn outline light
# string for full image to be clicked on by user
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# why did we index chain at end of our code?


# In[12]:


# with new image expanded, now we want to:
# parse the full size image url 
html = browser.html
img_soup = soup(html, 'html.parser')


# In[15]:


# find relative image url 
# value of the src will be different each time the page is updated 
# we cannot only record the current value

# .get src will pull the link to our recent image

# look inside <img> element, in class fancybox, get the link in these tags
img_url_relative = img_soup.find('img', class_='fancybox-image').get('src')
img_url_relative


# In[17]:


# add our link from previous cell
img_url = f'https://spaceimages-mars.com/{img_url_relative}'
img_url


# In[20]:


# 10.3.5 collect information about mars planet profile
# all our html code is in the <table> element for this site
# we can use .read_html() to scrape the whole table

# create a new df from the html table
# index at 0 to pull only 1st table/1st item in list
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# assign coumns to df to make it easier for user
df.columns=['description', 'Mars', 'Earth']
# turn the column into df index
df.set_index('description', inplace=True)
# print the df 
df


# In[21]:


# add the df to our web application 
df.to_html()

# output shows html code for the <table> element with nested elements


# In[23]:


# close the automated browser 
browser.quit()


# In[ ]:


# 10.3.6 export to Python

