import wrds
db = wrds.Connection()
print(db.describe_table(library='optionm', table = 'opprcd2022')['name'])