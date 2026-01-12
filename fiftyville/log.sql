-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Choose the crime report on "July 28, 2024" and on "Humphrey Street".
SELECT description FROM crime_scene_reports
 WHERE id = 295;
SELECT id
  FROM crime_scene_reports
 WHERE year = 2024 AND month = 7 AND day = 28
   AND street = 'Humphrey Street';
-- Returns id = 295 and 297
SELECT description FROM crime_scene_reports WHERE id = 295;
-- Know that it's id = 295, with the description:
-- 	Theft of the CS50 duck took place at 10:15am at the Humphrey Street
-- 	bakery. Interviews were conducted today with three witnesses
-- 	who were present at the time – each of their interview transcripts
-- 	mentions the bakery.
SELECT transcript FROM interviews
 WHERE year = 2024 AND month = 7 AND day = 28
   AND transcript LIKE '%bakery%';
-- 1. Sometime within ten minutes of the theft, I saw the thief get into a car
-- 	in the bakery parking lot and drive away. If you have security footage
-- 	from the bakery parking lot, you might want to look for cars that left
-- 	the parking lot in that time frame.
-- 2. I don't know the thief's name, but it was someone I recognized.
-- 	Earlier this morning, before I arrived at Emma's bakery, I was walking by
-- 	the ATM on Leggett Street and saw the thief there withdrawing some money.
-- 3. As the thief was leaving the bakery, they called someone who talked to
-- 	them for less than a minute. In the call, I heard the thief say that
-- 	they were planning to take the earliest flight out of Fiftyville tomorrow.
-- 	The thief then asked the person on the other end of the phone to purchase
-- 	the flight ticket.

-- 1. Thief-car left with a car from the bakery parking lot
-- 	between 10:15am and 10:25am.
SELECT activity FROM bakery_security_logs
 WHERE year = 2024 AND month = 7 AND day = 28
   AND hour = 10 AND minute BETWEEN 15 AND 25 GROUP BY activity;
-- The activity is exit.
SELECT license_plate FROM bakery_security_logs
 WHERE year = 2024 AND month = 7 AND day = 28
   AND hour = 10 AND minute BETWEEN 15 AND 25
   AND activity = 'exit';
+---------------+
| license_plate |
+---------------+
| 5P2BI95       |
| 94KL13X       |
| 6P58WS2       |
| 4328GD8       |
| G412CB7       |
| L93JTIZ       |
| 322W7JE       |
| 0NTHK55       |
+---------------+
-- 1-1. Search for the account owners.
SELECT id, name FROM people WHERE license_plate IN
       (SELECT license_plate FROM bakery_security_logs
         WHERE year = 2024 AND month = 7 AND day = 28
           AND hour = 10 AND minute BETWEEN 15 AND 25
           AND activity = 'exit') ORDER BY name;
+--------+---------+
|   id   |  name   |
+--------+---------+
| 243696 | Barry   |
| 686048 | Bruce   |
| 514354 | Diana   |
| 396669 | Iman    |
| 560886 | Kelsey  |
| 467400 | Luca    |
| 398010 | Sofia   |
| 221103 | Vanessa |
+--------+---------+

-- 2. The thief-ATM withdrew money at the ATM on Leggett Street before 10:15am.
SELECT transaction_type FROM atm_transactions GROUP BY transaction_type;
-- types: deposit and withdraw
SELECT account_number FROM atm_transactions
 WHERE year = 2024 AND month = 7 AND day = 28
   AND atm_location = 'Leggett Street'
   AND transaction_type = 'withdraw';
+----------------+
| account_number |
+----------------+
| 28500762       |
| 28296815       |
| 76054385       |
| 49610011       |
| 16153065       |
| 25506511       |
| 81061156       |
| 26013199       |
+----------------+

-- 2-1. Search for the account owners.
SELECT phone_number, id, name FROM people WHERE id IN
       (SELECT person_id FROM bank_accounts
         WHERE account_number IN
               (SELECT account_number FROM atm_transactions
                 WHERE year = 2024 AND month = 7 AND day = 28
                   AND atm_location = 'Leggett Street'
                   AND transaction_type = 'withdraw')) ORDER BY name;
