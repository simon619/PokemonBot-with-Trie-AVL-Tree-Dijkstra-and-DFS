import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="pwroot", database="pokemon_official_database")

mycursor = db.cursor()
mycursor.execute("DESCRIBE pokemon_official")
col_name = mycursor.fetchall()

mycursor = db.cursor()
mycursor.execute("SELECT * FROM pokemon_official")
record = mycursor.fetchall()
for i in range(len(record)):
    print(f"Pokemon -> {col_name[0][0]}: {record[i][0]}, {col_name[1][0]}: {record[i][1]},"
          f" {col_name[2][0]}: {record[i][2]}, {col_name[3][0]}: {record[i][3]}, {col_name[4][0]}: {record[i][4]},"
          f" {col_name[5][0]}: {record[i][5]}, {col_name[6][0]}: {record[i][6]}, {col_name[7][0]}: {record[i][7]},"
          f"{col_name[8][0]}: {record[i][8]}, {col_name[9][0]}: {record[i][9]}, {col_name[10][0]}: {record[i][10]},"
          f"{col_name[11][0]}: {record[i][11]}, {col_name[12][0]}: {record[i][12]}, {col_name[13][0]}: {record[i][14]},"
          f"{col_name[15][0]}: {record[i][15]}, {col_name[16][0]}: {record[i][16]}, {col_name[17][0]}: {record[i][17]},"
          f"{col_name[18][0]}: {record[i][18]}, {col_name[19][0]}: {record[i][19]}, {col_name[20][0]}: {record[i][20]},")
