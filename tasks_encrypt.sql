---- Create table
CREATE TABLE tasks_encrypt (
 id SERIAL PRIMARY KEY,
 task_name bytea
);


---- Define a function to encrypt tasks
CREATE OR REPLACE FUNCTION encrypt_tasks(tsk text, password text) RETURNS bytea AS $$
BEGIN
 RETURN pgp_sym_encrypt(tsk, password, 'compress-algo=1, cipher-algo=aes256');
END;
$$ LANGUAGE plpgsql;


---- CREATE - Insert encrypted tasks with my_todo_password as a password
--INSERT INTO tasks_encrypt (task_name)
--VALUES (encrypt_tasks('belajar enkripsi', 'my_todo_password'));


---- READ - Decrypted and select all data with my_todo_password as a password
--SELECT id, pgp_sym_decrypt(task_name, 'my_todo_password') as decrypted_tasks
--FROM tasks_encrypt;


---- READ - Without decrypted
--SELECT * FROM tasks_encrypt;


---- UPDATE
--UPDATE tasks_encrypt
--SET
--task_name = encrypt_tasks(
--  'updated_tasks',
--  'my_todo_password'
--)
--WHERE id = 1;


---- DELETE
--DELETE FROM tasks_encrypt WHERE id = 1;
