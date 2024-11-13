-- Keep a log of any SQL queries you execute as you solve the mystery.
/*  Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery */

/* First solid interviews that saw thief. Interviews 161,2,3 */
SELECT * FROM interviews WHERE transcript LIKE '%bakery%';
/* interviews 161: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame */
/* interviews 162: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money. */
/* interviews 163: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. */

/* List of possible withdrawls (transactions) that happened according to interview 163 Raymond. None particularly suspicious.*/
SELECT * FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street';
/**/

/*Overlap between flights leaving on the 28th or 29th and their destination airports*/
SELECT * FROM flights JOIN airports ON destination_airport_id = airports.id WHERE day = 29 OR day = 28; -- less refined
SELECT destination_airport_id, day, hour, minute, abbreviation, full_name, city FROM flights JOIN airports ON destination_airport_id = airports.id WHERE day = 29 OR day = 28 AND origin_airport_id = 8 ORDER BY day, hour, minute; -- more refined

/* Based on the combo of passenger_and_passport_list.sql and bank_records.sql */
/* People who both used the ATM on Leggett Street AND Flew the next morning*/
/* Suspects include: Bruce, Taylor, Kenny, Luca  */
/* Kenny is off the list as he did not go to the bakery on 7/28 */
/* Taylor left at 10:35, 20 min after the incident. Eye Witnesses stated that the perp left within 10min after the theft.*/
/* Luca never made a call of less than a minute after the theft*/
/* Robin was called by Bruce for 45 seconds on 7/28*/

-- Passenger and Transport List
SELECT * FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE flights.id = 36
;

/*Now using this list for extended bank records to see who the accomplice was*/

SELECT * FROM atm_transactions
JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number
JOIN people ON person_id = people.id
WHERE month = 7 AND day > 28
AND atm_location = 'Leggett Street';

-- Coincidence List
SELECT day, amount, name, phone_number, passport_number, license_plate, transaction_type FROM atm_transactions
JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number
JOIN people ON people.id = bank_accounts.person_id
WHERE day = 28
AND month = 7
AND atm_location = 'Leggett Street'
-- AND (license_plate = (SELECT license_plate FROM people WHERE name = 'Bruce')
-- OR license_plate = (SELECT license_plate FROM people WHERE name = 'Taylor')
-- OR license_plate = (SELECT license_plate FROM people WHERE name = 'Kenny')
-- OR license_plate = (SELECT license_plate FROM people WHERE name = 'Luca'))

;

SELECT * FROM bakery_security_logs
JOIN people ON people.license_plate = bakery_security_logs.license_plate
WHERE day = 28 AND month = 7
AND (name = 'Bruce'
OR name = 'Taylor'
OR name = 'Kenny'
OR name = 'Luca'
OR name = 'Robin')
;

-- Call Logs
SELECT caller, receiver, duration, name FROM phone_calls
JOIN people ON phone_calls.caller = people.phone_number
WHERE month = 7
AND day = 28
AND duration <=60
;

SELECT * FROM people
WHERE phone_number = '(375) 555-8161'
;

