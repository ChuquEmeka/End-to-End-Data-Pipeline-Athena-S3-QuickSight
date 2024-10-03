import pandas as pd
import numpy as np
import random
import json
import boto3
# Business Name
business_name = "EmekaMarkt Deutschland"

# Expanded product names list with their appropriate categories
expanded_product_data = {
    'Phone': 'Electronics', 
    'Clock': 'Home Appliances', 
    'Laptop': 'Computers', 
    'Keyboard': 'Accessories', 
    'Pot': 'Kitchenware', 
    'Plates': 'Kitchenware', 
    'Spoon': 'Kitchenware', 
    'Tablet': 'Electronics', 
    'Monitor': 'Electronics', 
    'Headphones': 'Electronics', 
    'Television': 'Electronics', 
    'Blender': 'Home Appliances', 
    'Microwave': 'Home Appliances', 
    'Couch': 'Furniture', 
    'Desk': 'Furniture', 
    'Chair': 'Furniture', 
    'Camera': 'Cameras', 
    'Refrigerator': 'Home Appliances', 
    'Oven': 'Home Appliances', 
    'Printer': 'Office Supplies', 
    'Vacuum Cleaner': 'Home Appliances', 
    'Air Conditioner': 'Home Appliances', 
    'Toaster': 'Home Appliances', 
    'Mixer': 'Home Appliances', 
    'Washing Machine': 'Home Appliances', 
    'Dryer': 'Home Appliances', 
    'Dishwasher': 'Home Appliances', 
    'Shoes': 'Footwear', 
    'Backpack': 'Bags', 
    'Watch': 'Accessories', 
    'Book': 'Books', 
    'Pen': 'Office Supplies', 
    'Notebook': 'Office Supplies', 
    'Mug': 'Drinkware', 
    'Towel': 'Home Textiles', 
    'Bicycle': 'Outdoor', 
    'Scooter': 'Outdoor', 
    'Drill': 'Tools', 
    'Hammer': 'Tools', 
    'Fan': 'Home Appliances', 
    'Heater': 'Home Appliances', 
    'Lamp': 'Lighting', 
    'Rug': 'Home Textiles', 
    'Curtains': 'Home Textiles', 
    'Pillow': 'Home Textiles', 
    'Mattress': 'Furniture', 
    'Blanket': 'Home Textiles', 
    'Wardrobe': 'Furniture', 
    'Cupboard': 'Furniture', 
    'Perfume': 'Accessories', 
    'Shampoo': 'Home Appliances', 
    'Conditioner': 'Home Appliances', 
    'Sofa': 'Furniture', 
    'Table': 'Furniture', 
    'Headset': 'Electronics', 
    'Smartwatch': 'Electronics', 
    'Charger': 'Electronics', 
    'Speaker': 'Electronics', 
    'Router': 'Electronics', 
    'Modem': 'Electronics', 
    'Projector': 'Electronics'
}

# Sample data lists with celebrity names
customer_names = [
    'Emma Watson', 'Dwayne Johnson', 'Angelina Jolie', 'Chris Hemsworth', 
    'Adele', 'Leonardo DiCaprio', 'Taylor Swift', 'Shakira', 
    'Ed Sheeran', 'Selena Gomez', 'Benedict Cumberbatch', 'Rihanna', 
    'Daniel Craig', 'Kate Winslet', 'Drake', 'Bruno Mars', 
    'Gal Gadot', 'Robert Downey Jr.', 'Scarlett Johansson', 'Zayn Malik'
]

# Expanded countries and their respective cities
country_city_mapping = {
    'Germany': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne'],
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'UK': ['London', 'Birmingham', 'Manchester', 'Glasgow', 'Liverpool'],
    'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
    'Italy': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo'],
    'Spain': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza'],
    'Netherlands': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven'],
    'China': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu'],
    'Japan': ['Tokyo', 'Osaka', 'Yokohama', 'Nagoya', 'Sapporo']
}

