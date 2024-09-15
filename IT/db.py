import json
import os
from uuid import uuid4
from validator import TypeValidator

class DB:
    def __init__(self):
        self.base_dir = os.getcwd()
        self.ensure_directory(self.base_dir)

    def ensure_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def create_table(self, table_name):
        table_path = os.path.join(self.base_dir, f"{table_name}.json")
        if os.path.exists(table_path):
            raise ValueError(f"Table '{table_name}' already exists.")
        
        # Створюємо пусту таблицю з полем id
        with open(table_path, 'w') as file:
            json.dump([], file, indent=4)

    def add_field(self, table_name, field_name, field_type):
        valid_types = ['integer', 'real', 'char', 'string']
        if field_type not in valid_types:
            raise ValueError(f"Field type '{field_type}' is not valid.")
        
        table_path = os.path.join(self.base_dir, f"{table_name}.json")
        if not os.path.exists(table_path):
            raise ValueError(f"Table '{table_name}' does not exist.")
        
        with open(table_path, 'r') as file:
            rows = json.load(file)
        
        for row in rows:
            row[field_name] = None
        
        with open(table_path, 'w') as file:
            json.dump(rows, file, indent=4)

    def insert_row(self, table_name, row_data):
        table_path = os.path.join(self.base_dir, f"{table_name}.json")
        if not os.path.exists(table_path):
            raise ValueError(f"Table '{table_name}' does not exist.")
        
        with open(table_path, 'r') as file:
            rows = json.load(file)
        
        # Перевіряємо кожне поле на відповідність типу
        for field, value in row_data.items():
            for existing_row in rows:
                if field in existing_row:
                    field_type = type(existing_row[field]).__name__
                    if not TypeValidator.validate(value, field_type):
                        raise ValueError(f"Value '{value}' is not valid for field '{field}' of type '{field_type}'")
        
        row_data['id'] = str(uuid4())
        rows.append(row_data)
        
        with open(table_path, 'w') as file:
            json.dump(rows, file, indent=4)

    def load_table(self, table_name):
        table_path = os.path.join(self.base_dir, f"{table_name}.json")
        if os.path.exists(table_path):
            with open(table_path, 'r') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(f"Table '{table_name}' does not exist.")
            
    def delete_table(self, table_name):
        table_path = os.path.join(self.base_dir, f"{table_name}.json")
        if os.path.exists(table_path):
            os.remove(table_path)
        else:
            raise FileNotFoundError(f"Table '{table_name}' does not exist.")
        
    def list_tables(self):
        return [f[:-5] for f in os.listdir(self.base_dir) if f.endswith('.json')]
    
    def delete_row(self, table_name, row_id):
        table_path = os.path.join(self.base_dir, f"{table_name}.json")
        if not os.path.exists(table_path):
            raise FileNotFoundError(f"Table '{table_name}' does not exist.")
        
        with open(table_path, 'r') as file:
            rows = json.load(file)
        
        rows = [row for row in rows if row['id'] != row_id]
        
        with open(table_path, 'w') as file:
            json.dump(rows, file, indent=4)
    
    def rename_table(self, old_name, new_name):
        old_table_path = os.path.join(self.base_dir, f"{old_name}.json")
        new_table_path = os.path.join(self.base_dir, f"{new_name}.json")

        if not os.path.exists(old_table_path):
            raise FileNotFoundError(f"Table '{old_name}' does not exist.")
        
        if os.path.exists(new_table_path):
            raise ValueError(f"Table with name {new_name} already exists.")
        
        os.rename(old_table_path, new_table_path)



# # Приклад використання
# db = SimpleDB()
# db.create_table("users")
# db.add_field("users", "username", "string")
# db.add_field("users", "email", "string")

# # Додаємо новий рядок
# db.insert_row("users", {"username": "alice", "email": "b@g.com"})
# db.insert_row("users", {"username": "bob", "email": "w@g.com"})