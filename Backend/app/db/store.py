from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from app.core.config import settings
from app.db import sqlite

try:
    from bson import ObjectId
    from pymongo import ASCENDING, DESCENDING, MongoClient
    from pymongo.errors import DuplicateKeyError
except ImportError:  # Local SQLite fallback can still run before pymongo is installed.
    ObjectId = None
    ASCENDING = DESCENDING = None
    MongoClient = None
    DuplicateKeyError = Exception


def using_mongo() -> bool:
    return bool(settings.MONGODB_URI.strip())


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _mongo_db():
    if not using_mongo():
        return None
    if MongoClient is None:
        raise RuntimeError("pymongo is required when MONGODB_URI is configured")
    client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    return client[settings.MONGODB_DB_NAME]


DEFAULT_NAVIGATION = [
    {
        "key": "products",
        "label": "Products",
        "to": "/category/all-products",
        "eyebrow": "Products",
        "title": "Explore Products",
        "text": "Discover premium cardio, strength, functional training, and home fitness equipment.",
        "columns": [
            ["All Products", "/category/all-products"],
            ["Shop Home Essentials", "/shop"],
            ["Treadmills", "/category/treadmills"],
            ["Bikes", "/category/exercise-bikes"],
            ["Ellipticals", "/category/ellipticals"],
            ["Rower", "/category/rower"],
            ["Stair Climbers", "/category/stair-climbers"],
            ["Multi Gyms", "/category/multi-gyms"],
            ["Dumbbells & Kettlebells", "/category/free-weights"],
            ["Benches", "/category/benches"],
            ["Barbells & Plates", "/category/free-weights"],
            ["Racks", "/category/multi-gyms"],
        ],
    },
    {
        "key": "home",
        "label": "Home Gym",
        "to": "/home-gym",
        "eyebrow": "Home Gym",
        "title": "Explore Home Gym",
        "text": "Build a personal wellness space with luxury equipment, room planning, and design support.",
        "columns": [
            ["Home Gym", "/home-gym"],
            ["Luxury Home Gym", "/luxury-home-gym"],
            ["Lifestyle Home Gym", "/lifestyle-home-gym"],
            ["Room Planner", "/room-planner"],
            ["Design at Technogym", "/design"],
        ],
    },
    {
        "key": "business",
        "label": "Business",
        "to": "/business",
        "eyebrow": "Business",
        "title": "Explore Business",
        "text": "Create professional fitness spaces for clubs, hotels, workplaces, and medical wellness.",
        "columns": [
            ["Business", "/business"],
            ["Commercial Equipment", "/business-equipment"],
            ["Fitness Clubs", "/business/health-clubs"],
            ["Hotels & Resorts", "/business/hospitality"],
            ["Corporate Wellness", "/business/corporate"],
            ["Medical & Rehab", "/business/medical"],
        ],
    },
    {
        "key": "support",
        "label": "Support",
        "to": "/support",
        "eyebrow": "Support",
        "title": "Explore Support",
        "text": "Get product care, service assistance, technical support, and customer guidance.",
        "columns": [
            ["Support Home", "/support"],
            ["Technogym Care", "/technogym-care"],
            ["Technical Support", "/technical-support"],
            ["Contacts", "/contacts"],
            ["Technogym App", "/technogym-app"],
        ],
    },
    {
        "key": "stories",
        "label": "Stories",
        "to": "/stories",
        "eyebrow": "Stories",
        "title": "Explore Stories",
        "text": "Read insights on wellness, sustainability, training culture, and design.",
        "columns": [
            ["Stories", "/stories"],
            ["Wellness", "/wellness"],
            ["Sustainability", "/sustainability"],
            ["Design", "/design"],
        ],
    },
]


