import json
import sqlite3
from pathlib import Path

from app.core.config import settings


BASE_DIR = Path(__file__).resolve().parents[2]


def db_path() -> Path:
    value = settings.DATABASE_URL
    if value.startswith("sqlite:///"):
        value = value.replace("sqlite:///", "", 1)
    path = Path(value)
    if not path.is_absolute():
        path = BASE_DIR / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_connection():
    connection = sqlite3.connect(db_path())
    connection.row_factory = sqlite3.Row
    return connection


categories = [
    ("Treadmills", "treadmills", "Running machines for home and commercial training.", "https://images.unsplash.com/photo-1538805060514-97d9cc17730c?auto=format&fit=crop&w=1000&q=85"),
    ("Bikes", "exercise-bikes", "Connected cycling, ride classes and indoor endurance.", "https://images.unsplash.com/photo-1594737625785-a6cbdabd333c?auto=format&fit=crop&w=1000&q=85"),
    ("Ellipticals", "ellipticals", "Low impact cardio with immersive digital programs.", "https://images.unsplash.com/photo-1571019613914-85f342c6a11e?auto=format&fit=crop&w=1000&q=85"),
    ("Rower", "rower", "Total body rowing experience for performance users.", "https://images.unsplash.com/photo-1599058917212-d750089bc07e?auto=format&fit=crop&w=1000&q=85"),
    ("Multi Gyms", "multi-gyms", "Compact full body strength stations.", "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?auto=format&fit=crop&w=1000&q=85"),
    ("Benches", "benches", "Stable workout benches for every strength setup.", "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?auto=format&fit=crop&w=1000&q=85"),
]

products = [
    ("Technogym MyRun", "technogym-myrun", "Treadmills", "INR 4,00,000", 400000, "Home bestseller", "Compact connected treadmill with guided running and refined design.", "Compact connected treadmill.", "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&w=1200&q=85", ["Compact footprint", "Connected app training", "Quiet home operation", "Premium display support"], 1),
    ("Run Personal", "run-personal", "Treadmills", "INR 8,90,000", 890000, "Designer line", "Luxury treadmill for villas, suites and high-end training rooms.", "Luxury treadmill.", "https://images.unsplash.com/photo-1571019613914-85f342c6a11e?auto=format&fit=crop&w=1200&q=85", ["Large running surface", "Luxury finish", "Entertainment ready", "Professional motor"], 1),
    ("Skillrun", "skillrun", "Treadmills", "Request price", 0, "Commercial", "Performance treadmill concept for athletic and club environments.", "Performance treadmill.", "https://images.unsplash.com/photo-1538805060514-97d9cc17730c?auto=format&fit=crop&w=1200&q=85", ["Athletic performance", "Commercial grade", "Power training", "Smart console"], 1),
    ("Technogym Bike", "technogym-bike", "Bikes", "INR 4,25,000", 425000, "Connected", "Premium indoor bike with immersive training and sleek home form factor.", "Premium indoor bike.", "https://images.unsplash.com/photo-1594737625785-a6cbdabd333c?auto=format&fit=crop&w=1200&q=85", ["Live workouts", "Silent resistance", "Compact design", "Connected console"], 1),
    ("Technogym Ride", "technogym-ride", "Bikes", "INR 5,25,000", 525000, "Cyclist choice", "Indoor cycling platform built for serious riders and data-led training.", "Indoor cycling platform.", "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1200&q=85", ["Road feel", "Training metrics", "Smart resistance", "Compact footprint"], 1),
    ("Skillrow", "skillrow", "Rower", "INR 4,80,000", 480000, "Full body", "Athletic rowing machine for endurance, strength and total body training.", "Full body rowing machine.", "https://images.unsplash.com/photo-1599058917212-d750089bc07e?auto=format&fit=crop&w=1200&q=85", ["Aquafeel resistance", "Power training", "Compact frame", "Team workouts"], 1),
    ("Technogym Bench", "technogym-bench", "Benches", "INR 1,65,000", 165000, "Home gym essential", "Compact bench with hidden tools for complete functional home training.", "Compact workout bench.", "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?auto=format&fit=crop&w=1200&q=85", ["Integrated tools", "Small footprint", "Full body workouts", "Designer finish"], 1),
    ("Unica Strength", "unica-strength", "Multi Gyms", "INR 7,40,000", 740000, "Strength station", "All-in-one strength station for private homes and premium wellness rooms.", "All-in-one strength station.", "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?auto=format&fit=crop&w=1200&q=85", ["Complete strength", "Luxury finish", "Guided movement", "Small footprint"], 1),
]


def init_db():
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                description TEXT,
                image TEXT,
                isActive INTEGER DEFAULT 1,
                createdAt TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                price TEXT,
                numericPrice INTEGER DEFAULT 0,
                tag TEXT,
                description TEXT,
                shortDescription TEXT,
                image TEXT,
                specs TEXT,
                isFeatured INTEGER DEFAULT 0,
                isActive INTEGER DEFAULT 1,
                createdAt TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullName TEXT NOT NULL,
                emailOrPhone TEXT NOT NULL,
                requirementType TEXT NOT NULL,
                message TEXT,
                status TEXT DEFAULT 'NEW',
                createdAt TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT NOT NULL,
                items TEXT NOT NULL,
                notes TEXT,
                status TEXT DEFAULT 'CREATED',
                createdAt TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        if conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO categories (name, slug, description, image) VALUES (?, ?, ?, ?)",
                categories,
            )

        if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            conn.executemany(
                """
                INSERT INTO products
                (name, slug, category, price, numericPrice, tag, description, shortDescription, image, specs, isFeatured)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [(*item[:-2], json.dumps(item[-2]), item[-1]) for item in products],
            )


def row_to_dict(row):
    data = dict(row)
    if "specs" in data and data["specs"]:
        data["specs"] = json.loads(data["specs"])
    if "isFeatured" in data:
        data["isFeatured"] = bool(data["isFeatured"])
    if "isActive" in data:
        data["isActive"] = bool(data["isActive"])
    return data
