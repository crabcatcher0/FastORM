import sqlite3
from .settings import DATABASE_NAME



class CrabModel:
    """
    :: Base class for creating database tables with auto-incremented primary keys.
    - Automatically creates a table with a primary key column named 'id' that auto-increments.
    - Foreign Keys are if given it creates the table with it too.
    - Checks if the table already exists if it exist it skips creation.
    - Constructs the column and optional foreign key constraints.
    """

    @classmethod
    def table(cls, table_name: str, column: dict, foreign_keys:list = None):
        database_name = DATABASE_NAME
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';
        """)

        result = cursor.fetchone()
        if result:
            print(f"Table '{table_name}' already exists. Skipping...")
        else:
            colmn_def = ", ".join([f"{col} {dtype}" for col, dtype in column.items()])

            fk_constraints = ""
            if foreign_keys:
                fk_constraints = ", " + ", ".join(foreign_keys)
            try:
                cursor.execute(f"""
                    CREATE TABLE {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {colmn_def}
                    {fk_constraints}
                    );
                """)
                print(f"Table '{table_name}' created.\nColumn: {', '.join(column.keys())} created.")
            except (sqlite3.OperationalError, Exception) as e:
                print(f'Error: {str(e)}')

        conn.commit()
        conn.close()



    @classmethod
    def add_column(cls, table_name: str, column_name: str, data_type: str):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute(f"""
            PRAGMA table_info({table_name});
        """)
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]

        if column_name in column_names:
            print(f"Column '{column_name}' already exists... Skipping...")
        else:
            try:
                cursor.execute(f"""
                    ALTER TABLE {table_name}
                    ADD COLUMN {column_name} {data_type};
            """)
                print(f"Column '{column_name}' created.")
            except Exception as e:
                print(f'Error: {str(e)}')

        conn.commit()
        conn.close()



    @classmethod
    def add_data(cls, column: dict):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        columns = ', '.join(column.keys())
        placeholders = ', '.join(['?' for _ in column.values()])
        values = tuple(column.values())
        table_name = cls.__name__.lower()
        
        try:
            cursor.execute(f"""
                INSERT INTO {table_name} ({columns}) VALUES ({placeholders})
            """, values)

            print(f'Data added to {table_name}....')
            
        except Exception as e:
            print(f'Error: {str(e)}')

        conn.commit()
        conn.close()

    
    @classmethod
    def delete(cls, pk=int):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        table_name = cls.__name__.lower()
        try:
            cursor.execute(f"""
                DELETE FROM {table_name} WHERE id = ?;
                """, (pk,))
            print(f"Data with id={pk} deleted....Ok..")

        except Exception as e:
            print(f"Error: {str(e)}")

        conn.commit()
        conn.close()



    @classmethod
    def update(cls, pk: int, **columns):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        table_name = cls.__name__.lower()
        set_clause = ", ".join([f"{col} = ?" for col in columns.keys()])
        data = list(columns.values())
        data.append(pk)

        try:
            cursor.execute(f"""
                UPDATE {table_name}
                SET {set_clause}
                WHERE id=?
            """, data)
            print(f"Record with id={pk} updated successfully.")

        except Exception as e:
            print(f'Error with update: {str(e)}')

        finally:
            cursor.fetchall()
            conn.close()



    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.table_name = cls.__name__.lower()
        cls.model = cls.__name__.lower()

        cls.table(
            table_name = cls.table_name,
            column = cls._column
        )


class ForeignKey:
    """
    Utility class for creating foreign key constraints in table definitions.
    - create_foreignkey(field_name: str, referenced_table: str):
        generates a foreign key constraint for a column.
    - parameters:
        - field_name (str): name of the column in the current table that will be a foreign key.
        - model (str): the name of the table that contains the primary key being referenced.
    """
    
    @staticmethod
    def create_foreignkey(field_name: str, model: str):
        return f"FOREIGN KEY ({field_name}) REFERENCES {model}(id)"

