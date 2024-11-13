SELECT month, day, amount, transaction_type, name FROM atm_transactions
JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number
JOIN people ON person_id = people.id
WHERE month = 7
AND name = 'Robin'
;

