import mysql.connector
from InquirerPy import inquirer

conn = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)

class Kasir:

    def loginadmin(self):
        username = inquirer.text(message="Masukan username admin").execute()
        password = inquirer.number(message="Masukan password admin").execute()

        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM admin WHERE username = %s AND password = %s",
            (username, password)
        )
        result = cursor.fetchone()

        if result:
            print("Login berhasil, selamat datang admin")
            return True
        else:
            print("Username atau password salah")
            return False

    def tambahbarang(self):
        kode = inquirer.text(message="Masukan kode barang").execute()
        nama = inquirer.text(message="Masukan nama barang").execute()
        harga = int(inquirer.number(message="Masukan harga barang").execute())
        banyak = int(inquirer.number(message="Masukan jumlah barang").execute())

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM stock WHERE kode_barang = %s", (kode,))
        result = cursor.fetchone()

        if result:
            cursor.execute(
                "UPDATE stock SET stok_barang = stok_barang + %s WHERE kode_barang = %s",
                (banyak, kode)
            )
            print("Stok berhasil ditambahkan")
        else:
            cursor.execute(
                "INSERT INTO stock (kode_barang, nama_barang, harga, stok_barang) VALUES (%s, %s, %s, %s)",
                (kode, nama, harga, banyak)
            )
            print("Barang baru ditambahkan")

        conn.commit()

    def transaksi(self):
        cursor = conn.cursor()
        cursor.execute("SELECT kode_barang, nama_barang, harga, stok_barang FROM stock")
        data = cursor.fetchall()
        if not data:
            print("Tidak ada barang di stock")
            return
        pilihan = [
            f"{item[0]} - {item[1]} (Rp{item[2]}) [Stok: {item[3]}]"
            for item in data
        ]
        pilih = inquirer.select(
            message="Pilih barang yang ingin dibeli",
            choices=pilihan
        ).execute()
        kode = pilih.split(" - ")[0]
        cursor.execute(
            "SELECT nama_barang, harga, stok_barang FROM stock WHERE kode_barang = %s",
            (kode,)
        )
        barang = cursor.fetchone()
        nama, harga, stok = barang
        jumlah = int(inquirer.number(message="Masukan jumlah barang").execute())
        if jumlah > stok:
            print("Stok tidak mencukupi")
            return
        total = harga * jumlah
        diskon = 0
        if total > 200000:
            diskon = total * 0.10
        total_bayar = total - diskon
        cursor.execute(
            "UPDATE stock SET stok_barang = stok_barang - %s WHERE kode_barang = %s",
            (jumlah, kode)
        )
        conn.commit()

        # STRUK
        print("\n STRUK BELANJA")
        print(f"Barang   : {nama}")
        print(f"Harga    : Rp{harga}")
        print(f"Jumlah   : {jumlah}")
        print(f"Total    : Rp{total}")

        if diskon > 0:
            print(f"Diskon   : Rp{int(diskon)}")

        print(f"Bayar    : Rp{int(total_bayar)}")
        print("===========================")


app = Kasir()

if app.loginadmin():
    while True:
        menu = inquirer.select(
            message="Pilih menu",
            choices=[
                "Tambah Barang",
                "Transaksi",
                "Keluar"
            ]
        ).execute()

        if menu == "Tambah Barang":
            app.tambahbarang()
        elif menu == "Transaksi":
            app.transaksi()
        else:
            print("Program selesai")
            break