DEFAULT_PAGES = [
    {
        "path": "/",
        "title": "A complete modern Technogym experience.",
        "text": "Home gym, commercial fitness, product discovery, support, stories, and consultation in one refined experience.",
        "eyebrow": "Premium wellness equipment for modern India",
        "image": "https://images.unsplash.com/photo-1605296867304-46d5465a13f1?auto=format&fit=crop&w=1400&q=85",
        "highlights": ["Equipment categories", "Design support", "Business solutions"],
    },
    {
        "path": "/shop",
        "title": "Shop Home Essentials",
        "text": "Curated premium products for modern home wellness.",
        "image": "https://images.unsplash.com/photo-1605296867304-46d5465a13f1?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/home-gym",
        "title": "Home Gym Design",
        "text": "Create a personal training room with premium equipment, layout support and connected workouts.",
        "image": "https://images.unsplash.com/photo-1558611848-73f7eb4001a1?auto=format&fit=crop&w=1400&q=85",
        "sectionTitle": "A personal gym designed around your lifestyle",
        "cards": [
            ["Room fit", "Plan equipment around available space, ceiling height, floor finish and daily movement habits."],
            ["Quiet performance", "Focus on compact, refined products that feel premium inside apartments and private homes."],
            ["Connected training", "Combine cardio, strength and app-led programs so the room supports long-term progress."],
        ],
        "highlights": ["Luxury layouts", "Compact cardio", "Strength zones", "Design consultation"],
    },
    {
        "path": "/luxury-home-gym",
        "title": "Luxury Home Gym",
        "text": "Premium private wellness rooms planned around equipment, interiors and daily training rituals.",
        "image": "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?auto=format&fit=crop&w=1400&q=85",
        "sectionTitle": "Luxury training spaces with a refined finish",
        "cards": [
            ["Premium equipment", "Select cardio and strength pieces that look as good as they perform."],
            ["Interior fit", "Match finishes, footprint and layout to villas, apartments and private rooms."],
            ["Guided setup", "Move from inspiration to a practical room plan and consultation request."],
        ],
        "highlights": ["Private gyms", "Interior planning", "Premium cardio", "Strength design"],
    },
    {
        "path": "/lifestyle-home-gym",
        "title": "Lifestyle Home Gym",
        "text": "Everyday wellness spaces for training, recovery and healthier routines at home.",
        "image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1400&q=85",
        "sectionTitle": "Home wellness that fits the way you live",
        "cards": [
            ["Daily movement", "Build routines around compact equipment and flexible training zones."],
            ["Family friendly", "Plan a space that supports different fitness levels and wellness goals."],
            ["Connected support", "Use digital training and consultation flows to keep progress simple."],
        ],
        "highlights": ["Daily training", "Compact rooms", "Recovery", "Connected fitness"],
    },
    {
        "path": "/room-planner",
        "title": "Room Planner",
        "text": "Create room layouts, add equipment and build your gym concept.",
        "image": "https://images.unsplash.com/photo-1558611848-73f7eb4001a1?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/business",
        "title": "Commercial Gym Machines and Pro Equipment",
        "text": "Solutions for clubs, hotels, corporate wellness, medical and sports facilities.",
        "image": "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?auto=format&fit=crop&w=1400&q=85",
        "sectionTitle": "Professional wellness spaces with measurable impact",
        "cards": [
            ["Facility planning", "Build layouts for hotels, clubs, corporate wellness rooms and medical fitness spaces."],
            ["Member experience", "Create training zones that are easy to navigate, durable and visually consistent."],
            ["Service continuity", "Support equipment choices with maintenance, onboarding and lifecycle planning."],
        ],
        "highlights": ["Health clubs", "Hospitality", "Corporate wellness", "Medical fitness"],
    },
    {
        "path": "/business-equipment",
        "title": "Commercial Equipment",
        "text": "Durable cardio, strength and functional equipment for professional fitness environments.",
        "image": "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?auto=format&fit=crop&w=1400&q=85",
        "sectionTitle": "Equipment built for repeated professional use",
        "cards": [
            ["Cardio floors", "Plan treadmill, bike, rower and elliptical zones for busy facilities."],
            ["Strength areas", "Combine benches, multi gyms and free weights for complete training paths."],
            ["Lifecycle support", "Support purchasing with service, maintenance and upgrade planning."],
        ],
        "highlights": ["Cardio", "Strength", "Functional zones", "Service"],
    },
    {
        "path": "/business/health-clubs",
        "title": "Fitness Clubs",
        "text": "Premium club layouts designed for member experience, durability and training flow.",
        "image": "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/business/hospitality",
        "title": "Hotels & Resorts",
        "text": "Wellness spaces for hospitality properties that want a premium guest fitness experience.",
        "image": "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/business/corporate",
        "title": "Corporate Wellness",
        "text": "Employee wellness rooms and movement spaces for modern workplaces.",
        "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/business/medical",
        "title": "Medical & Rehab",
        "text": "Movement environments for rehabilitation, active ageing and supervised wellness.",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/support",
        "title": "Support",
        "text": "Customer support, technical assistance, e-learning and service flows.",
        "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1400&q=85",
        "sectionTitle": "Support built around your equipment",
        "cards": [
            ["Product care", "Find the right route for maintenance, warranty questions and everyday equipment guidance."],
            ["Technical help", "Organize service requests with useful product, issue and contact details from the start."],
            ["Digital support", "Connect app, account and training service questions with a clear follow-up flow."],
        ],
        "highlights": ["Maintenance", "Warranty guidance", "Technical assistance", "App support"],
    },
    {
        "path": "/technogym-care",
        "title": "Technogym Care",
        "text": "Service and care support for keeping equipment ready for daily training.",
        "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/technical-support",
        "title": "Technical Support",
        "text": "Request product help, technical assistance and next-step service guidance.",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/technogym-app",
        "title": "Technogym App",
        "text": "Connected training, digital services and app-supported wellness journeys.",
        "image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/contacts",
        "title": "Contact Us",
        "text": "Lead form and contact flow for consultation, marketing and technical requests.",
        "image": "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/checkout",
        "title": "Checkout",
        "text": "Modern ecommerce checkout for selected products and consultation-led purchasing.",
        "image": "https://images.unsplash.com/photo-1556742502-ec7c0e9f34b1?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/stories",
        "title": "Stories",
        "text": "Editorial hub for longevity, people, sports, fitness, health, mind and nutrition.",
        "image": "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?auto=format&fit=crop&w=1400&q=85",
        "sectionTitle": "Wellness thinking for better movement",
        "cards": [
            ["Wellness culture", "Explore ideas around movement, longevity, nutrition and everyday performance."],
            ["Design stories", "See how premium equipment and interiors can shape better training environments."],
            ["Sustainability", "Follow product thinking that connects performance, materials and responsible choices."],
        ],
        "highlights": ["Wellness", "Design", "Performance", "Sustainability"],
    },
    {
        "path": "/wellness",
        "title": "Wellness",
        "text": "Movement, recovery, nutrition and mindset content for a more complete wellness lifestyle.",
        "image": "https://images.unsplash.com/photo-1517963879433-6ad2b056d712?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/sustainability",
        "title": "Sustainability",
        "text": "Responsible product thinking across performance, materials and long-term equipment value.",
        "image": "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/design",
        "title": "Design at Technogym",
        "text": "Interior design, premium materials, layouts and design-led wellness experiences.",
        "image": "https://images.unsplash.com/photo-1558611848-73f7eb4001a1?auto=format&fit=crop&w=1400&q=85",
    },
    {
        "path": "/account",
        "title": "My Account",
        "text": "Profile, orders, saved consultations and app-connected preferences.",
        "image": "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?auto=format&fit=crop&w=1400&q=85",
    },
]


