import pandas as pd
import json
import boto3
from io import StringIO


def read_sales_data_from_s3(bucket_name, s3_file_path):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=s3_file_path)
    raw_data = obj['Body'].read().decode('utf-8')
    df_raw = pd.read_csv(StringIO(raw_data))
    return df_raw

def save_to_s3(bucket_name, s3_file_path, df):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, s3_file_path).put(Body=csv_buffer.getvalue())

def silver_transformation(input_bucket, input_file, output_bucket, output_file):
    # Load raw sales data from S3
    df_raw = read_sales_data_from_s3(input_bucket, input_file)

    # Exploding the JSON columns for each sale
    df_sales_expanded = pd.DataFrame()

    # Exploding Product data
    df_raw['Product'] = df_raw['Product'].apply(lambda x: json.loads(x)[0])
    df_product = pd.json_normalize(df_raw['Product'])
    df_sales_expanded = pd.concat([df_raw, df_product], axis=1)
    df_sales_expanded.drop(columns=['Product'], inplace=True)

    # Exploding Customer data
    df_raw['Customer'] = df_raw['Customer'].apply(lambda x: json.loads(x)[0])
    df_customer = pd.json_normalize(df_raw['Customer'])
    df_sales_expanded = pd.concat([df_sales_expanded, df_customer], axis=1)
    df_sales_expanded.drop(columns=['Customer'], inplace=True)

    # Exploding Location data
    df_raw['Location'] = df_raw['Location'].apply(lambda x: json.loads(x)[0])
    df_location = pd.json_normalize(df_raw['Location'])
    df_sales_expanded = pd.concat([df_sales_expanded, df_location], axis=1)
    df_sales_expanded.drop(columns=['Location'], inplace=True)

    # Exploding Promotion data
    df_raw['Promotion'] = df_raw['Promotion'].apply(lambda x: json.loads(x)[0])
    df_promotion = pd.json_normalize(df_raw['Promotion'])
    df_sales_expanded = pd.concat([df_sales_expanded, df_promotion], axis=1)
    df_sales_expanded.drop(columns=['Promotion'], inplace=True)

    # Exploding Shipping data
    df_raw['Shipping'] = df_raw['Shipping'].apply(lambda x: json.loads(x)[0])
    df_shipping = pd.json_normalize(df_raw['Shipping'])
    df_sales_expanded = pd.concat([df_sales_expanded, df_shipping], axis=1)
    df_sales_expanded.drop(columns=['Shipping'], inplace=True)

    # Exploding Review data
    df_raw['Review'] = df_raw['Review'].apply(lambda x: json.loads(x)[0])
    df_review = pd.json_normalize(df_raw['Review'])
    df_sales_expanded = pd.concat([df_sales_expanded, df_review], axis=1)
    df_sales_expanded.drop(columns=['Review'], inplace=True)

    # Save the silver table to S3
    save_to_s3(output_bucket, output_file, df_sales_expanded)

    print("Data transformation complete. Saved to:", output_file)

# Main execution
if __name__ == "__main__":
    input_bucket = 'emeka-market-raw-sales-data'
    input_file = 'sample_raw_sales_data.csv'
    output_bucket = 'emeka-transformed-sales-data'
    output_file = 'combined_transformed_data.csv'

    silver_transformation(input_bucket, input_file, output_bucket, output_file)
