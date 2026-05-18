from app.db.store import init_storage, using_mongo


def main():
    init_storage()
    database = "MongoDB" if using_mongo() else "SQLite"
    print(f"{database} database initialized with Technogym catalog data.")


if __name__ == "__main__":
    main()
