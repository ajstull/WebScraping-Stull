# imports
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
#import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# scrap all function
def scrape_all():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #goal is return a jsom that has all data needed, then load into MongoDB

    #get the information from the mars news page
    news_title, news_paragraph = scrape_news(browser)

    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    browser.quit()
    
    return marsData


#Scrape from the mars news page
def scrape_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #Delay for loading the page, it protects against scraping but it doesnt lol
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Converting the browser HTML to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    news_title = slide_elem.find('div', class_='content_title').get_text()

    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    return news_title, news_p

#Scrape through the featured image page
def scrape_feature_img(browser):
    #Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #Find by tag and click the full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click() 

    #Parsing the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    img_url = f'https://https://spaceimages-mars.com/{img_url_rel}'

    return img_url


#Scrape through the facts page
def scrape_facts_page(browser):
    
    #Visit URL
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Converting the browser html to a soup object
    html = browser.html
    facts_soup = soup(html, 'html.parser')

    #Finding the 'facts' location
    factsLocation = facts_soup.find('div', class_="diagram mt-4")
    factTable = factsLocation.find('table') # grabs the HTML code for the fact table

    #Creating an empty string to store facts
    facts = ""

    #Adding the text to the 'facts' string then return 'facts'
    facts += str(factTable)

    return facts

#Scrape through the hemi pages
def scrape_hemispheres(browser):
    
    #Visit URL
    url = "https://marshemispheres.com/"
    browser.visit(url)

    #Creating a list 
    hemisphere_image_urls = []

    #Next, using for loop, loop through these links, then click the link, then find the sample anchor, and return the href
    for i in range(4):
        hemisphereInfo = {}
        
        #To avoid a 'stale' element exception we will have to find the elements on each loop
        browser.find_by_css('a.product-item img')[i].click()
        
        #Then we find the sample image anchor tag 
        sample = browser.links.find_by_text('Sample').first
        
        #extract the href
        hemisphereInfo["img_url"] = sample['href']
        
        #Get hemis title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
        
        #Append hemis object to list
        hemisphere_image_urls.append(hemisphereInfo)
        
        browser.back()

        #Return the hemis urls 
        return hemisphere_image_urls



# set up as a flask app
if __name__ == "__main__":
    print(scrape_all())