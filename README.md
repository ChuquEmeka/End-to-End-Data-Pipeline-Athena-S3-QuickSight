# EmekaMarkt E2E Data Project

## Project Overview

The **EmekaMarkt E2E Data Project** is an end-to-end data pipeline project that demonstrates cloud-based data engineering, ETL processes, and business intelligence reporting using AWS. The project focuses on transforming e-commerce sales data and generating insightful reports in AWS QuickSight, while adhering to AWS Free Tier limits.  


  
### Explanation of Star Schema and Entity-Relationship Diagram

In my EmekaMarkt E2E Data Project, I adopted the **star schema** to effectively model my data for a few key reasons.

The star schema is a type of database schema that organizes data into fact and dimension tables. The **fact table**, which represents the core transactional data, is positioned at the center, while the surrounding **dimension tables** contain descriptive attributes related to the facts. For example, my fact table, **Fact Sales**, includes metrics like quantity sold and payment details, while dimension tables like **Customer Dim**, **Product Dim**, and **Location Dim** provide additional context, such as customer information, product specifications, and location details.

The primary advantages of using a star schema are:

1. **Simplicity and Clarity**: The star schema is easy to understand and navigate. The straightforward relationship between the fact table and the dimension tables makes it intuitive for users and analysts to query data and generate reports.

2. **Performance Optimization**: This schema design allows for faster query performance. Since dimension tables are denormalized, they reduce the number of joins needed when querying the data, which significantly speeds up retrieval times.

3. **Enhanced Reporting**: With a star schema, it becomes simpler to create complex reports and visualizations. For my project, this structure facilitates efficient data analysis, especially when I connect the transformed data to AWS QuickSight for business insights.

I also created an **Entity-Relationship Diagram (ERD)** to visually represent the relationships between the different entities in my data model. The ERD provides a clear overview of how the fact table interacts with the various dimension tables through foreign key relationships. This visual aid not only helps in understanding the data model but also serves as documentation for future reference.

By adopting the star schema and ERD, I can ensure that my data model is both efficient and effective for analysis, allowing me to derive valuable insights from the e-commerce sales data while preparing it for potential future needs.  
![ER](images/ER.png)


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


