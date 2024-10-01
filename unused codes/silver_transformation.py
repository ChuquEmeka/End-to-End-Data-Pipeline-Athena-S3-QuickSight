import pandas as pd
import json

def silver_transformation(input_file, output_file):
    # Load raw sales data
    df_raw = pd.read_csv(input_file)

    # Function to load JSON objects from string
    def json_to_dataframe(json_str):
        json_data = json.loads(json_str)
        return pd.json_normalize(json_data)

    # Explode the JSON columns for each sale
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

    # Save the silver table
    df_sales_expanded.to_csv(output_file, index=False)

    return df_sales_expanded  # Return the expanded DataFrame for testing

silver_transformation('raw_sales_data.csv', 'silver_sales_data.csv')





# import pandas as pd
# import json

# # Load raw sales data
# df_raw = pd.read_csv('raw_sales_data.csv')

# # Function to load JSON objects from string
# def json_to_dataframe(json_str):
#     json_data = json.loads(json_str)
#     return pd.json_normalize(json_data)

# # Explode the JSON columns for each sale
# df_sales_expanded = pd.DataFrame()

# # Exploding Product data
# df_raw['Product'] = df_raw['Product'].apply(lambda x: json.loads(x)[0])
# df_product = pd.json_normalize(df_raw['Product'])
# df_sales_expanded = pd.concat([df_raw, df_product], axis=1)
# df_sales_expanded.drop(columns=['Product'], inplace=True)

# # Exploding Customer data
# df_raw['Customer'] = df_raw['Customer'].apply(lambda x: json.loads(x)[0])
# df_customer = pd.json_normalize(df_raw['Customer'])
# df_sales_expanded = pd.concat([df_sales_expanded, df_customer], axis=1)
# df_sales_expanded.drop(columns=['Customer'], inplace=True)

# # Exploding Location data
# df_raw['Location'] = df_raw['Location'].apply(lambda x: json.loads(x)[0])
# df_location = pd.json_normalize(df_raw['Location'])
# df_sales_expanded = pd.concat([df_sales_expanded, df_location], axis=1)
# df_sales_expanded.drop(columns=['Location'], inplace=True)

# # Exploding Promotion data
# df_raw['Promotion'] = df_raw['Promotion'].apply(lambda x: json.loads(x)[0])
# df_promotion = pd.json_normalize(df_raw['Promotion'])
# df_sales_expanded = pd.concat([df_sales_expanded, df_promotion], axis=1)
# df_sales_expanded.drop(columns=['Promotion'], inplace=True)

# # Exploding Shipping data
# df_raw['Shipping'] = df_raw['Shipping'].apply(lambda x: json.loads(x)[0])
# df_shipping = pd.json_normalize(df_raw['Shipping'])
# df_sales_expanded = pd.concat([df_sales_expanded, df_shipping], axis=1)
# df_sales_expanded.drop(columns=['Shipping'], inplace=True)

# # Exploding Review data
# df_raw['Review'] = df_raw['Review'].apply(lambda x: json.loads(x)[0])
# df_review = pd.json_normalize(df_raw['Review'])
# df_sales_expanded = pd.concat([df_sales_expanded, df_review], axis=1)
# df_sales_expanded.drop(columns=['Review'], inplace=True)

# # Save the silver table
# df_sales_expanded.to_csv('silver_sales_data.csv', index=False)

# # Display sample outputs
# print("Silver Sales Data Sample:")
# print(df_sales_expanded.head())
