from app import db, create_app


if __name__ == "__main__":
    # db.drop_all(app=create_app())
    db.create_all(app=create_app())
