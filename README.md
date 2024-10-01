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
EmekaMarkt-E2E-DataProject/  
├── unit_test_folder/  
│   ├── customer_dim.csv  
│   ├── fact_sales.csv  
│   ├── location_dim.csv  
│   ├── product_dim.csv  
│   ├── promotion_dim.csv  
│   ├── raw_sales_data.csv  
│   ├── review_dim.csv  
│   └── shipping_dim.csv  
├── unused codes/  
│   ├── all_sales_data.py  
│   ├── create_sample_sales_dataset.py  
│   ├── raw.py  
│   ├── silver_transformation.py  
│   └── transformation_code.py  
├── output/  
│   ├── customer_dim.csv  
│   ├── fact_sales.csv  
│   ├── location_dim.csv  
│   ├── product_dim.csv  
│   ├── promotion_dim.csv  
│   ├── review_dim.csv  
│   └── shipping_dim.csv  
├── requirements.txt  
├── sales_raw_data_creation.py  
├── sample_raw_sales_data.csv  
├── silver_transformed_all.py  
├── transformation_unit_test.py  
└── .github/  
    └── workflows/  
        └── ci_cd_pipeline.yml  


## Workflow

1. **Data Generation**: 
   - E-commerce data is simulated and saved as `raw_sales_data.csv`.
   - Data includes dimensions such as customers, products, promotions, and shipping.

2. **ETL Pipeline**:
   - **Transformation Logic**: Implemented in `silver_transformed_all.py`, this script processes raw data and generates cleaned dimension and fact tables.
   - **Unit Testing**: `transformation_unit_test.py` ensures the transformation logic is correct.

3. **Data Storage**:
   - Raw data is stored in the S3 bucket `emeka-market-raw-sales-data`.
   - Transformed data is also uploaded to the S3 bucket after successful transformations.

4. **CI/CD Pipeline**: Managed through GitHub Actions:
   - On each push or pull request to the `master` branch, the following steps are executed:
     - Code is checked out from the repository.
     - Python environment is set up with dependencies installed from `requirements.txt`.
     - Unit tests are executed. If they pass, the transformation script is run, and the output is saved to S3.
     - Glue job execution is planned for future implementation.

## CI/CD Pipeline (GitHub Actions)

The CI/CD pipeline is defined in `.github/workflows/ci_cd_pipeline.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - master
  pull_request:
    branches:
      - master

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt  

      - name: Install AWS CLI
        run: |
          pip install awscli

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1 

      - name: Run unit tests
        run: |
          python transformation_unit_test.py  

      - name: Apply transformation on Production Data and save Dimension and Fact Tables to S3
        if: success()  
        run: |
          python silver_transformed_all.py 

      - name: Also Run silver_transformation
        if: success()  
        run: |
          python "unused codes/silver_transformation.py"

