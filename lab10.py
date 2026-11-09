import psycopg2

conn = psycopg2.connect(
    dbname="lab10",
    user="postgres",
    password="lab123",
    host="localhost",
    port="5432",
)

cursor = conn.cursor()

print("QUESTION 1: Satellites with Completed Downlinks in North Region")
cursor.execute("""
    SELECT DISTINCT s.satellite_name
    FROM Satellites s
    JOIN Downlinks d ON s.satellite_id = d.satellite_id
    JOIN Ground_Stations g ON d.station_id = g.station_id
    WHERE d.status = 'Completed' AND g.region = 'North'
    ORDER BY s.satellite_name ASC;
""")
results1 = cursor.fetchall()

for row in results1:
    print(row)
print()

print("QUESTION 2: Ground Stations Receiving > 30 GB (Completed)")
cursor.execute("""
    SELECT g.station_name, SUM(d.data_gb) AS total_data
    FROM Ground_Stations g
    JOIN Downlinks d ON g.station_id = d.station_id
    WHERE d.status = 'Completed'
    GROUP BY g.station_id, g.station_name
    HAVING SUM(d.data_gb) > 30
    ORDER BY total_data DESC;
""")
results2 = cursor.fetchall()

for row in results2:
    print(row)
print()

print("QUESTION 3: Satellites with Completed Downlinks at >= 2 Stations")
cursor.execute("""
    SELECT 
        s.satellite_id, 
        s.satellite_name, 
        COUNT(DISTINCT d.station_id) AS distinct_stations, 
        SUM(d.data_gb) AS total_completed_data
    FROM Satellites s
    JOIN Downlinks d ON s.satellite_id = d.satellite_id
    WHERE d.status = 'Completed'
    GROUP BY s.satellite_id, s.satellite_name
    HAVING COUNT(DISTINCT d.station_id) >= 2
    ORDER BY distinct_stations DESC, s.satellite_name ASC;
""")
results3 = cursor.fetchall()

for row in results3:
    print(row)
print()

cursor.close()
conn.close()