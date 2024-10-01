import pandas as pd

# Load CSV files into DataFrames
df_product = pd.read_csv('Product_Dim.csv')
df_customer = pd.read_csv('Customer_Dim.csv')
df_transaction = pd.read_csv('Transaction_Dim.csv')
df_fact = pd.read_csv('Fact_Table.csv')

# Inspect the data (optional)
#print(df_product.head())
#print(df_customer.head())
#print(df_transaction.head())
#print(df_fact.head())

# Merge/join the fact table with the product dimension table
df_merged = pd.merge(df_fact, df_product, on='ProductID', how='left')

# Merge the resulting table with the customer dimension table
df_merged = pd.merge(df_merged, df_customer, on='CustomerID', how='left')

# Merge the resulting table with the transaction dimension table
df_merged = pd.merge(df_merged, df_transaction, on='TransactionID', how='left')

# Save the final merged DataFrame to a CSV file
df_merged.to_csv('all_sales_data_combined.csv', index=False)

# Inspect the final merged data (optional)
#print(df_merged.head())
