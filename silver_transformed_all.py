import pandas as pd
import json
import os

# Function to transform raw sales data and save as separate tables
def transform_sales_data(input_file='raw_sales_data.csv', output_dir='output'):
    # Load raw sales data
    df_raw = pd.read_csv(input_file)

    # Exploding Product data and getting unique records
    df_raw['Product'] = df_raw['Product'].apply(lambda x: json.loads(x)[0])
    df_product = pd.json_normalize(df_raw['Product']).drop_duplicates(subset='ProductID')
    df_product.rename(columns={"ProductID": "ProductID"}, inplace=True)
    df_product['ProductID'] = df_product['ProductID'].astype(int)

    # Exploding Customer data and getting unique records
    df_raw['Customer'] = df_raw['Customer'].apply(lambda x: json.loads(x)[0])
    df_customer = pd.json_normalize(df_raw['Customer']).drop_duplicates(subset='CustomerID')
    df_customer.rename(columns={"CustomerID": "CustomerID"}, inplace=True)
    df_customer['CustomerID'] = df_customer['CustomerID'].astype(int)

    # Exploding Location data and getting unique records
    df_raw['Location'] = df_raw['Location'].apply(lambda x: json.loads(x)[0])
    df_location = pd.json_normalize(df_raw['Location']).drop_duplicates(subset='LocationID')
    df_location.rename(columns={"LocationID": "LocationID"}, inplace=True)
    df_location['LocationID'] = df_location['LocationID'].astype(int)

    # Exploding Promotion data and getting unique records
    df_raw['Promotion'] = df_raw['Promotion'].apply(lambda x: json.loads(x)[0])
    df_promotion = pd.json_normalize(df_raw['Promotion']).drop_duplicates(subset='PromotionID')
    df_promotion.rename(columns={"PromotionID": "PromotionID"}, inplace=True)
    df_promotion['PromotionID'] = df_promotion['PromotionID'].astype(int)

    # Exploding Shipping data and getting unique records
    df_raw['Shipping'] = df_raw['Shipping'].apply(lambda x: json.loads(x)[0])
    df_shipping = pd.json_normalize(df_raw['Shipping']).drop_duplicates(subset='ShippingID')
    df_shipping.rename(columns={"ShippingID": "ShippingID"}, inplace=True)
    df_shipping['ShippingID'] = df_shipping['ShippingID'].astype(int)

    # Exploding Review data and getting unique records
    df_raw['Review'] = df_raw['Review'].apply(lambda x: json.loads(x)[0])
    df_review = pd.json_normalize(df_raw['Review']).drop_duplicates(subset='ReviewID')
    df_review.rename(columns={"ReviewID": "ReviewID"}, inplace=True)
    df_review['ReviewID'] = df_review['ReviewID'].astype(int)

    # Create the Fact table
    df_fact_sales = df_raw[['SaleID', 'Quantity', 'Date', 'PaymentID']].copy()

    # Ensure SaleID is int
    df_fact_sales['SaleID'] = df_fact_sales['SaleID'].astype(int)

    # Map IDs directly
    df_fact_sales['ShippingID'] = df_raw['Shipping'].apply(lambda x: x['ShippingID'] if isinstance(x, dict) else json.loads(x)[0]['ShippingID'])
    df_fact_sales['PromotionID'] = df_raw['Promotion'].apply(lambda x: x['PromotionID'] if isinstance(x, dict) else json.loads(x)[0]['PromotionID'])
    df_fact_sales['ReviewID'] = df_raw['Review'].apply(lambda x: x['ReviewID'] if isinstance(x, dict) else json.loads(x)[0]['ReviewID'])
    df_fact_sales['ProductID'] = df_raw['Product'].apply(lambda x: x['ProductID'] if isinstance(x, dict) else json.loads(x)[0]['ProductID'])
    df_fact_sales['LocationID'] = df_raw['Location'].apply(lambda x: x['LocationID'] if isinstance(x, dict) else json.loads(x)[0]['LocationID'])
    df_fact_sales['CustomerID'] = df_raw['Customer'].apply(lambda x: x['CustomerID'] if isinstance(x, dict) else json.loads(x)[0]['CustomerID'])

    # Save unique dimension tables and fact table to CSV in the specified output directory
    df_product.to_csv(os.path.join(output_dir, 'product_dim.csv'), index=False)
    df_customer.to_csv(os.path.join(output_dir, 'customer_dim.csv'), index=False)
    df_location.to_csv(os.path.join(output_dir, 'location_dim.csv'), index=False)
    df_promotion.to_csv(os.path.join(output_dir, 'promotion_dim.csv'), index=False)
    df_shipping.to_csv(os.path.join(output_dir, 'shipping_dim.csv'), index=False)
    df_review.to_csv(os.path.join(output_dir, 'review_dim.csv'), index=False)
    df_fact_sales.to_csv(os.path.join(output_dir, 'fact_sales.csv'), index=False)

    print("Data transformation complete. Saved tables:")
    print("- product_dim.csv")
    print("- customer_dim.csv")
    print("- location_dim.csv")
    print("- promotion_dim.csv")
    print("- shipping_dim.csv")
    print("- review_dim.csv")
    print("- fact_sales.csv")

# Call the function if you want to execute the transformation
transform_sales_data()
