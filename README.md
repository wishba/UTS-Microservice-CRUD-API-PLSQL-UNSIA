# UTS Microservice CRUD API PLSQL UNSIA

## Requirement

-   Sudah terinstal python dan postgresql
-   Jalankan command `pip install psycopg2 dotenv`

## Cara menjalankan program user manager API

1. Download code
2. Jalankan pgAdmin dan buat database bernama `users`
3. Pada database users buka psql tool dan input command `CREATE EXTENSION pgcrypto;` untuk install ekstensi pgcrypto
4. Pada database users buka query tool dan masukan `user_encrypt.sql` untuk membuat table data_user dan membuat fungsi encrypt_data untuk fitur enkripsi aes256
5. Buka `.env.example` lalu sesuaikan code didalamnya. Setelah itu rename file menjadi `.env`
6. Nyalakan server dengan command `python main.py`
7. Jalankan program users manager API menggunakan postman atau software sejenis. Untuk mempermudah bisa import `collection_manage_user.json` pada postman

## Contoh Menjalankan Menggunakan Postman

-   Create

    ![create](screenshot/create.png)

-   Read

    ![read](screenshot/read.png)

-   Update

    ![update](screenshot/update.png)

-   Delete

    ![delete](screenshot/delete.png)

## Pengaplikasian Enkripsi AES256

### Perbandingan Select Data

-   Jika tidak memasukan password

    ![no password](screenshot/no%20password.png)

-   Jika memasukan password

    ![dengan password](screenshot/dengan%20password.png)
