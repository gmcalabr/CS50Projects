/*Now using this list for extended bank records to see who the accomplice was*/

SELECT * FROM atm_transactions
JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number
JOIN people ON person_id = people.id
WHERE month = 7 AND day > 28
AND atm_location = 'Leggett Street';

/* Command Line: cat bank_records.sql | sqlite3 fiftyville.db */

/* fiftyville/ $ cat bank_records.sql | sqlite3 fiftyville.db */
/* +-----+----------------+------+-------+-----+----------------+------------------+--------+----------------+-----------+---------------+--------+---------+----------------+-----------------+---------------+ */
/* | id  | account_number | year | month | day |  atm_location  | transaction_type | amount | account_number | person_id | creation_year |   id   |  name   |  phone_number  | passport_number | license_plate | */
/* +-----+----------------+------+-------+-----+----------------+------------------+--------+----------------+-----------+---------------+--------+---------+----------------+-----------------+---------------+ */
/* | 267 | 49610011       | 2023 | 7     | 28  | Leggett Street | withdraw         | 50     | 49610011       | 686048    | 2010          | 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       | */
/* | 275 | 86363979       | 2023 | 7     | 28  | Leggett Street | deposit          | 10     | 86363979       | 948985    | 2010          | 948985 | Kaelyn  | (098) 555-1164 | 8304650265      | I449449       | */
/* | 336 | 26013199       | 2023 | 7     | 28  | Leggett Street | withdraw         | 35     | 26013199       | 514354    | 2012          | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       | */
/* | 269 | 16153065       | 2023 | 7     | 28  | Leggett Street | withdraw         | 80     | 16153065       | 458378    | 2012          | 458378 | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       | */
/* | 264 | 28296815       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     | 28296815       | 395717    | 2014          | 395717 | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       | */
/* | 288 | 25506511       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     | 25506511       | 396669    | 2014          | 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       | */
/* | 246 | 28500762       | 2023 | 7     | 28  | Leggett Street | withdraw         | 48     | 28500762       | 467400    | 2014          | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       | */
/* | 266 | 76054385       | 2023 | 7     | 28  | Leggett Street | withdraw         | 60     | 76054385       | 449774    | 2015          | 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       | */
/* | 313 | 81061156       | 2023 | 7     | 28  | Leggett Street | withdraw         | 30     | 81061156       | 438727    | 2018          | 438727 | Benista | (338) 555-6650 | 9586786673      | 8X428L0       | */
/* +-----+----------------+------+-------+-----+----------------+------------------+--------+----------------+-----------+---------------+--------+---------+----------------+-----------------+---------------+ */

