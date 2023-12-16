CREATE TABLE data_user (
 	id SERIAL PRIMARY KEY,
	user_name bytea,
 	user_role bytea
);


-- function to encrypt data user
CREATE OR REPLACE FUNCTION encrypt_data(user_data text, password text) RETURNS bytea AS $$
BEGIN
	RETURN pgp_sym_encrypt(user_data, password, 'compress-algo=1, cipher-algo=aes256');
END;
$$ LANGUAGE plpgsql;


---- insert encrypted user
--INSERT INTO data_user (user_name, user_role)
--VALUES (encrypt_data('wisnu bayu', 'admin_password'), encrypt_data('operator', 'admin_password'));


---- update user data
--UPDATE data_user
--SET
--user_name = encrypt_data(
--  'wisnu bayu aji',
--  'admin_password'
--),
--user_role = encrypt_data(
--	'operator',
--	'admin_password'
--)
--WHERE id = 1;


---- delete user
--DELETE FROM data_user WHERE id = 1;


---- read decrypted data
--SELECT 
--id, 
--pgp_sym_decrypt(user_name, 'admin_password') AS user_name, 
--pgp_sym_decrypt(user_role, 'admin_password') AS user_role
--FROM data_user;


---- select only
--SELECT * FROM data_user