# Unit cost dictionary to simulate realistic costs for products
unit_cost_data = {
    'Phone': 300, 'Clock': 20, 'Laptop': 800, 'Keyboard': 30, 'Pot': 15, 
    'Plates': 10, 'Spoon': 5, 'Tablet': 200, 'Monitor': 150, 'Headphones': 50, 
    'Television': 400, 'Blender': 40, 'Microwave': 100, 'Couch': 500, 'Desk': 150, 
    'Chair': 100, 'Camera': 600, 'Refrigerator': 800, 'Oven': 400, 'Printer': 150, 
    'Vacuum Cleaner': 200, 'Air Conditioner': 500, 'Toaster': 25, 'Mixer': 30, 
    'Washing Machine': 600, 'Dryer': 400, 'Dishwasher': 450, 'Shoes': 60, 
    'Backpack': 40, 'Watch': 100, 'Book': 15, 'Pen': 3, 'Notebook': 5, 'Mug': 7, 
    'Towel': 10, 'Bicycle': 200, 'Scooter': 300, 'Drill': 80, 'Hammer': 20, 
    'Fan': 50, 'Heater': 80, 'Lamp': 25, 'Rug': 40, 'Curtains': 30, 'Pillow': 20, 
    'Mattress': 400, 'Blanket': 25, 'Wardrobe': 600, 'Cupboard': 350, 'Perfume': 50, 
    'Shampoo': 10, 'Conditioner': 10, 'Sofa': 700, 'Table': 300, 'Headset': 70, 
    'Smartwatch': 250, 'Charger': 20, 'Speaker': 150, 'Router': 100, 'Modem': 90, 'Projector': 400
}

# Generating unique IDs for products and customers
product_ids = list(range(1, len(expanded_product_data) + 1))
customer_ids = list(range(1, len(customer_names) + 1))

n_records = 150000
# n_records = 15
# Creating a DataFrame for sales transactions (fact table)
sales_data = {
    'SaleID': np.arange(1, n_records + 1),
    'ProductID': [random.choice(product_ids) for _ in range(n_records)],  # Foreign Key
    'CustomerID': [random.choice(customer_ids) for _ in range(n_records)],  # Foreign Key
    'Quantity': np.random.randint(1, 10, size=n_records),
}

# Generating sequential transaction dates
start_date = pd.Timestamp('2014-01-01')  # Start date
end_date = pd.to_datetime('now').normalize()  # Ensure it does not exceed now
# end_date = pd.to_datetime('now', utc=True).normalize()
date_range = pd.date_range(start=start_date, end=end_date, freq='H')

# Assigning random dates (including time) for each transaction
sales_data['Date'] = [random.choice(date_range) for _ in range(n_records)]

# Creating DataFrame for sales transactions
df_sales = pd.DataFrame(sales_data)

# Ensuring LocationID is present
df_location = pd.DataFrame({
    'LocationID': np.arange(1, len(country_city_mapping) + 1),
    'Country': list(country_city_mapping.keys()),
    'State': [None] * len(country_city_mapping),  # Assuming no states for simplicity
    'City': [random.choice(cities) for cities in country_city_mapping.values()],
    'PostalCode': [random.randint(10000, 99999) for _ in range(len(country_city_mapping))],
    'Region': ['Europe' if country in ['Germany', 'UK', 'France', 'Italy', 'Spain', 'Netherlands'] 
               else 'North America' if country in ['USA', 'Canada'] 
               else 'Asia' if country in ['China', 'Japan'] 
               else 'Other' 
               for country in country_city_mapping.keys()]
})

# Adding a random LocationID to each sale
df_sales['LocationID'] = [random.choice(df_location['LocationID']) for _ in range(n_records)]

# Creating DataFrame for products
df_product = pd.DataFrame({
    'ProductID': product_ids,
    'ProductName': list(expanded_product_data.keys()),
    'Category': list(expanded_product_data.values()),
    'UnitCost': [unit_cost_data[product] for product in expanded_product_data.keys()],
    'UnitPrice': [round(cost * random.uniform(1.5, 3), 2) for cost in unit_cost_data.values()],
})

# Creating DataFrame for customers
df_customer = pd.DataFrame({
    'CustomerID': customer_ids,
    'CustomerName': customer_names,
    'Email': [f'{name.lower().replace(" ", ".")}@example.com' for name in customer_names],
    'PhoneNumber': [f'+49-{random.randint(1000000000, 9999999999)}' for _ in range(len(customer_names))],
    'LoyaltyStatus': [random.choice(['Bronze', 'Silver', 'Gold']) for _ in range(len(customer_names))]
})

