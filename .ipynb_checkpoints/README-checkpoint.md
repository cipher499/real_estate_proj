# real_estate_proj
A web application consisting of analytics, a price predictor, and a recommendation system on real estate data of Gurgaon. <p>

### Data Cleaning
- load in excel and spend time with the data, delete unnecessary rows
- delete the link and property id columms
- correct column names
- df['society'] = df['society'].apply(lambda name: re.sub(r'\d+(\.\d+)?\s?*', '',   	str(name)).strip()).str.lower()
- price -> make consistent
- price per feet
- bedroom == NaN; drop rows
- bedroom string formatting
- additional rooms column: make it binary-> (fill na with 'not available')
- create a new column, Area = price/price_per_sq_ft; df.insert(loc=4..
- property type column
