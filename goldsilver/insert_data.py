import mysql.connector
import json

# Define your MySQL connection parameters
db_config = {
    # 'host': 'localhost',
    # 'user': 'WebSilverGold',
    # 'password': 'ZNu6W7uEm99Y3VdGLXjN',
    # 'database': 'silvergoldprice'
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'goldnew',
}

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Read JSON data from file
with open('jm.json', 'r', encoding='utf-8') as file:
    products_data = json.load(file)

# Define SQL query
sql = '''
INSERT INTO Latestgoldsilver (
    unique_id_for_common_products,
    product_name,
    unique_short_name,
    product_url,
    product_category,
    product_specifications,
    product_image,
    product_description,
    product_year,
    product_type,
    product_weight,
    product_website_image,
    scrap_from,
    sku,
    price
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
'''

# Iterate over each product and insert into the table
for product in products_data:
    try:
        cursor.execute(sql, (
            '',  # unique_id_for_common_products
            product.get('product_name', ''),
            '',  # unique_short_name
            product.get('product_url', ''),
            product.get('product_category', ''),
            product.get('product_specifications', ''),
            product.get('product_image', ''),
            product.get('product_description', ''),
            product.get('product_year', ''),
            product.get('product_type', ''),
            product.get('product_weight', ''),
            product.get('product_website_image', ''),
            product.get('scrap_from', ''),
            product.get('sku', ''),
            product.get('price', '')
        ))
        connection.commit()
        print("Record inserted successfully")
    except mysql.connector.Error as error:
        print(f"Failed to insert record into MySQL table: {error}")

# Close connection
cursor.close()
connection.close()

