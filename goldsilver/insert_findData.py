import mysql.connector
import json

# Define your MySQL connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'gold'
}

# Connect to the database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Read JSON data from file
# with open('jmbullion-today.json', 'r', encoding='utf-8') as file:
with open('find09042024.json', 'r', encoding='utf-8') as file:
    products_data = json.load(file)

# Define SQL query
sql = '''
INSERT INTO findbull (
    
    company_name,
    product_name,
    head,
    dealer,
    price,
    dealer_premium,
    link,
    image_src,
    image_path,
    weight,
    type,
    metal,
    category,
    Collections
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
'''

# Iterate over each product and insert into the table
for product in products_data:
    try:
        cursor.execute(sql, (
            product.get('company_name', ''),
            product.get('product_name', ''),
            product.get('head', ''),
            product.get('dealer', ''),
            product.get('price', ''),
            product.get('dealer_premium', ''),
            product.get('link', ''),
            product.get('image_src', ''),
            product.get('image_path', ''),
            product.get('weight', ''),
            product.get('type', ''),
            product.get('metal', ''),
            product.get('category', ''),
            product.get('Collections', ''),

        ))
        connection.commit()
        print("Record inserted successfully")
    except mysql.connector.Error as error:
        print(f"Failed to insert record into MySQL table: {error}")

# Close connection
cursor.close()
connection.close()

