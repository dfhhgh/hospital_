class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:yugi2017@host.docker.internal:3306/HospitalDB"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    # SECRET_KEY