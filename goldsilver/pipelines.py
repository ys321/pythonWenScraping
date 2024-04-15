import mysql.connector

class GoldsilverPipeline:
    def __init__(self):
        # Update these values with your actual database credentials
        db_params = {
            # 'host': 'localhost',
            # 'user': 'WebSilverGold',
            # 'password': 'ZNu6W7uEm99Y3VdGLXjN',
            # 'database': 'silvergoldprice',
            # 'port': '3306',  # Change this if your MySQL server uses a different port
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'pygold',
            'port': '3306',
        }

        self.connection = mysql.connector.connect(**db_params)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        if self.connection:
            self.connection.commit()  # Commit any pending changes
            self.connection.close()

    def process_item(self, item, spider):
        sql = """
            INSERT INTO goldsilver (
                product_name,
                product_url,
                product_category,
                product_specifications,
                product_image,
                product_description,
                sku,
                price
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            item.get("product_name"),
            item.get("product_url"),
            item.get("product_category"),
            item.get("product_specifications"),
            item.get("product_image"),
            item.get("product_description"),
            item.get("sku"),
            item.get("price")
        )

        try:
            self.cursor.execute(sql, values)
            self.connection.commit()  # Commit the transaction

        except Exception as e:
            print(f"Error inserting item into database: {e}")
            self.connection.rollback()  # Rollback the transaction

        return item