+--------+---------+
|   id   |  name   |
+--------+---------+
| 438727 | Benista |
| 458378 | Brooke  |
| 686048 | Bruce   |
| 514354 | Diana   |
| 396669 | Iman    |
| 395717 | Kenny   |
| 467400 | Luca    |
| 449774 | Taylor  |
+--------+---------+

-- 3. Phone tracking - Thief-caller
SELECT COUNT(id) FROM phone_calls
 WHERE year = 2024 AND month = 7 AND day = 28
   AND duration < 1;
-- Know that duration's unit is second and id is useless.
SELECT COUNT(id) FROM people WHERE phone_number IN
       (SELECT id FROM phone_calls
         WHERE year = 2024 AND month = 7 AND day = 28
           AND duration < 60) ORDER BY name;
SELECT phone_number, id, name FROM people WHERE id IN
       (SELECT person_id FROM bank_accounts
         WHERE account_number IN
               (SELECT account_number FROM atm_transactions
                 WHERE year = 2024 AND month = 7 AND day = 28
                   AND atm_location = 'Leggett Street'
                   AND transaction_type = 'withdraw')) ORDER BY name;
-- Know that id is useless.
SELECT caller, receiver FROM phone_calls
 WHERE year = 2024 AND month = 7 AND day = 28
   AND duration < 60 ORDER BY caller;
+----------------+----------------+
|     caller     |    receiver    |
+----------------+----------------+
| (031) 555-6622 | (910) 555-3251 |
| (130) 555-0289 | (996) 555-8899 |
| (286) 555-6063 | (676) 555-6554 |
| (338) 555-6650 | (704) 555-2131 |
| (367) 555-5533 | (375) 555-8161 |
| (499) 555-9472 | (892) 555-8872 |
| (499) 555-9472 | (717) 555-1342 |
| (770) 555-1861 | (725) 555-3243 |
| (826) 555-1652 | (066) 555-9701 |
+----------------+----------------+
SELECT id, name FROM people WHERE phone_number IN
       (SELECT caller FROM phone_calls
         WHERE year = 2024 AND month = 7 AND day = 28
         AND duration < 60) ORDER BY name;
+--------+---------+
|   id   |  name   |
+--------+---------+
| 438727 | Benista |
| 686048 | Bruce   |
| 907148 | Carina  |
| 514354 | Diana   |
| 560886 | Kelsey  |
| 395717 | Kenny   |
| 398010 | Sofia   |
| 449774 | Taylor  |
+--------+---------+


Suspects:
		Thief-car
+--------+---------+
|   id   |  name   |
+--------+---------+
| 243696 | Barry   |
| 686048 | Bruce   |
| 514354 | Diana   |
| 396669 | Iman    |
| 560886 | Kelsey  |
| 467400 | Luca    |
| 398010 | Sofia   |
| 221103 | Vanessa |
+--------+---------+
Thief-ATM
+--------+---------+
|   id   |  name   |
+--------+---------+
| 438727 | Benista |
| 458378 | Brooke  |
| 686048 | Bruce   |
| 514354 | Diana   |
| 396669 | Iman    |
| 395717 | Kenny   |
| 467400 | Luca    |
| 449774 | Taylor  |
+--------+---------+
Thief-caller
+--------+---------+
|   id   |  name   |
+--------+---------+
| 438727 | Benista |
| 686048 | Bruce   |
| 907148 | Carina  |
| 514354 | Diana   |
| 560886 | Kelsey  |
| 395717 | Kenny   |
| 398010 | Sofia   |
| 449774 | Taylor  |
+--------+---------+
-- Since the personnel interested is singular: the theif, as authorities believe,
-- we can cross reference all three lists.
SELECT id, name FROM people WHERE license_plate IN
       (SELECT license_plate FROM bakery_security_logs
         WHERE year = 2024 AND month = 7 AND day = 28
           AND hour = 10 AND minute BETWEEN 15 AND 25
           AND activity = 'exit')
