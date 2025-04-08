import mysql.connector as mysql

from datetime import datetime

from decimal import Decimal

# Database connection

db = mysql.connect(

host="localhost",

user="root",

passwd="Jananir40@",

database="messbill"

)

cursor = db.cursor()

# Update bill function (your existing code)

def update_bill(fingerprint_id):

cursor.execute("SELECT * FROM stud_details where fp_id=%s", (fingerprint_id,))

person = cursor.fetchone()

print(person)

if person is None:

print("Warning: Fingerprint ID not found in stud_details table.")

return

if person:

today = datetime.today()

time_str = datetime.now().time()

day = today.strftime("%A")

meal = get_meal_type(time_str)

rate = get_meal_rate(day)

cursor.execute("SELECT breakfast,lunch,snacks,dinner,tot_amt FROM stud_details WHERE fp_id=%s",
(fingerprint_id,))

tot_amt = cursor.fetchone()

new_amt = Decimal('0.0')

break_amt=Decimal('0.0')

lunch_amt=Decimal('0.0')

snacks_amt=Decimal('0.0')

dinner_amt=Decimal('0.0')

if tot_amt:

new_amt = Decimal(str(tot_amt[4]))

if break_amt:

break_amt=Decimal(str(tot_amt[0]))

if lunch_amt:

lunch_amt=Decimal(str(tot_amt[1]))

if snacks_amt:

snacks_amt=Decimal(str(tot_amt[2]))

if dinner_amt:

break_amt=Decimal(str(tot_amt[3]))

rate = get_meal_rate(day)

if meal == 'breakfast':

break_amt+= Decimal(str(rate[1]))

cursor.execute("UPDATE stud_details SET breakfast=%s WHERE fp_id=%s",(break_amt,fingerprint_id))

elif meal == 'lunch':

lunch_amt += Decimal(str(rate[2]))

cursor.execute("UPDATE stud_details SET lunch=%s WHERE fp_id=%s",(lunch_amt,fingerprint_id))

elif meal == 'snacks':

snacks_amt += Decimal(str(rate[3]))

cursor.execute("UPDATE stud_details SET snacks=%s WHERE fp_id=%s",(snacks_amt,fingerprint_id))

else:

dinner_amt += Decimal(str(rate[4]))

cursor.execute("UPDATE stud_details SET dinner=%s WHERE fp_id=%s",(dinner_amt,fingerprint_id))

print(new_amt)

print(meal)

print(time_str, day)

cursor.execute("UPDATE stud_details SET entry=%s, curr_day=%s where fp_id=%s", (time_str, day, fingerprint_id))

cursor.execute("UPDATE stud_details SET tot_amt=(SELECT SUM(breakfast+lunch+snacks+dinner)as new_amt)
WHERE fp_id=%s", (fingerprint_id,))

cursor.execute("SELECT * FROM meals_rates")

meals = cursor.fetchall()

for m in meals:

print(m)

print()

cursor.execute("SELECT * FROM stud_details")

records = cursor.fetchall()

for record in records:

print(record)

db.commit()

# Get meal type function (your existing code)

def get_meal_type(time_str):

if time_str < datetime.strptime("12:00:00", "%H:%M:%S").time():

return "breakfast"

elif time_str < datetime.strptime("17:00:00", "%H:%M:%S").time():

return "lunch"

elif time_str < datetime.strptime("18:30:00", "%H:%M:%S").time():

return "snacks"

else:

return "dinner"

# Get meal rate function (your existing code)

def get_meal_rate(day):

cursor.execute("SELECT * FROM meals_rates WHERE days=%s", (day,))

return cursor.fetchone()

# User input for fingerprint ID

fp_id = int(input("Enter Fingerprint ID: "))

# Update bill and perform visualizations

update_bill(fp_id)