# Creating DataFrame for promotions
promotion_ids = range(1, 11)  # Assuming 10 promotions
df_promotion = pd.DataFrame({
    'PromotionID': promotion_ids,
    'PromotionName': [f'Promo {i}' for i in promotion_ids],
    'DiscountRate': [random.uniform(0.05, 0.5) for _ in promotion_ids]  # 5% to 50% discount
})

# Creating DataFrame for shipping methods
shipping_ids = range(1, 6)  # Assuming 5 shipping methods
df_shipping = pd.DataFrame({
    'ShippingID': shipping_ids,
    'Method': ['Standard', 'Express', 'Overnight', 'International', 'Free'],
    'Cost': [random.uniform(5.0, 50.0) for _ in shipping_ids]  # Random shipping costs
})

# Creating DataFrame for payment methods
payment_ids = range(1, 5)  # Assuming 4 payment methods
df_payment = pd.DataFrame({
    'PaymentID': payment_ids,
    'Method': ['Credit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery'],
})

# Creating DataFrame for product reviews
df_product_reviews = pd.DataFrame({
    'ReviewID': range(1, 101),  # 100 reviews
    'ProductID': [random.choice(product_ids) for _ in range(100)],
    'CustomerID': [random.choice(customer_ids) for _ in range(100)],
    'Rating': [random.randint(1, 5) for _ in range(100)],
    'Comment': [f'This is a review for product {random.choice(product_ids)}' for _ in range(100)],
})

# Creating DataFrame for marketing channels
df_marketing = pd.DataFrame({
    'ChannelID': range(1, 6),  # Assuming 5 marketing channels
    'ChannelName': ['Email', 'Social Media', 'Search Engine', 'Affiliate', 'Direct'],
})

# Creating JSON objects for each sale and add dimension data as JSON strings
json_objects = []
for index, row in df_sales.iterrows():
    sale_record = {
        "SaleID": int(row['SaleID']),
        "ProductID": int(row['ProductID']),
        "CustomerID": int(row['CustomerID']),
        "Quantity": int(row['Quantity']),
        "Date": row['Date'].isoformat(),
        "LocationID": int(row['LocationID']),
        "PaymentID": int(random.choice(payment_ids)),
        "ShippingID": int(random.choice(shipping_ids)),
        "PromotionID": int(random.choice(promotion_ids)),
        "ReviewID": int(random.choice(df_product_reviews['ReviewID'])),
    }
    
    # Adding dimension data as JSON strings
    sale_record['Product'] = df_product[df_product['ProductID'] == sale_record['ProductID']].to_json(orient='records')
    sale_record['Customer'] = df_customer[df_customer['CustomerID'] == sale_record['CustomerID']].to_json(orient='records')
    sale_record['Location'] = df_location[df_location['LocationID'] == sale_record['LocationID']].to_json(orient='records')
    sale_record['Promotion'] = df_promotion[df_promotion['PromotionID'] == sale_record['PromotionID']].to_json(orient='records')
    sale_record['Shipping'] = df_shipping[df_shipping['ShippingID'] == sale_record['ShippingID']].to_json(orient='records')
    sale_record['Review'] = df_product_reviews[df_product_reviews['ReviewID'] == sale_record['ReviewID']].to_json(orient='records')
    sale_record['MarketingChannel'] = df_marketing[df_marketing['ChannelID'] == sale_record['PromotionID']].to_json(orient='records')

    json_objects.append(sale_record)

# Converting to DataFrame for CSV
df_final = pd.DataFrame(json_objects)

# Save to CSV
# df_final.to_csv('sample_raw_sales_data.csv', index=False)
#########################################################################

output_file = 'raw_sales_data.csv'
df_final.to_csv(output_file, index=False)

# Uploading to S3
s3 = boto3.client('s3')
bucket_name = 'emeka-market-raw-sales-data'
s3_file_path = 'raw_sales_data.csv'  # This is the key (name) you want for the file in S3

# Uploading the file to S3 with the specified bucket name and key
s3.upload_file(output_file, bucket_name, s3_file_path)

print(f"Sales data saved to {output_file} and uploaded to S3 bucket {bucket_name}.")
#########################################################################
# Displaying sample outputs
print("Sales Data Sample with Dimensions:")
print(df_final.head())