INTERSECT
SELECT id, name FROM people WHERE id IN
       (SELECT person_id FROM bank_accounts
         WHERE account_number IN
               (SELECT account_number FROM atm_transactions
                 WHERE year = 2024 AND month = 7 AND day = 28
                   AND atm_location = 'Leggett Street'
                   AND transaction_type = 'withdraw'))
INTERSECT
SELECT id, name FROM people WHERE phone_number IN
       (SELECT caller FROM phone_calls
         WHERE year = 2024 AND month = 7 AND day = 28
         AND duration < 60) ORDER BY name;
+--------+-------+
|   id   | name  |
+--------+-------+
| 686048 | Bruce |
| 514354 | Diana |
+--------+-------+

-- 4. Earliest flight out of Fiftyville tomorrow (29/07/2024)
SELECT * FROM airports;
SELECT * FROM flights;
-- Know to select flights by id.
SELECT id, hour FROM flights WHERE origin_airport_id IN
       (SELECT id FROM airports WHERE city = 'Fiftyville'
           AND year = 2024 AND month = 7 AND day = 29)
      ORDER BY hour LIMIT 5;
+----+------+
| id | hour |
+----+------+
| 36 | 8    |
| 43 | 9    |
| 23 | 12   |
| 53 | 15   |
| 18 | 16   |
+----+------+

-- 5. Filter through the flights by the id of suspects.
SELECT id, name FROM people WHERE passport_number IN
       (SELECT passport_number FROM passengers
         WHERE flight_id IN (36, 43))
            --    (SELECT id FROM flights WHERE origin_airport_id IN
            --            (SELECT id FROM airports WHERE city = 'Fiftyville'
            --            AND year = 2024 AND month = 7 AND day = 29)))
INTERSECT
SELECT id, name FROM people WHERE id IN (686048, 514354)
ORDER BY name;
-- Theif found:
+--------+-------+
|   id   | name  |
+--------+-------+
| 686048 | Bruce |
+--------+-------+
-- Checked and flight_id is verified as 36.
SELECT city FROM airports WHERE id =
       (SELECT destination_airport_id FROM flights
         WHERE id = 36
           AND year = 2024 AND month = 7 AND day = 29);
+---------------+
|     city      |
+---------------+
| New York City |
+---------------+
-- 6. And the accomplice is:
SELECT id, name FROM people WHERE phone_number IN
       (SELECT receiver FROM phone_calls WHERE caller =
               (SELECT phone_number FROM people WHERE id = 686048));
+--------+--------+
|   id   |  name  |
+--------+--------+
| 205082 | Pamela |
+--------+--------+
-- 6-1. Double check if she booked the flight.
-- 	No purchase information of the flight ticket. Cannot verify.




-- 7. It's wrong. Re-investigate.
SELECT id, name FROM people WHERE phone_number IN
      (SELECT receiver FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28
          AND caller =
          (SELECT phone_number FROM people WHERE id = 686048));
+--------+---------+
|   id   |  name   |
+--------+---------+
| 315221 | Gregory |
| 652398 | Carl    |
| 864400 | Robin   |
| 985497 | Deborah |
+--------+---------+
SELECT id, name FROM people WHERE phone_number IN
      (SELECT receiver FROM phone_calls WHERE caller =
          (SELECT phone_number FROM people WHERE id = 686048));
+--------+-----------+
|   id   |   name    |
+--------+-----------+
| 205082 | Pamela    |
| 230917 | Karen     |
| 313837 | Tyler     |
| 315221 | Gregory   |
| 539107 | Joseph    |
| 600585 | Bryan     |
| 639344 | Charlotte |
| 652398 | Carl      |
| 660982 | Thomas    |
| 864400 | Robin     |
| 985497 | Deborah   |
+--------+-----------+
-- Pamela didn't call Bruce on the date of crime,
-- 	but due to the misuse of syntax "=" instead of "IN",
-- 	the database returns only the first row in id, aka Pamela.
SELECT id, name FROM people WHERE phone_number IN
      (SELECT receiver FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28
          AND caller =
              (SELECT phone_number FROM people WHERE id = 686048)
          AND duration < 60);
+--------+-------+
|   id   | name  |
+--------+-------+
| 864400 | Robin |
+--------+-------+
