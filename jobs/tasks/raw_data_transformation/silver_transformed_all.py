

import pandas as pd
import json
import os
import boto3
from io import StringIO

# Function to read raw sales data directly from S3
def read_sales_data_from_s3(bucket_name='emeka-market-raw-sales-data', s3_file_path='sample_raw_sales_data.csv'):
    s3 = boto3.client('s3')
    # Read the CSV file from S3 into a DataFrame
    obj = s3.get_object(Bucket=bucket_name, Key=s3_file_path)
    raw_data = obj['Body'].read().decode('utf-8')
    df_raw = pd.read_csv(StringIO(raw_data))
    return df_raw

# Function to transform raw sales data and save as separate tables
def transform_sales_data(df_raw, output_dir='output'):
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



    import boto3
    from io import StringIO

    # Initialize the S3 client
    # s3 = boto3.client('s3')
    # bucket_name = 'emeka-transformed-sales-data'

    # # Function to upload a DataFrame to S3 as CSV
    # def upload_to_s3(df, folder_name, file_name, bucket):
    #     csv_buffer = StringIO()
    #     df.to_csv(csv_buffer, index=False)
    #     s3.put_object(Bucket=bucket, Key=f'{folder_name}/{file_name}', Body=csv_buffer.getvalue())

    # # Save unique dimension tables and fact table to their respective folders in S3
    # upload_to_s3(df_product, 'product_dim', 'product_dim.csv', bucket_name)
    # upload_to_s3(df_customer, 'customer_dim', 'customer_dim.csv', bucket_name)
    # upload_to_s3(df_location, 'location_dim', 'location_dim.csv', bucket_name)
    # upload_to_s3(df_promotion, 'promotion_dim', 'promotion_dim.csv', bucket_name)
    # upload_to_s3(df_shipping, 'shipping_dim', 'shipping_dim.csv', bucket_name)
    # upload_to_s3(df_review, 'review_dim', 'review_dim.csv', bucket_name)
    # upload_to_s3(df_fact_sales, 'fact_sales', 'fact_sales.csv', bucket_name)



    print("Data transformation complete. Saved tables:")
    print("- product_dim.csv")
    print("- customer_dim.csv")
    print("- location_dim.csv")
    print("- promotion_dim.csv")
    print("- shipping_dim.csv")
    print("- review_dim.csv")
    print("- fact_sales.csv")

# Main execution
if __name__ == "__main__":
    df_raw = read_sales_data_from_s3()  # Read the raw sales data from S3
    transform_sales_data(df_raw)  # Transform the data
