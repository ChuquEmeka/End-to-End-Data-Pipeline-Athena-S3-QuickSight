import pandas as pd
import json

# Load the CSV with the relational data
file_path = 'sales_data_combined.csv'  # Update this to your raw data file
df = pd.read_csv(file_path)

# Print the columns of the DataFrame to debug
print("Columns in DataFrame:", df.columns)

# Extract the JSON data into a separate DataFrame
if 'RelationalData' in df.columns:
    df['RelationalData'] = df['RelationalData'].apply(json.loads)  # Load JSON strings into dict
    relational_data = pd.json_normalize(df['RelationalData'])  # Normalize the JSON data
else:
    print("Column 'RelationalData' not found. Please check the CSV file.")
    exit()

# Check the normalized data columns
print("Normalized Data Columns:", relational_data.columns)

# Extracting Product Dimension Table excluding UnitCost and Supplier
df_product = relational_data[['Product.ProductID', 'Product.ProductName', 'Product.Category']].drop_duplicates().reset_index(drop=True)
df_product.columns = ['ProductID', 'ProductName', 'Category']  # Renaming columns

# Extracting Customer Dimension Table
df_customer = relational_data[['Customer.CustomerID', 'Customer.CustomerName', 'Customer.Region']].drop_duplicates().reset_index(drop=True)
df_customer.columns = ['CustomerID', 'CustomerName', 'Region']  # Renaming columns

# Creating a mapping of SaleID to ProductID and CustomerID
mapping_df = relational_data[['Sale.SaleID', 'Product.ProductID', 'Customer.CustomerID']].copy()
mapping_df.columns = ['TransactionID', 'ProductID', 'CustomerID']

# Extracting the Transaction Dimension Table
df_transaction = relational_data[['Sale.SaleID', 'Sale.PaymentMethod']].drop_duplicates().reset_index(drop=True)
df_transaction.columns = ['TransactionID', 'PaymentMethod']  # Renaming columns

# Creating the Fact table with all relevant fields including UnitCost
df_fact = relational_data[['Sale.SaleID', 'Sale.Quantity', 'Sale.FinalPrice', 'Sale.Date', 
                           'Sale.ShippingCost', 'Sale.Discount', 'Product.UnitCost']].copy()
df_fact.columns = ['TransactionID', 'Quantity', 'FinalPrice', 'TransactionDate', 
                   'ShippingCost', 'Discount', 'UnitCost']  # Renaming columns

# Merge to get the correct ProductID and CustomerID based on TransactionID
df_fact = df_fact.merge(mapping_df, on='TransactionID', how='left')  # Join with mapping_df to get ProductID and CustomerID

# Reorder the fact table columns
df_fact = df_fact[['TransactionID', 'ProductID', 'CustomerID', 'Quantity', 
                   'FinalPrice', 'TransactionDate', 'ShippingCost', 'Discount', 'UnitCost']]

# Saving each table to CSV in the same directory
df_product.to_csv('Product_Dim.csv', index=False)
df_customer.to_csv('Customer_Dim.csv', index=False)
df_transaction.to_csv('Transaction_Dim.csv', index=False)
df_fact.to_csv('Fact_Table.csv', index=False)

print("Star schema dimensional tables and Fact table saved successfully!")