def _serialize(document: dict[str, Any]) -> dict[str, Any]:
    data = dict(document)
    if "_id" in data:
        data["id"] = str(data.pop("_id"))
    if "createdAt" in data and isinstance(data["createdAt"], datetime):
        data["createdAt"] = data["createdAt"].isoformat()
    if "updatedAt" in data and isinstance(data["updatedAt"], datetime):
        data["updatedAt"] = data["updatedAt"].isoformat()
    return data


def _id_filter(value: str) -> dict[str, Any]:
    if ObjectId is not None and ObjectId.is_valid(value):
        return {"_id": ObjectId(value)}
    return {"id": value}


def _seed_mongo(db):
    db.categories.create_index([("slug", ASCENDING)], unique=True)
    db.products.create_index([("slug", ASCENDING)], unique=True)
    db.pages.create_index([("path", ASCENDING)], unique=True)
    db.navigation.create_index([("key", ASCENDING)], unique=True)

    if db.categories.count_documents({}) == 0:
        db.categories.insert_many([
            {
                "name": name,
                "slug": slug,
                "description": description,
                "image": image,
                "isActive": True,
                "createdAt": _now(),
            }
            for name, slug, description, image in sqlite.categories
        ])
    if db.products.count_documents({}) == 0:
        db.products.insert_many([
            {
                "name": name,
                "slug": slug,
                "category": category,
                "price": price,
                "numericPrice": numeric_price,
                "tag": tag,
                "description": description,
                "shortDescription": short_description,
                "image": image,
                "specs": specs,
                "isFeatured": bool(is_featured),
                "isActive": True,
                "createdAt": _now(),
            }
            for name, slug, category, price, numeric_price, tag, description, short_description, image, specs, is_featured in sqlite.products
        ])
    for item in DEFAULT_NAVIGATION:
        db.navigation.update_one(
            {"key": item["key"]},
            {"$setOnInsert": {"createdAt": _now()}, "$set": item},
            upsert=True,
        )
    for item in DEFAULT_PAGES:
        db.pages.update_one(
            {"path": item["path"]},
            {"$setOnInsert": {"createdAt": _now()}, "$set": {**item, "isActive": True}},
            upsert=True,
        )


