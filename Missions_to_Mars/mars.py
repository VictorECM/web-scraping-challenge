# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo

#from selenium import webdriver
from splinter import Browser
from bs4 import BeautifulSoup
import fileinput
import os

mars_info={}
def scrape():
  
    url='https://mars.nasa.gov/news/'

    print(url)
    response=requests.get(url)
    print(response)

    soup=BeautifulSoup(response.text,'html.parser')


    # Examine the website for results and determine the element

    results= soup.find_all('div',class_='content_title')
    print(results)


    results = soup.find_all('div', class_='slide')
    results


    results = soup.find_all('div', class_='slide')

    errors = 0

    posts_list = []

    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            news_title = result.find('div', class_='content_title').find('a').text
            
            news_title = news_title.replace('\n', '').replace('\r', '')
            #title = title.find('a').text
            print(news_title)
            
            # Identify and return price of listing
            news_p = result.find('div', class_='rollover_description_inner').text
            
            news_p = news_p.replace('\n', '').replace('\r', '')
            print(news_p)
            
            # Identify and return link to listing
            news_link = result.find('div', class_='content_title').a['href']
            print(news_link)
            
            print('***********\n')
            
            # Run only if title, price, and link are available
            if (news_title and news_p and news_link):
    #             print results
                print('-------------')
                print(news_title)
                print(news_p)
                print(news_link)


                # Dictionary to be inserted as a MongoDB document
                post = {
                    'news_title': news_title,
                    'news_p': news_p,
                    'news_link': news_link
                }
    #             print(post)
    #             
                posts_list.append(post)
                
            
            


        except Exception as e:
            errors =+ 1
    mars_info["post"] =posts_list
    

    # Step-2 JPL Mars Space Images -Featured

    #pointing to the directory where chromedriver exists
    executable_path = {"executable_path":r"C:\Users\Divya\Web based activities\Web_scrapping_challenge\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless = False)



    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)


    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, "html.parser")

    # Retrieve background-image url from style tag 
    image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = "https://www.jpl.nasa.gov"

    # Concatenate website url with scrapped route
    image_url = main_url + image_url

    # Display full link to featured image
    image_url

    quotes = soup.find_all('img')

    for quote in quotes:
        if 'spaceimages' in quote['src']:
            print(quote['src'])
    mars_info["Feature-image"]= image_url

    featured_image_url

    # Mars Facts- space-facts.com/mars

    import pandas as pd


    url = 'https://space-facts.com/mars/'


    tables = pd.read_html(url)
    tables



    df = tables[0]
    df.columns = ['KPI', 'Data']
    df


    html_table = df.to_html(index=False, border=None)
    html_table



    html_table = html_table.replace('\n', '')

    html_table


    html_table = html_table.replace('<table border="1" class="dataframe">', '<table class="table">')
    html_table = html_table.replace('<thead>', '<thead class="thead-dark">')
    html_table = html_table.replace('<tr style="text-align: right;">', '<tr>')

    html_table = html_table.replace('<th>', '<th scope="col">')

    html_table


    df.to_html(buf='Output/table1.html',index=False, border=None)
    mars_info["table"]= html_table

    import fileinput



    with fileinput.FileInput('output/table1.html', inplace=True) as file:
        for line in file:
            print(line.replace('<table border="1" class="dataframe">', '<table class="table">').              replace('<thead>', '<thead class="thead-dark">').              replace('<tr style="text-align: right;">', '<tr>').              replace('<th>', '<th scope="col">'),              end='')


    # get_ipython().system('output/table.html')

    # Mars Hemispheres- USGS Website

    executable_path = {"executable_path":r"C:\Users\Divya\Web based activities\Web_scrapping_challenge\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless = False)


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # print(soup)


    hemisphere_data=requests.get(url)
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        

    # Display hemisphere_image_urls
    hemisphere_image_urls
    mars_info["hemisphere"]= hemisphere_image_urls


    # print(hemisphere_image_urls)



    return(mars_info)