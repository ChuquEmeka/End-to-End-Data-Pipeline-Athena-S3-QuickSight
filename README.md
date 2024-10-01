# EmekaMarkt E2E Data Project

## Project Overview

The **EmekaMarkt E2E Data Project** is an end-to-end data pipeline project that demonstrates cloud-based data engineering, ETL processes, and business intelligence reporting using AWS. The project focuses on transforming e-commerce sales data and generating insightful reports in AWS QuickSight, while adhering to AWS Free Tier limits.

### Key Components

1. **Data Generation**: Simulated e-commerce sales data is generated, encompassing sales transactions enriched with product information, customer details, promotions, shipping methods, and reviews.
2. **ETL Pipeline**: A robust ETL pipeline is established to extract, transform, and load data.
3. **Data Storage**: Raw and transformed data is stored in Amazon S3 buckets.
4. **Unit Testing**: Automated unit tests validate the transformation logic before deploying to production.
5. **CI/CD Pipeline**: Continuous integration and deployment are implemented using GitHub Actions, ensuring code quality and automated deployments.

## Project Structure

EmekaMarkt-E2E-DataProject/ ├── unit_test_folder/ │ ├── customer_dim.csv │ ├── fact_sales.csv │ ├── location_dim.csv │ ├── product_dim.csv │ ├── promotion_dim.csv │ ├── raw_sales_data.csv │ ├── review_dim.csv │ └── shipping_dim.csv ├── unused codes/ │ ├── all_sales_data.py │ ├── create_sample_sales_dataset.py │ ├── raw.py │ ├── silver_transformation.py │ └── transformation_code.py ├── output/ │ ├── customer_dim.csv │ ├── fact_sales.csv │ ├── location_dim.csv │ ├── product_dim.csv │ ├── promotion_dim.csv │ ├── review_dim.csv │ └── shipping_dim.csv ├── requirements.txt ├── sales_raw_data_creation.py ├── sample_raw_sales_data.csv ├── silver_transformed_all.py ├── transformation_unit_test.py └── .github/ └── workflows/ └── ci_cd_pipeline.yml