def init_storage():
    if using_mongo():
        _seed_mongo(_mongo_db())
    else:
        sqlite.init_db()


def get_navigation():
    if using_mongo():
        rows = _mongo_db().navigation.find({}).sort("key", ASCENDING)
        data = [_serialize(row) for row in rows]
        return data or DEFAULT_NAVIGATION
    return DEFAULT_NAVIGATION


def get_pages():
    if using_mongo():
        rows = _mongo_db().pages.find({"isActive": {"$ne": False}}).sort("path", ASCENDING)
        data = [_serialize(row) for row in rows]
        return data or DEFAULT_PAGES
    return DEFAULT_PAGES


def get_page_by_path(path: str):
    normalized = path if path.startswith("/") else f"/{path}"
    if using_mongo():
        row = _mongo_db().pages.find_one({"path": normalized, "isActive": {"$ne": False}})
        return _serialize(row) if row else None
    return next((page for page in DEFAULT_PAGES if page["path"] == normalized), None)


def get_categories():
    if using_mongo():
        rows = _mongo_db().categories.find({"isActive": {"$ne": False}}).sort("name", ASCENDING)
        return [_serialize(row) for row in rows]
    with sqlite.get_connection() as conn:
        rows = conn.execute("SELECT * FROM categories WHERE isActive = 1 ORDER BY name").fetchall()
    return [sqlite.row_to_dict(row) for row in rows]


def get_category_by_slug(slug: str):
    if using_mongo():
        row = _mongo_db().categories.find_one({"slug": slug, "isActive": {"$ne": False}})
        return _serialize(row) if row else None
    with sqlite.get_connection() as conn:
        row = conn.execute("SELECT * FROM categories WHERE slug = ? AND isActive = 1", (slug,)).fetchone()
    return sqlite.row_to_dict(row) if row else None


