import mysql.connector

# Use the new password you just set
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tanu**123", 
    database="real_estate"
)
cursor = db.cursor()

# Sample data: (Price in Lakhs, Sqft, BHK, Locality, City, Geometry)
data = [
    (85.5, 1200, 2, 'Andheri', 'Mumbai', 'POINT(72.8696 19.1136)'),
    (120.0, 1800, 3, 'Bandra', 'Mumbai', 'POINT(72.8402 19.0522)'),
    (45.0, 600, 1, 'Borivali', 'Mumbai', 'POINT(72.8573 19.2290)'),
    (210.0, 2500, 4, 'Worli', 'Mumbai', 'POINT(72.8168 19.0176)'),
    (95.0, 1400, 2, 'Powai', 'Mumbai', 'POINT(72.9052 19.1176)')
]

query = "INSERT INTO property_listings (price_total, area_sqft, bhk_count, locality_name, city, location) VALUES (%s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))"

cursor.executemany(query, data)
db.commit()
print(f"Successfully inserted {cursor.rowcount} rows.")