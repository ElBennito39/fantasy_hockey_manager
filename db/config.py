import psycopg2

# Connect to your postgres DB
# returns Connection if successful
conn = psycopg2.connect("dbname=fantasy_hockey_manager_bn user=postgres host='localhost' password=test1234" )

print("PostgreSQL server information")
print(conn.get_dsn_parameters(), "\n")

# Open a cursor to perform database operations
cur = conn.cursor()

# Build query string
query_create_tables = """
CREATE TABLE IF NOT EXISTS players (
  id serial,
  external_id VARCHAR   UNIQUE NOT NULL,
  full_name   VARCHAR   NOT NULL
);
"""

# Execute a query
cur.execute( query_create_tables )
conn.commit()

# create function to create player
def create_player(connection, cursor, player_attributes):
  q = "INSERT INTO players VALUES ( %s, %s, %s ) ON CONFLICT DO NOTHING;"
  cursor.execute( q, player_attributes )
  connection.commit()

# # create several players
# TODO: for some reason only the first player is created. Not sure why yet
create_player(conn, cur, ( 4, 'XXX-XXX' , 'jhtfjyt Howser'     ) )
print("created")
create_player(conn, cur, ( 2, 'XXX-XXX' , 'James Van Der Beek' ) )
print("created")
create_player(conn, cur, ( 3, 'XXX-XXX' , 'Freddie Prince Jr.' ) )
print("created")

# select players
cur.execute("SELECT * FROM players;")

# Retrieve query results
players = cur.fetchall()

print( players )