def create_category(data: dict[str, Any]):
    if using_mongo():
        payload = {**data, "isActive": data.get("isActive", True), "createdAt": _now()}
        result = _mongo_db().categories.insert_one(payload)
        return _serialize(_mongo_db().categories.find_one({"_id": result.inserted_id}))
    with sqlite.get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO categories (name, slug, description, image, isActive) VALUES (?, ?, ?, ?, ?)",
            (data["name"], data["slug"], data.get("description", ""), data.get("image", ""), int(data.get("isActive", True))),
        )
        row = conn.execute("SELECT * FROM categories WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return sqlite.row_to_dict(row)


def get_products(category: str | None = None, search: str | None = None, featured: bool | None = None):
    if using_mongo():
        query: dict[str, Any] = {"isActive": {"$ne": False}}
        if category:
            query["category"] = {"$regex": category, "$options": "i"}
        if featured is not None:
            query["isFeatured"] = featured
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"category": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
            ]
        rows = _mongo_db().products.find(query).sort("createdAt", DESCENDING)
        return [_serialize(row) for row in rows]

    clauses = ["isActive = 1"]
    params: list[Any] = []
    if category:
        clauses.append("LOWER(category) LIKE ?")
        params.append(f"%{category.lower()}%")
    if featured is not None:
        clauses.append("isFeatured = ?")
        params.append(int(featured))
    if search:
        clauses.append("(LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(description) LIKE ?)")
        value = f"%{search.lower()}%"
        params.extend([value, value, value])
    sql = f"SELECT * FROM products WHERE {' AND '.join(clauses)} ORDER BY createdAt DESC"
    with sqlite.get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [sqlite.row_to_dict(row) for row in rows]


def get_product_by_slug(slug: str):
    if using_mongo():
        row = _mongo_db().products.find_one({"slug": slug, "isActive": {"$ne": False}})
        return _serialize(row) if row else None
    with sqlite.get_connection() as conn:
        row = conn.execute("SELECT * FROM products WHERE slug = ? AND isActive = 1", (slug,)).fetchone()
    return sqlite.row_to_dict(row) if row else None


