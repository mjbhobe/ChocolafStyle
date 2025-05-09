"""connect.py : connecting to PostgreSQL database using SqlAlchemy + psycopg2 """

from sqlalchemy import create_engine, text
import urllib.parse

pwd = urllib.parse.quote_plus("M@st5r$#")

# connection string format = userID:pwd@host:post/db_name
conn_str = f"postgres:{pwd}@localhost:5432/dvdrental"
engine = create_engine(f"postgresql+psycopg2://{conn_str}")
conn = engine.connect()

sql = text("select * from actor limit 5")
# fetch all records
records = conn.execute(sql).fetchall()

for rec in records:
    print("\n", rec)

# a very complex SQL
sql2 = text(
    """
with t1 as (
    select c.name as Genre, count(cu.customer_id) as Total_rent_demand
    from category c
    join film_category fc using (category_id)
    join film f using(film_id)
    join inventory i using(film_id)
    join rental r using(inventory_id)
    join customer cu using(customer_id)
    group by 1
    order by 2 desc
),
t2 as (
   select c.name as Genre, sum(p.amount) as Total_Sales
   from category c 
   join film_category fc using(category_id)
   join film f using(film_id)
   join inventory i using(film_id)
   join rental r using(inventory_id)
   join payment p using(rental_id)
   group by 1
   order by 2 desc
)
select t1.genre, t1.total_rent_demand, t2.total_sales
from t1 join t2 
on t1.genre = t2.genre
limit 10
"""
)

records2 = conn.execute(sql2).fetchall()
for rec in records2:
    print("\n", rec)
