#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Importing the required modules/libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[4]:


# Taking input from the user

print("Enter the url of the flipkart webpage !")
URL = input()


# In[5]:


HEADERS = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15','Accept-Language':'en-US,en;q=0.5'}
webpage = requests.get(URL,headers=HEADERS)

if (webpage.status_code == 200 ):
    print("Data Fetched Successfully !")
else:
    print(f"Error {webpage.status_code} !")

soup = BeautifulSoup(webpage.content,'html.parser')


# In[6]:


# Extracting the product links from webpage

parent_tags = soup.find_all("div", attrs={'class':'_1AtVbE col-12-12'})

links_list=[]

for tags in parent_tags:

    sub_parent_tags = tags.find("div", attrs={'class':'_13oc-S'})
    anchor_tag_soup = BeautifulSoup(str(sub_parent_tags),'html.parser')
    anchor_tag_links = anchor_tag_soup.find_all("a")
    
    for link in anchor_tag_links:
        
        product_link = "https://www.flipkart.com" + link.get('href')
        links_list.append(product_link)
            
# Converting the list to set so that frequency of each link remains 1

links_set = set(links_list)


# In[7]:


flipkart_scrapData = {'Product_Name':[],'Price':[],'Rating':[],'Availability':[],'Product_Link':[]}


# In[8]:


# Functions to scrap product details

# Function to extract product name 

def fetch_productName(product_link_soup):
    
    try:
        # Extracting the tag of product name
        product_name_tag = product_link_soup.find("span", attrs={'class':'B_NuCI'})
        
        # Extracting the product name
        product_name = (product_name_tag).text.strip()
    
    except AttributeError:
        product_name = "Not Available"
        
    return product_name

# Function to extract product price

def fetch_productPrice(product_link_soup):
    
    try:
        # Extracting upper tag of product price
        product_price_uppertag = product_link_soup.find("div", attrs={'class':'_25b18c'})
        
        # Extracting tag of product tag
        product_price_tag = product_price_uppertag.find("div", attrs={'class':'_30jeq3 _16Jk6d'})
        
        # Extracting the product price
        product_price = (product_price_tag).text.strip()
    
    except AttributeError:
        product_price = "Not Available"
        
    return product_price

# Function to extract product rating

def fetch_productRating(product_link_soup):
    
    try:
        # Extracting the uppper tag of product rating
        product_rating_tag = product_link_soup.find("span", attrs={'class':'_1lRcqv'}).find("div", attrs={'class':'_3LWZlK'})
        
        # Extracting the product rating
        product_rating = (product_rating_tag).text.strip() + "★"
    
    except AttributeError:
        product_rating = "NA"
        
    return product_rating

# Function to extract availability of product

def fetch_productAvailability(product_link_soup):
    
    try:
        product_availability_tag = product_link_soup.find("div", attrs={'class':'_2JC05C'})
        product_availability = product_availability_tag.text.strip()
        
    except AttributeError:
        try:
            # Extracting upper tag of product availability
            product_availability_uppertag = product_link_soup.find("div", attrs={'class':'_1AtVbE col-12-12'})
            
            # Extracting product availability
            product_availability_tag = product_availability_uppertag.find("div", attrs={'class':'_16FRp0'})
            product_availability = product_availability_tag.text.strip()
            
        except AttributeError:
            product_availability = "Available"
            
    return product_availability


# In[9]:


# Scrapping Product Details & Storing in a dictionary

for link in links_set:
    new_webpage = requests.get(link,headers=HEADERS)
    
    if ( new_webpage.status_code != 200 ):
        
        error_message = ("Error " + str(new_webpage.status_code) + " Access Denied")
        
    
        flipkart_scrapData['Product_Name'].append(error_message)
        flipkart_scrapData['Price'].append(error_message)
        flipkart_scrapData['Rating'].append(error_message)
        flipkart_scrapData['Availability'].append(error_message)
        flipkart_scrapData['Product_Link'].append(link)
        
        continue
        
    product_link_soup = BeautifulSoup(new_webpage.content,'html.parser')
    
    flipkart_scrapData['Product_Name'].append(fetch_productName(product_link_soup))
    flipkart_scrapData['Price'].append(fetch_productPrice(product_link_soup))
    flipkart_scrapData['Rating'].append(fetch_productRating(product_link_soup))
    flipkart_scrapData['Availability'].append(fetch_productAvailability(product_link_soup))
    flipkart_scrapData['Product_Link'].append(link)
    


# In[10]:


# Generating a dataframe using pandas library

flipkart_df = pd.DataFrame.from_dict(flipkart_scrapData)

# Converting the scrap data to a CSV File

flipkart_df.to_csv("flipkart_scrapData.csv",index=False)


# In[11]:


flipkart_df


# In[ ]:





# In[ ]:




