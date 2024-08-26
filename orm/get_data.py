import sqlite3
from .settings import DATABASE_NAME



class GetData:

    @staticmethod
    def get_data(table_name: str, fields: list):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        all_fields = ", ".join(fields)

        cursor.execute(f"""
            SELECT {all_fields} FROM {table_name};
        """)
        print("Operation Completed..Status..Ok...")
        
        rows = cursor.fetchall()     
        conn.close()
        return rows
    
    
    @staticmethod
    def get_one_or_404(table_name: str, fields: tuple, pk=None):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        row = None
        try:
            fields_str = ", ".join(fields)
            
            cursor.execute(f"SELECT {fields_str} FROM {table_name} WHERE id=?", (pk,))
            row = cursor.fetchone()
            if row:
                print('Operation Complete.....Ok.')
            else:
                print(f"No record found for id={pk}")

        except Exception as e:
            print(f'Error: {str(e)}')

        finally:
            conn.close()
        
        return row


