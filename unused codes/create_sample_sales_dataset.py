import pandas as pd
import numpy as np
import random
import json

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

# Sample data lists
customer_names = ['Olivia Johnson', 'Liam Smith', 'Emma Brown', 'Noah Davis', 'Ava Miller',
                  'Oliver Wilson', 'Sophia Moore', 'Elijah Taylor', 'Isabella Anderson', 'Lucas Thomas',
                  'Mia Jackson', 'Mason White', 'Amelia Harris', 'James Martin', 'Harper Thompson',
                  'Benjamin Garcia', 'Evelyn Martinez', 'Logan Robinson', 'Charlotte Clark', 'Alexander Rodriguez',
                  'Grace Lewis', 'Jackson Lee', 'Lily Walker', 'Aiden Hall', 'Scarlett Young',
                  'Caleb Allen', 'Aria King', 'Gabriel Wright', 'Chloe Scott', 'Samuel Green']

regions = ['North America', 'Europe', 'Asia', 'South America']
payment_methods = ['Credit Card', 'PayPal', 'Bank Transfer', 'Cash', 'Bitcoin', 'Apple Pay', 'Google Pay']
suppliers = ['Amazon', 'eBay', 'AliExpress', 'Walmart', 'Target']
marketing_channels = ['Social Media', 'Search Engine', 'Email', 'Direct', 'Affiliate', 'Paid Ads']

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

# Create DataFrame for products
df_product = pd.DataFrame({
    'ProductID': product_ids,
    'ProductName': list(expanded_product_data.keys()),
    'Category': list(expanded_product_data.values()),
    'UnitCost': [unit_cost_data[name] for name in expanded_product_data.keys()],
    'Supplier': [random.choice(suppliers) for _ in range(len(expanded_product_data))]
})

# Create DataFrame for customers
df_customer = pd.DataFrame({
    'CustomerID': customer_ids,
    'CustomerName': customer_names,
    'Region': [random.choice(regions) for _ in customer_ids],
    'CustomerSegment': [random.choice(['B2B', 'B2C']) for _ in customer_ids],
    'LoyaltyProgram': [random.choice(['Silver', 'Gold', 'Platinum', 'None']) for _ in customer_ids]
})

# Create DataFrame for suppliers
df_supplier = pd.DataFrame({
    'SupplierID': range(1, len(suppliers) + 1),
    'SupplierName': suppliers,
    'ContactInfo': [f'contact@supplier{idx}.com' for idx in range(1, len(suppliers) + 1)],
    'Location': ['Germany'] * len(suppliers)
})

# Create DataFrame for shipping methods
shipping_methods = ['Standard', 'Express', 'Overnight']
df_shipping = pd.DataFrame({
    'ShippingID': range(1, len(shipping_methods) + 1),
    'ShippingMethod': shipping_methods,
    'ShippingCost': [5.0, 10.0, 20.0],
    'ShippingTime': ['3-5 days', '1-3 days', 'Next day'],
    'Carrier': ['Carrier A', 'Carrier B', 'Carrier C'],
    'ShippingRegion': ['Europe', 'Europe', 'Europe']
})

# Create DataFrame for payment methods
payment_methods_data = {
    'PaymentMethodID': range(1, len(payment_methods) + 1),
    'PaymentMethodName': payment_methods,
    'TransactionFee': [1.5, 0, 0.5, 0, 0.1, 0.0, 0.0]
}

df_payment_methods = pd.DataFrame(payment_methods_data)

# Create DataFrame for marketing channels
df_marketing_channels = pd.DataFrame({
    'ChannelID': range(1, len(marketing_channels) + 1),
    'ChannelName': marketing_channels,
    'ChannelType': ['Social', 'Organic', 'Email', 'Direct', 'Paid'],
    'ConversionRate': np.random.rand(len(marketing_channels))  # Random conversion rates
})

# Create DataFrame for promotions
df_promotions = pd.DataFrame({
    'PromotionID': range(1, 6),
    'PromotionType': ['Discount', 'Bundle', 'Seasonal', 'Clearance', 'Loyalty Reward'],
    'DiscountRate': [0.10, 0.15, 0.20, 0.25, 0.30],
    'StartDate': pd.date_range(start='2024-01-01', periods=5, freq='M'),
    'EndDate': pd.date_range(start='2024-02-01', periods=5, freq='M')
})

