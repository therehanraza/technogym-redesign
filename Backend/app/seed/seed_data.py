from app.db.sqlite import init_db


def main():
    init_db()
    print("SQLite database initialized with Technogym catalog data.")


if __name__ == "__main__":
    main()
