class Config:
    # SQLALCHEMY_DATABASE_URI = (
    #     "mssql+pyodbc://@.\\SQLEXPRESS/HospitalDB_2?"
    #     "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    # )
    SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://@localhost\\MSSQLSERVER01/HospitalDB_2?"
    "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    # SECRET_KEY