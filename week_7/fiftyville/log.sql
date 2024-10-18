is it possible to rewrite the SQL queries but they still get the same results:

-- Keep a log of any SQL queries you execute as you solve the mystery.

-- View all tables in the DB
.table
airports              crime_scene_reports   people
atm_transactions      flights               phone_calls
bakery_security_logs  interviews
bank_accounts         passengers

-- View crime_scene_reports

SELECT description
   ...>   FROM crime_scene_reports
   ...>  WHERE month = 7
   ...>    AND day = 28
   ...>    AND street = 'Humphrey Street';

-- The witness transcript might hold further clues.

SELECT name, transcript
  FROM interviews
 WHERE month = 7
   AND day = 28;

-- Narrow list for descriptions near bakery,
SELECT name, transcript
  FROM interviews
 WHERE month = 7
   AND day = 28
   AND transcript LIKE '%bakery%'
 ORDER BY name;

--Ruth mentioned that the thief drove away in a car from the bakery within 10 minutes of the theft.

SELECT name, bakery_security_logs.hour, bakery_security_logs.minute
  FROM people
  JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate
 WHERE bakery_security_logs.month = 7
   AND bakery_security_logs.day = 28
   AND bakery_security_logs.activity = 'exit'
   AND bakery_security_logs.hour = 10
   AND bakery_security_logs.minute >= 15
   AND bakery_security_logs.minute <= 25
 ORDER BY bakery_security_logs.minute;

-- Eugene mentioned the thief was withdrawing money from the ATM on Leggett Street.

SELECT account_number, amount
  FROM atm_transactions
 WHERE month = 7
   AND day = 28
   AND atm_location = 'Leggett Street'
   AND transaction_type = 'withdraw';

-- Find names and account numbers.

SELECT name, atm_transactions.amount
  FROM people
  JOIN bank_accounts
    ON people.id = bank_accounts.person_id
  JOIN atm_transactions
    ON bank_accounts.account_number = atm_transactions.account_number
 WHERE atm_transactions.month = 7
   AND atm_transactions.day = 28
   AND atm_transactions.atm_location = 'Leggett Street'
   AND atm_transactions.transaction_type = 'withdraw';

-- Raymond used the phone asked the person on the other end of the call to buy a flight ticket for the earliest flight on July 29. Raging Clue!

SELECT abbreviation, full_name, city
  FROM airports
 WHERE city = 'Fiftyville';

-- Check phone call records to find the person who bought the tickets.
SELECT name, phone_calls.duration
  FROM people
  JOIN phone_calls
    ON people.phone_number = phone_calls.caller
 WHERE phone_calls.month = 7
   AND phone_calls.day = 28
   AND phone_calls.duration <= 60
 ORDER BY phone_calls.duration;

-- Check potential names of the call recipients and arranging them based on the call durations.
SELECT name, phone_calls.duration
  FROM people
  JOIN phone_calls
    ON people.phone_number = phone_calls.receiver
 WHERE phone_calls.month = 7
   AND phone_calls.day = 28
   AND phone_calls.duration <= 60
   ORDER BY phone_calls.duration;

-- Finding the flights on July 29 from Fiftyville airport, and ordering them by time.
SELECT flights.id, full_name, city, flights.hour, flights.minute
  FROM airports
  JOIN flights
    ON airports.id = flights.destination_airport_id
 WHERE flights.origin_airport_id =
       (SELECT id
          FROM airports
         WHERE city = 'Fiftyville')
   AND flights.year = 2021
   AND flights.month = 7
   AND flights.day = 29
 ORDER BY flights.hour, flights.minute;

-- Check passenger list.

Passengers.flight_id, name, passengers.passport_number, passengers.seat
  FROM people
  JOIN passengers
    ON people.passport_number = passengers.passport_number
  JOIN flights
    ON passengers.flight_id = flights.id
 WHERE flights.month = 7
   AND flights.day = 29
   AND flights.hour = 8
   AND flights.minute = 20
 ORDER BY passengers.passport_number;

-- Bruce is the duck thief, as he appears on every list: ATM transactions, phone calls, and flight passengers. He likely fled to New York City, taking a flight there, with Robin as the accomplice who bought the ticket and helped him escape.