# Create DataFrame for product reviews
df_product_reviews = pd.DataFrame({
    'ReviewID': range(1, n_records // 10),  # Assume 10% of products have reviews
    'ProductID': [random.choice(product_ids) for _ in range(n_records // 10)],
    'CustomerID': [random.choice(customer_ids) for _ in range(n_records // 10)],
    'Rating': np.random.randint(1, 6, size=n_records // 10),  # Ratings from 1 to 5
    'Feedback': ['Great product!' for _ in range(n_records // 10)],  # Sample feedback
    'ReviewDate': [random.choice(date_range) for _ in range(n_records // 10)]
})

# Create DataFrame for returns and refunds
df_returns = pd.DataFrame({
    'ReturnID': range(1, n_records // 20),  # Assume 5% of transactions result in returns
    'ProductID': [random.choice(product_ids) for _ in range(n_records // 20)],
    'CustomerID': [random.choice(customer_ids) for _ in range(n_records // 20)],
    'ReturnReason': ['Defective' for _ in range(n_records // 20)],
    'RefundAmount': [random.uniform(10, 100) for _ in range(n_records // 20)],
    'ReturnDate': [random.choice(date_range) for _ in range(n_records // 20)],
    'RefundDate': [random.choice(date_range) for _ in range(n_records // 20)]
})

# Create DataFrame for loyalty programs
df_loyalty_programs = pd.DataFrame({
    'LoyaltyProgramID': range(1, len(customer_ids) + 1),
    'CustomerID': customer_ids,
    'LoyaltyPoints': [random.randint(0, 1000) for _ in customer_ids],
    'MembershipLevel': [random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']) for _ in customer_ids],
    'JoinDate': [random.choice(date_range) for _ in customer_ids]
})

# Generate a random shipping method for each sale
df_sales['ShippingMethod'] = [random.choice(shipping_methods) for _ in range(n_records)]

# Function to generate payment method based on weights
def generate_payment_method(row):
    return random.choices(payment_methods, weights=[0.4, 0.3, 0.15, 0.1, 0.025, 0.025], k=1)[0]

df_sales['PaymentMethod'] = df_sales.apply(generate_payment_method, axis=1)

# Add additional fields for profit margin and return reasons
df_sales['SalePrice'] = df_sales['Quantity'] * df_product['UnitCost'][df_sales['ProductID'] - 1].values
df_sales['TotalRevenue'] = df_sales['SalePrice'] * df_sales['Quantity']
df_sales['ProfitMargin'] = df_sales['TotalRevenue'] * np.random.uniform(0.1, 0.3, size=n_records)  # Random profit margin between 10-30%
df_sales['ReturnFlag'] = np.random.choice(['Yes', 'No'], size=n_records, p=[0.05, 0.95])  # 5% returns
df_sales['ReturnReason'] = np.where(df_sales['ReturnFlag'] == 'Yes',
                                     np.random.choice(['Defective', 'Not as described', 'Changed mind'], size=n_records),
                                     None)

# Add loyalty points earned
df_sales['LoyaltyPointsEarned'] = df_sales['SalePrice'] * 0.1  # 10% of sale price

# Combine all dimensions into a single JSON object for each sale
def combine_dimensions(row):
    product_info = df_product.loc[df_product['ProductID'] == row['ProductID']].iloc[0]
    customer_info = df_customer.loc[df_customer['CustomerID'] == row['CustomerID']].iloc[0]
    
    return json.dumps({
        'Product': {
            'ProductID': product_info['ProductID'],
            'ProductName': product_info['ProductName'],
            'Category': product_info['Category'],
            'UnitCost': product_info['UnitCost'],
            'Supplier': product_info['Supplier']
        },
        'Customer': {
            'CustomerID': customer_info['CustomerID'],
            'CustomerName': customer_info['CustomerName'],
            'Region': customer_info['Region'],
            'CustomerSegment': customer_info['CustomerSegment'],
            'LoyaltyProgram': customer_info['LoyaltyProgram']
        },
        'Shipping': {
            'ShippingMethod': row['ShippingMethod'],
            'Cost': df_shipping.loc[df_shipping['ShippingMethod'] == row['ShippingMethod'], 'ShippingCost'].values[0],
            'DeliveryTime': df_shipping.loc[df_shipping['ShippingMethod'] == row['ShippingMethod'], 'ShippingTime'].values[0]
        },
        'Payment': {
            'PaymentMethod': row['PaymentMethod'],
            'TransactionFee': df_payment_methods.loc[df_payment_methods['PaymentMethodName'] == row['PaymentMethod'], 'TransactionFee'].values[0]
        },
        'SaleInfo': {
            'Quantity': row['Quantity'],
            'SaleDate': row['Date'],
            'SalePrice': row['SalePrice'],
            'TotalRevenue': row['TotalRevenue'],
            'ProfitMargin': row['ProfitMargin'],
            'ReturnFlag': row['ReturnFlag'],
            'ReturnReason': row['ReturnReason'],
            'LoyaltyPointsEarned': row['LoyaltyPointsEarned']
        },
        'Promotion': {
            'PromotionID': random.choice(df_promotions['PromotionID']),
            'PromotionType': 'Discount',
            'DiscountRate': 0.10,
            'StartDate': '2024-01-01',
            'EndDate': '2024-02-01'
        },
        'Review': {
            'ReviewID': random.choice(df_product_reviews['ReviewID']),
            'Rating': random.randint(1, 5),
            'Feedback': 'Great product!',
            'ReviewDate': '2024-01-01'
        },
        'ReturnInfo': {
            'ReturnID': random.choice(df_returns['ReturnID']),
            'ReturnReason': 'Defective',
            'RefundAmount': random.uniform(10, 100),
            'ReturnDate': '2024-01-02',
            'RefundDate': '2024-01-03'
        },
        'LoyaltyProgram': {
            'LoyaltyProgramID': customer_info['CustomerID'],
            'LoyaltyPoints': random.randint(0, 1000),
            'MembershipLevel': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']),
            'JoinDate': '2024-01-01'
        },
        'MarketingChannel': {
            'ChannelID': random.choice(df_marketing_channels['ChannelID']),
            'ChannelName': random.choice(marketing_channels),
            'ChannelType': 'Social',
            'ConversionRate': np.random.rand()
        }
    })

# Apply the combine function to create a new column with the JSON object
df_sales['TransactionData'] = df_sales.apply(combine_dimensions, axis=1)

# Save to CSV
df_sales[['SaleID', 'TransactionData']].to_csv('sales_data.csv', index=False)

print("Sales data has been successfully created and saved.")
