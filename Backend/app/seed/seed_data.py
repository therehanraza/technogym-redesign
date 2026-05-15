from app.db.sqlite import init_db


def main():
    init_db()
    print("SQLite database initialized with sample Technogym data.")


if __name__ == "__main__":
    main()
