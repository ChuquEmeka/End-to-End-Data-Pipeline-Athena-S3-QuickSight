
import sys
import os
# Adding the root project directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from jobs.tasks.raw_data_transformation.silver_transformed_all import transform_sales_data

import pandas as pd
import json
import os
import unittest
# from silver_transformed_all import transform_sales_data
from unittest.mock import patch
from io import StringIO  # Import StringIO

class TestSalesTransformation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a mock raw sales data for testing
        cls.raw_data = {
            'SaleID': [1, 2],
            'Product': [
                json.dumps([{'ProductID': 1, 'ProductName': 'Phone', 'Category': 'Electronics', 'UnitCost': 300, 'UnitPrice': 600}]),
                json.dumps([{'ProductID': 2, 'ProductName': 'Laptop', 'Category': 'Computers', 'UnitCost': 800, 'UnitPrice': 1200}])
            ],
            'Customer': [
                json.dumps([{'CustomerID': 1, 'CustomerName': 'Emma Watson', 'Email': 'emma.watson@example.com', 'PhoneNumber': '+49-1234567890', 'LoyaltyStatus': 'Gold'}]),
                json.dumps([{'CustomerID': 2, 'CustomerName': 'Dwayne Johnson', 'Email': 'dwayne.johnson@example.com', 'PhoneNumber': '+49-0987654321', 'LoyaltyStatus': 'Silver'}])
            ],
            'Quantity': [2, 1],
            'Date': ['2024-09-30T12:00:00', '2024-09-30T13:00:00'],
            'Location': [
                json.dumps([{'LocationID': 1, 'Country': 'Germany', 'City': 'Berlin', 'PostalCode': 10115, 'Region': 'Europe'}]),
                json.dumps([{'LocationID': 1, 'Country': 'Germany', 'City': 'Berlin', 'PostalCode': 10115, 'Region': 'Europe'}])
            ],
            'PaymentID': [1, 2],
            'Shipping': [
                json.dumps([{'ShippingID': 1, 'Method': 'International', 'Cost': 48.45527535}]),
                json.dumps([{'ShippingID': 2, 'Method': 'Express', 'Cost': 15.63674313}])
            ],
            'Promotion': [
                json.dumps([{'PromotionID': 1, 'Discount': 10}]),
                json.dumps([{'PromotionID': 1, 'Discount': 5}])
            ],
            'Review': [
                json.dumps([{'ReviewID': 1, 'Rating': 5, 'Comment': 'Excellent!'}]),
                json.dumps([{'ReviewID': 2, 'Rating': 4, 'Comment': 'Very good.'}])
            ],
        }

        cls.output_dir = cls.output_dir = 'unit_test/data'  # Changed to 'unit_test_folder'
        os.makedirs(cls.output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

        # Save raw sales data in the output directory for transformation
        cls.df_raw = pd.DataFrame(cls.raw_data)

    def test_transform_sales_data(self):
        # Call the transformation function with the raw DataFrame
        transform_sales_data(self.df_raw)

        # Load the resulting tables from the test output directory
        df_product = pd.read_csv(os.path.join(self.output_dir, 'product_dim.csv'))
        df_customer = pd.read_csv(os.path.join(self.output_dir, 'customer_dim.csv'))
        df_location = pd.read_csv(os.path.join(self.output_dir, 'location_dim.csv'))
        df_promotion = pd.read_csv(os.path.join(self.output_dir, 'promotion_dim.csv'))
        df_shipping = pd.read_csv(os.path.join(self.output_dir, 'shipping_dim.csv'))
        df_review = pd.read_csv(os.path.join(self.output_dir, 'review_dim.csv'))
        df_fact_sales = pd.read_csv(os.path.join(self.output_dir, 'fact_sales.csv'))

        # Test the dimensions and fact table counts
        self.assertEqual(df_product.shape[0], 2)
        self.assertEqual(df_customer.shape[0], 2)
        self.assertEqual(df_location.shape[0], 1)
        self.assertEqual(df_promotion.shape[0], 1)
        self.assertEqual(df_shipping.shape[0], 2)
        self.assertEqual(df_review.shape[0], 2)
        self.assertEqual(df_fact_sales.shape[0], 2)

        # Test all values in the dataframes
        pd.testing.assert_frame_equal(
            df_product,
            pd.DataFrame({
                'ProductID': [1, 2],
                'ProductName': ['Phone', 'Laptop'],
                'Category': ['Electronics', 'Computers'],
                'UnitCost': [300, 800],
                'UnitPrice': [600, 1200]
            })
        )

        pd.testing.assert_frame_equal(
            df_customer,
            pd.DataFrame({
                'CustomerID': [1, 2],
                'CustomerName': ['Emma Watson', 'Dwayne Johnson'],
                'Email': ['emma.watson@example.com', 'dwayne.johnson@example.com'],
                'PhoneNumber': ['+49-1234567890', '+49-0987654321'],
                'LoyaltyStatus': ['Gold', 'Silver']
            })
        )

        pd.testing.assert_frame_equal(
            df_location,
            pd.DataFrame({
                'LocationID': [1],
                'Country': ['Germany'],
                'City': ['Berlin'],
                'PostalCode': [10115],
                'Region': ['Europe']
            })
        )

        pd.testing.assert_frame_equal(
            df_promotion,
            pd.DataFrame({
                'PromotionID': [1],
                'Discount': [10]  # Ensure this matches the expected output
            })
        )

        pd.testing.assert_frame_equal(
            df_shipping,
            pd.DataFrame({
                'ShippingID': [1, 2],
                'Method': ['International', 'Express'],
                'Cost': [48.45527535, 15.63674313]
            })
        )

        pd.testing.assert_frame_equal(
            df_review,
            pd.DataFrame({
                'ReviewID': [1, 2],
                'Rating': [5, 4],
                'Comment': ['Excellent!', 'Very good.']
            })
        )

        pd.testing.assert_frame_equal(
            df_fact_sales,
            pd.DataFrame({
                'SaleID': [1, 2],
                'Quantity': [2, 1],
                'Date': ['2024-09-30T12:00:00', '2024-09-30T13:00:00'],
                'PaymentID': [1, 2],
                'ShippingID': [1, 2],
                'PromotionID': [1, 1],
                'ReviewID': [1, 2],
                'ProductID': [1, 2],
                'LocationID': [1, 1],
                'CustomerID': [1, 2],
            })
        )

if __name__ == '__main__':
    unittest.main()

