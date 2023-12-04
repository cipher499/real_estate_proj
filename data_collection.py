import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

city = "gurgaon"

# User Agent
headers = {
    'authority': 'www.99acres.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': f'https://www.99acres.com/flats-in-{city}-ffid-page',
    'sec-ch-ua': '"Chromium";v="107", "Not;A=Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/527.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

# create the directory structure
project_dir = "/home/shwetank/git_ projects/real_estate_proj"

subdirectories = ["data", f"data/{city}", f"data/{city}/flats", f"data/{city}/societies", f'data/{city}/residential', f'data/{city}/independ_pageent_houses']

for subdir in subdirectories:
    dir_path = os.path.join(project_dir, subdir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"created directory: {dir_path}")
    else:
        print(f"directory already exists: {dir_path}")

"""
Scraping the 99acres website for flats data in the chosen city
"""

# Page number to start_page from
start_page = int(input("Enter page number to start_page from:")) # start_pageing Page

# scraping upto 10 pages; can be varied
end_page = start_page+10

page_num = start_page
req=0

# create a dataframe to store the collected data
flats = pd.DataFrame()

try :
    while page_num < end_page:
        i=1
        url = f'https://www.99acres.com/flats-in-{city}-ffid-page-{page_num}'
        page = requests.get(url, headers=headers)
        pageSoup = BeautifulSoup(page.content, 'html.parser')
        req+=1
        for soup in pageSoup.select_one('div[data-label="SEARCH"]').select('section[data-hydration-on-demand="true"]'):

        # Extract property name and property sub-name
            try:
                property_name = soup.select_one('a.srpTuple__propertyName').text.strip()
                # Extract link
                link = soup.select_one('a.srpTuple__propertyName')['href']
                society = soup.select_one('#srp_tuple_society_heading').text.strip()
            except:
                continue
            # Detail Page
            page = requests.get(link, headers=headers)
            dpageSoup = BeautifulSoup(page.content, 'html.parser')
            req += 1
            try:
                #price Range
                price = dpageSoup.select_one('#pdPrice2').text.strip()
            except:
                price = ''

            # Area
            try:
                area = soup.select_one('#srp_tuple_price_per_unit_area').text.strip()
            except:
                area =''
            # Area with Type
            try:
                areaWithType = dpageSoup.select_one('#factArea').text.strip()
            except:
                areaWithType = ''


            # Configuration
            try:
                bedRoom = dpageSoup.select_one('#bedRoomNum').text.strip()
            except:
                bedRoom = ''
            try:
                bathroom = dpageSoup.select_one('#bathroomNum').text.strip()
            except:
                bathroom = ''
            try:
                balcony = dpageSoup.select_one('#balconyNum').text.strip()
            except:
                balcony = ''

            try:
                additionalRoom = dpageSoup.select_one('#additionalRooms').text.strip()
            except:
                additionalRoom = ''


            # Address

            try:
                address = dpageSoup.select_one('#address').text.strip()
            except:
                address = ''
            # Floor Number
            try:
                floorNum = dpageSoup.select_one('#floorNumLabel').text.strip()
            except:
                floorNum = ''

            try:
                facing = dpageSoup.select_one('#facingLabel').text.strip()
            except:
                facing = ''

            try:
                agePossession = dpageSoup.select_one('#agePossessionLbl').text.strip()
            except:
                agePossession = ''

            # Nearby Locations

            try:
                nearbyLocations = [i.text.strip() for i in dpageSoup.select_one('div.NearByLocation__tagWrap').select('span.NearByLocation__infoText')]
            except:
                nearbyLocations = ''

            # Descriptions
            try:
                description = dpageSoup.select_one('#description').text.strip()
            except:
                description = ''

            # Furnish Details
            try:
                furnishDetails = [i.text.strip() for i in dpageSoup.select_one('#FurnishDetails').select('li')]
            except:
                furnishDetails = ''

            # Features
            if furnishDetails:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[1].select('li')]
                except:
                    features = ''
            else:
                try:
                    features = [i.text.strip() for i in dpageSoup.select('#features')[0].select('li')]
                except:
                    features = ''



            # Rating by Features
            try:
                rating = [i.text for i in dpageSoup.select_one('div.review__rightSide>div>ul>li>div').select('div.ratingByFeature__circleWrap')]
            except:
                rating = ''
            # print(top_f)

            try:
                # Property ID
                property_id = dpageSoup.select_one('#Prop_Id').text.strip()
            except:
                property_id = ''

            # Create a dictionary with the given variables
            property_data = {
            'property_name': property_name,
            'link': link,
            'society': society,
            'price': price,
            'area': area,
            'areaWithType': areaWithType,
            'bedRoom': bedRoom,
            'bathroom': bathroom,
            'balcony': balcony,
            'additionalRoom': additionalRoom,
            'address': address,
            'floorNum': floorNum,
            'facing': facing,
            'agePossession': agePossession,
            'nearbyLocations': nearbyLocations,
            'description': description,
            'furnishDetails': furnishDetails,
            'features': features,
            'rating': rating,
            'property_id': property_id
        }


            temp_df = pd.DataFrame.from_records([property_data])
            # print(temp_df)
            flats = pd.concat([flats, temp_df], ignore_index=True)
            i += 1
            # if os.path.isfile(csv_file):
            # # Append_page DataFrame to the existing file without header
            #     temp_df.to_csv(csv_file, mode='a', header=False, index=False)
            # else:
            #     # Write DataFrame to the file with header
            #     temp_df.to_csv(csv_file, mode='a', header=True, index=False)

            if req % 4==0:
                time.sleep(10)
            if req % 15 == 0:
                time.sleep(50)
        print(f'{page_num} -> {i}')
        page_num += 1

except AttributeError as e:
    print(e)
    print("----------------")
    print("""Your IP might have blocked. Delete Runtime and reconnect again with updating start_page page number.\n
            You would see in output above like 1 -> 15\ and so 1 is page number and 15 is data items extracted.""")
    csv_file_path = f"/home/shwetank/git_ projects/real_estate_proj/data/gurgaon/flats/flats_{city}_data-page-{start_page}-{page_num-1}.csv"

    # This file will be new every time if start_page page will chnage, but still taking here mode as append_page
    if os.path.isfile(csv_file_path):
    # Append_page DataFrame to the existing file without header
        flats.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        # Write DataFrame to the file with header - first time write
        flats.to_csv(csv_file_path, mode='a', header=True, index=False)