def create_product(data: dict[str, Any]):
    if using_mongo():
        payload = {**data, "isActive": data.get("isActive", True), "createdAt": _now()}
        result = _mongo_db().products.insert_one(payload)
        return _serialize(_mongo_db().products.find_one({"_id": result.inserted_id}))
    with sqlite.get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO products
            (name, slug, category, price, numericPrice, tag, description, shortDescription, image, specs, isFeatured, isActive)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"], data["slug"], data["category"], data["price"], data["numericPrice"],
                data["tag"], data["description"], data["shortDescription"], data["image"],
                json.dumps(data["specs"]), int(data["isFeatured"]), int(data["isActive"]),
            ),
        )
        row = conn.execute("SELECT * FROM products WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return sqlite.row_to_dict(row)


def update_product(product_id: str, data: dict[str, Any]):
    if using_mongo():
        data["updatedAt"] = _now()
        result = _mongo_db().products.update_one(_id_filter(product_id), {"$set": data})
        row = _mongo_db().products.find_one(_id_filter(product_id))
        return _serialize(row) if result.matched_count and row else None
    if "specs" in data:
        data["specs"] = json.dumps(data["specs"])
    fields = ", ".join([f"{key} = ?" for key in data])
    with sqlite.get_connection() as conn:
        result = conn.execute(f"UPDATE products SET {fields} WHERE id = ?", [*data.values(), product_id])
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    return sqlite.row_to_dict(row) if result.rowcount and row else None


def disable_product(product_id: str) -> bool:
    if using_mongo():
        result = _mongo_db().products.update_one(_id_filter(product_id), {"$set": {"isActive": False, "updatedAt": _now()}})
        return bool(result.matched_count)
    with sqlite.get_connection() as conn:
        result = conn.execute("UPDATE products SET isActive = 0 WHERE id = ?", (product_id,))
    return bool(result.rowcount)


def create_inquiry(data: dict[str, Any]):
    if using_mongo():
        payload = {**data, "status": "NEW", "createdAt": _now()}
        result = _mongo_db().inquiries.insert_one(payload)
        return _serialize(_mongo_db().inquiries.find_one({"_id": result.inserted_id}))
    with sqlite.get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO inquiries (fullName, emailOrPhone, requirementType, message, status)
            VALUES (?, ?, ?, ?, 'NEW')
            """,
            (data["fullName"], data["emailOrPhone"], data["requirementType"], data.get("message", "")),
        )
        row = conn.execute("SELECT * FROM inquiries WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return sqlite.row_to_dict(row)


def get_inquiries():
    if using_mongo():
        rows = _mongo_db().inquiries.find({}).sort("createdAt", DESCENDING)
        return [_serialize(row) for row in rows]
    with sqlite.get_connection() as conn:
        rows = conn.execute("SELECT * FROM inquiries ORDER BY createdAt DESC").fetchall()
    return [sqlite.row_to_dict(row) for row in rows]


def update_inquiry_status(inquiry_id: str, status: str):
    if using_mongo():
        result = _mongo_db().inquiries.update_one(_id_filter(inquiry_id), {"$set": {"status": status, "updatedAt": _now()}})
        row = _mongo_db().inquiries.find_one(_id_filter(inquiry_id))
        return _serialize(row) if result.matched_count and row else None
    with sqlite.get_connection() as conn:
        result = conn.execute("UPDATE inquiries SET status = ? WHERE id = ?", (status, inquiry_id))
        row = conn.execute("SELECT * FROM inquiries WHERE id = ?", (inquiry_id,)).fetchone()
    return sqlite.row_to_dict(row) if result.rowcount and row else None


def _decode_order(data: dict[str, Any]) -> dict[str, Any]:
    if isinstance(data.get("customer"), str):
        data["customer"] = json.loads(data["customer"])
    if isinstance(data.get("items"), str):
        data["items"] = json.loads(data["items"])
    return data


def create_order(data: dict[str, Any]):
    if using_mongo():
        payload = {**data, "status": "CREATED", "createdAt": _now()}
        result = _mongo_db().orders.insert_one(payload)
        return _serialize(_mongo_db().orders.find_one({"_id": result.inserted_id}))
    with sqlite.get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO orders (customer, items, notes, status) VALUES (?, ?, ?, 'CREATED')",
            (json.dumps(data["customer"]), json.dumps(data["items"]), data.get("notes", "")),
        )
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _decode_order(sqlite.row_to_dict(row))


def get_orders():
    if using_mongo():
        rows = _mongo_db().orders.find({}).sort("createdAt", DESCENDING)
        return [_serialize(row) for row in rows]
    with sqlite.get_connection() as conn:
        rows = conn.execute("SELECT * FROM orders ORDER BY createdAt DESC").fetchall()
    return [_decode_order(sqlite.row_to_dict(row)) for row in rows]


def get_order_by_id(order_id: str):
    if using_mongo():
        row = _mongo_db().orders.find_one(_id_filter(order_id))
        return _serialize(row) if row else None
    with sqlite.get_connection() as conn:
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return _decode_order(sqlite.row_to_dict(row)) if row else None


def update_order_status(order_id: str, status: str):
    if using_mongo():
        result = _mongo_db().orders.update_one(_id_filter(order_id), {"$set": {"status": status, "updatedAt": _now()}})
        row = _mongo_db().orders.find_one(_id_filter(order_id))
        return _serialize(row) if result.matched_count and row else None
    with sqlite.get_connection() as conn:
        result = conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return _decode_order(sqlite.row_to_dict(row)) if result.rowcount and row else None
