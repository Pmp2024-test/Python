from sqlalchemy import create_engine
from sqlalchemy import create_engine, text


db_connection_string = "postgresql://qa:skyqa@5.101.50.27:5432/x_clients"
db = create_engine(db_connection_string)


def test_db_connection():
	names = db.table_names()
	assert names[1] == 'company'
	

def test_select():
    rows = db.execute("SELECT * FROM company").fetchall()
    print(rows)
    row1 = rows[0]

    assert row1[0] == 1
    assert row1["name"] == "QA Студия 'ТестировщикЪ'"

    
def test_select_1_row():
    sql_statement = text("SELECT * FROM company WHERE id = :company_id")
    rows = db.execute(sql_statement, company_id = 1).fetchall()

    assert len(rows) == 1
    assert rows[0]["name"] == "QA Студия 'ТестировщикЪ'"

    
def test_select_1_row_with_two_filters():
    sql_statement = text("SELECT * FROM company "
                       "WHERE \"is_active\" = :is_active AND id >= :id")
    rows = db.execute(sql_statement, id = 10, is_active = True).fetchall()

    assert len(rows) == 2

def test_insert():
    sql = text("INSERT INTO company(\"name\") VALUES (:new_name)")
    rows = db.execute(sql, new_name = 'Skypro')

def test_update():
    sql = text("UPDATE company SET description = :descr WHERE id = :id")
    rows = db.execute(sql, descr = 'New descr', id = 10)

def test_delete():
    sql = text("DELETE FROM company WHERE id = :id")
    rows = db.execute(sql, id = 10)
