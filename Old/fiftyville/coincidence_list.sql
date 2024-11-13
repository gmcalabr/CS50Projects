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

/* Activity records for people who took money from the ATM on Leggett Street on the 28th and also flew the 29th */
/*Command Line Code: cat coincidence_list.sql | sqlite3 fiftyville.db */

-- +-----+--------+---------+----------------+-----------------+---------------+------------------+
-- | day | amount |  name   |  phone_number  | passport_number | license_plate | transaction_type |
-- +-----+--------+---------+----------------+-----------------+---------------+------------------+
-- | 28  | 50     | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       | withdraw         |
-- | 28  | 10     | Kaelyn  | (098) 555-1164 | 8304650265      | I449449       | deposit          |
-- | 28  | 35     | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       | withdraw         |
-- | 28  | 80     | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       | withdraw         |
-- | 28  | 20     | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       | withdraw         |
-- | 28  | 20     | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       | withdraw         |
-- | 28  | 48     | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       | withdraw         |
-- | 28  | 60     | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       | withdraw         |
-- | 28  | 30     | Benista | (338) 555-6650 | 9586786673      | 8X428L0       | withdraw         |
-- +-----+--------+---------+----------------+-----------------+---------------+------------------+
-- +-----+------+-------+-----+------+--------+----------+---------------+--------+--------+----------------+-----------------+---------------+
-- | id  | year | month | day | hour | minute | activity | license_plate |   id   |  name  |  phone_number  | passport_number | license_plate |
-- +-----+------+-------+-----+------+--------+----------+---------------+--------+--------+----------------+-----------------+---------------+
-- | 232 | 2023 | 7     | 28  | 8    | 23     | entrance | 94KL13X       | 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | 237 | 2023 | 7     | 28  | 8    | 34     | entrance | 1106N58       | 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
-- | 248 | 2023 | 7     | 28  | 8    | 50     | entrance | 4V16VO0       | 864400 | Robin  | (375) 555-8161 | NULL            | 4V16VO0       |
-- | 249 | 2023 | 7     | 28  | 8    | 50     | exit     | 4V16VO0       | 864400 | Robin  | (375) 555-8161 | NULL            | 4V16VO0       |
-- | 254 | 2023 | 7     | 28  | 9    | 14     | entrance | 4328GD8       | 467400 | Luca   | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 261 | 2023 | 7     | 28  | 10   | 18     | exit     | 94KL13X       | 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | 263 | 2023 | 7     | 28  | 10   | 19     | exit     | 4328GD8       | 467400 | Luca   | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 268 | 2023 | 7     | 28  | 10   | 35     | exit     | 1106N58       | 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
-- +-----+------+-------+-----+------+--------+----------+---------------+--------+--------+----------------+-----------------+---------------+
