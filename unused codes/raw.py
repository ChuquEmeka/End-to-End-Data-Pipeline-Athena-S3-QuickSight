import pandas as pd
import numpy as np
import random
import json

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

# Generate unique IDs for products and customers
product_ids = list(range(1, len(expanded_product_data) + 1))
customer_ids = list(range(1, len(customer_names) + 1))

# Generate sales data
n_records = 300000

# Create a DataFrame for sales transactions (fact table)
sales_data = {
    'SaleID': np.arange(1, n_records + 1),
    'ProductID': [random.choice(product_ids) for _ in range(n_records)],  # Foreign Key
    'CustomerID': [random.choice(customer_ids) for _ in range(n_records)],  # Foreign Key
    'Quantity': np.random.randint(1, 10, size=n_records),
}

# Generate sequential transaction dates
start_date = pd.Timestamp('2014-01-01')  # Start date
end_date = pd.to_datetime('now').normalize()  # Ensure it does not exceed now
date_range = pd.date_range(start=start_date, end=end_date, freq='H')

# Assign random dates (including time) for each transaction
sales_data['Date'] = [random.choice(date_range) for _ in range(n_records)]

# Create DataFrame for sales transactions
df_sales = pd.DataFrame(sales_data)

# Ensure LocationID is present
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

# Add a random LocationID to each sale
df_sales['LocationID'] = [random.choice(df_location['LocationID']) for _ in range(n_records)]

# Create DataFrame for products
df_product = pd.DataFrame({
    'ProductID': product_ids,
    'ProductName': list(expanded_product_data.keys()),
    'Category': list(expanded_product_data.values()),
    'UnitCost': [unit_cost_data[product] for product in expanded_product_data.keys()],
    'UnitPrice': [cost * 1.5 for cost in unit_cost_data.values()],  # Example pricing strategy
})

# Create DataFrame for customers
df_customer = pd.DataFrame({
    'CustomerID': customer_ids,
    'CustomerName': customer_names,
    'Email': [f"{name.replace(' ', '').lower()}@example.com" for name in customer_names],
    'PhoneNumber': [f"+49 {random.randint(100000000, 999999999)}" for _ in customer_names],
})

# Create Payment dimension
payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Cash', 'Bank Transfer']
payment_data = pd.DataFrame({
    'PaymentID': np.arange(1, len(payment_methods) + 1),
    'PaymentMethod': payment_methods,
})

# Add PaymentID to sales data
df_sales['PaymentID'] = [random.choice(payment_data['PaymentID']) for _ in range(n_records)]

# Create Shipping dimension
shipping_data = {
    'ShippingID': np.arange(1, n_records + 1),
    'ShippingMethod': ['Standard', 'Express', 'Next Day'],
    'ShippingCost': [5.99, 9.99, 19.99],
}
df_shipping = pd.DataFrame(shipping_data)

# Add ShippingID to sales data
df_sales['ShippingID'] = [random.choice(df_shipping['ShippingID']) for _ in range(n_records)]

# Create Promotion dimension
promotion_data = {
    'PromotionID': np.arange(1, 6),  # Assuming 5 promotions
    'PromotionName': ['10% Off', 'Buy 1 Get 1 Free', 'Free Shipping', '20% Off', '5% Cashback'],
    'StartDate': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01']),
    'EndDate': pd.to_datetime(['2024-01-31', '2024-02-28', '2024-03-31', '2024-04-30', '2024-05-31']),
}
df_promotion = pd.DataFrame(promotion_data)

# Add PromotionID to sales data
df_sales['PromotionID'] = [random.choice(df_promotion['PromotionID']) for _ in range(n_records)]

# Create Review dimension
review_data = {
    'ReviewID': np.arange(1, n_records + 1),
    'ReviewText': [f"This product is {random.choice(['amazing', 'good', 'average', 'bad', 'excellent'])}!" for _ in range(n_records)],
    'Rating': [random.randint(1, 5) for _ in range(n_records)],
}
df_review = pd.DataFrame(review_data)

# Add ReviewID to sales data
df_sales['ReviewID'] = [random.choice(df_review['ReviewID']) for _ in range(n_records)]

# Create Marketing Channel dimension
marketing_channels = ['Email', 'Social Media', 'Search Engine', 'Affiliate', 'Direct']
df_marketing_channel = pd.DataFrame({
    'MarketingChannelID': np.arange(1, len(marketing_channels) + 1),
    'MarketingChannel': marketing_channels,
})

# Add MarketingChannelID to sales data
df_sales['MarketingChannelID'] = [random.choice(df_marketing_channel['MarketingChannelID']) for _ in range(n_records)]

# Output the generated data
df_sales.to_csv('sales_data.csv', index=False)
df_product.to_csv('product_data.csv', index=False)
df_customer.to_csv('customer_data.csv', index=False)
df_location.to_csv('location_data.csv', index=False)
payment_data.to_csv('payment_data.csv', index=False)
df_shipping.to_csv('shipping_data.csv', index=False)
df_promotion.to_csv('promotion_data.csv', index=False)
df_review.to_csv('review_data.csv', index=False)
df_marketing_channel.to_csv('marketing_channel_data.csv', index=False)

print("Data generation complete! Data saved to CSV files.")
