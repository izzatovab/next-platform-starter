import json
import re

# Viloyatlar ro'yxati
REGIONS = {
    "1": ["Tashkent", "01"],
    "2": ["Namangan", "50"],
    "3": ["Syrdarya", "20"],
    "4": ["Jizzakh", "25"],
    "5": ["Samarkand", "30"],
    "6": ["Fergana", "40"],
    "7": ["Andijan", "60"],
    "8": ["Kashkadarya", "70"],
    "9": ["Surkhandarya", "75"],
    "10": ["Bukhara", "80"],
    "11": ["Navoi", "85"],
    "12": ["Khorezm", "90"]
}

class DataHandler:
    @staticmethod
    def read_data(file_name):
        try:
            with open(file_name, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def write_data(file_name, data):
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

class Panel:
    def __init__(self):
        self.data_handler = DataHandler()

    def view_plates(self):
        plates = self.data_handler.read_data("plates.json")
        if not plates:
            print("Hozircha raqamlar mavjud emas.")
            return
        print("\nMavjud raqamlar:")
        for idx, plate in enumerate(plates, start=1):
            formatted_price = f"{int(plate['price']):,}".replace(",", ".")
            print(f"{idx}. [{plate['region']}] {plate['plate']} - {formatted_price} so'm")

class AdminPanel(Panel):
    def add_plate(self):
        plates = self.data_handler.read_data("plates.json")
        region_code = self.select_region()
        while True:
            plate = input("Raqamni kiriting (3 harf va 3 ketma-ket son): ").upper()
            if self.is_valid_plate(plate):
                if any(p["plate"] == plate for p in plates):
                    print("Bu raqam allaqachon mavjud. Qayta urinib ko'ring.")
                    continue
                break
            else:
                print("Noto'g'ri format. Raqam quyidagi shaklda bo'lishi kerak: ABC123.")
        while True:
            try:
                price = int(input("Narxni kiriting: "))
                break
            except ValueError:
                print("Narxni to'g'ri formatda kiriting (faqat sonlar).")
        plates.append({"region": region_code, "plate": plate, "price": price})
        self.data_handler.write_data("plates.json", plates)
        print("Raqam muvaffaqiyatli qo'shildi.")

    def remove_plate(self):
        plates = self.data_handler.read_data("plates.json")
        if not plates:
            print("Hozircha ro'yxatda hech qanday raqam yo'q.")
            return
        self.view_plates()
        while True:
            try:
                plate_id = int(input("O'chirish kerak bo'lgan raqam ID-sini kiriting: ")) - 1
                if 0 <= plate_id < len(plates):
                    plates.pop(plate_id)
                    self.data_handler.write_data("plates.json", plates)
                    print("Raqam muvaffaqiyatli o'chirildi.")
                    break
                else:
                    print("Noto'g'ri ID.")
            except ValueError:
                print("Iltimos, ID ni to'g'ri kiriting.")

    def edit_plate(self):
        plates = self.data_handler.read_data("plates.json")
        if not plates:
            print("Hozircha ro'yxatda hech qanday raqam yo'q.")
            return
        self.view_plates()
        while True:
            try:
                plate_id = int(input("Tahrirlash kerak bo'lgan raqam ID-sini kiriting: ")) - 1
                if 0 <= plate_id < len(plates):
                    break
                else:
                    print("Noto'g'ri ID.")
            except ValueError:
                print("Iltimos, ID ni to'g'ri kiriting.")
        new_price = int(input("Yangi narxni kiriting: "))
        plates[plate_id]["price"] = new_price
        self.data_handler.write_data("plates.json", plates)
        print("Raqam muvaffaqiyatli tahrirlandi.")

    def view_sold_plates(self):
        purchases = self.data_handler.read_data("purchases.json")
        if not purchases:
            print("Hozircha hech qanday sotilgan raqam yo'q.")
            return
        print("\nSotilgan raqamlar:")
        for idx, purchase in enumerate(purchases, start=1):
            print(f"{idx}. [{purchase['plate']['region']}] {purchase['plate']['plate']} - {purchase['plate']['price']} so'm")

    def view_financials(self):
        purchases = self.data_handler.read_data("purchases.json")
        if not purchases:
            print("Hozircha hech qanday xarid mavjud emas.")
            return
        total_income = sum(purchase['plate']['price'] for purchase in purchases)
        print(f"Umumiy daromad: {total_income:,} so'm")

    def select_region(self):
        while True:
            print("\nViloyatni tanlang:")
            for key, value in REGIONS.items():
                print(f"{key}: {value[0]} [{value[1]}]")
            region_choice = input("Tanlovingizni kiriting: ")
            if region_choice in REGIONS:
                selected_region = REGIONS[region_choice]
                print(f"Siz {selected_region[0]} viloyatini tanladingiz [{selected_region[1]}].")
                return selected_region[1]
            else:
                print("Noto'g'ri tanlov. Qayta urinib ko'ring.")

    @staticmethod
    def is_valid_plate(plate):
        pattern = r'^[A-Z]{3}\d{3}$|^\d{3}[A-Z]{3}$|^[A-Z]{1,2}\d{3}[A-Z]{1}$|^[A-Z]{1}\d{3}[A-Z]{1,2}$|^\d{3}[A-Z]{1,2}$'
        return bool(re.match(pattern, plate))

class UserPanel(Panel):
    def buy_plate(self):
        plates = self.data_handler.read_data("plates.json")
        if not plates:
            print("Hozircha raqamlar mavjud emas.")
            return
        self.view_plates()
        while True:
            try:
                plate_id = int(input("Sotib olish kerak bo'lgan raqam ID-sini kiriting: ")) - 1
                if 0 <= plate_id < len(plates):
                    break
                else:
                    print("Noto'g'ri ID.")
            except ValueError:
                print("Iltimos, raqam ID-sini to'g'ri kiriting.")
        name = input("Ismingizni kiriting: ")
        phone_number = str(input("Telefon raqamingizni kiriting: +"))
        while len(str(phone_number)) != 12 or not str(phone_number).isdigit():
            print("Telefon raqami noto'g'ri. Qayta urinib ko'ring.")
            phone_number = input("Telefon raqamingizni kiriting: +")
        address = input("Manzilingizni kiriting: ")
        while True:
            card_number = str(input("Plastik karta raqamingizni kiriting (16 ta son): "))
            if len(card_number) == 16 and card_number.isdigit():
                break
            else:
                print("Karta raqami noto'g'ri. Qayta urinib ko'ring.")
        purchases = self.data_handler.read_data("purchases.json")
        purchases.append({"name": name, "phone": phone_number, "address": address, "plate": plates[plate_id]})
        self.data_handler.write_data("purchases.json", purchases)
        plates.pop(plate_id)
        self.data_handler.write_data("plates.json", plates)
        print("Raqam muvaffaqiyatli sotildi.")

    def view_purchases(self):
        purchases = self.data_handler.read_data("purchases.json")
        if not purchases:
            print("Hozircha hech qanday xarid mavjud emas.")
            return
        print("\nXaridlar tarixi:")
        for idx, purchase in enumerate(purchases, start=1):
            print(f"{idx}. Xaridor: {purchase['name']}, Telefon: +{purchase['phone']}, Manzil: {purchase['address']}, Raqam: [{purchase['plate']['region']}] {purchase['plate']['plate']} - {purchase['plate']['price']} so'm")

def main_menu():
    admin = AdminPanel()
    user = UserPanel()
    while True:
        print("\nAsosiy menyu:\n1. Admin panel\n2. Foydalanuvchi panel\n3. Chiqish")
        choice = input("Tanlovingizni kiriting: ")
        if choice == "1":
            while True:
                print("\nAdmin panel:\n1. Raqam qo'shish\n2. Raqamlarni ko'rish\n3. Raqamni o'chirish\n4. Raqamni tahrirlash\n5. Sotilgan raqamlarni ko'rish\n6. Buxgalteriya\n7. Asosiy menyuga qaytish")
                admin_choice = input("Tanlovingizni kiriting: ")
                if admin_choice == "1":
                    admin.add_plate()
                elif admin_choice == "2":
                    admin.view_plates()
                elif admin_choice == "3":
                    admin.remove_plate()
                elif admin_choice == "4":
                    admin.edit_plate()
                elif admin_choice == "5":
                    admin.view_sold_plates()
                elif admin_choice == "6":
                    admin.view_financials()
                elif admin_choice == "7":
                    break
                else:
                    print("Noto'g'ri tanlov. Qayta urinib ko'ring.")
        elif choice == "2":
            while True:
                print("\nFoydalanuvchi panel:\n1. Raqamlarni ko'rish\n2. Raqam sotib olish\n3. Xarid tarixini ko'rish\n4. Asosiy menyuga qaytish")
                user_choice = input("Tanlovingizni kiriting: ")
                if user_choice == "1":
                    user.view_plates()
                elif user_choice == "2":
                    user.buy_plate()
                elif user_choice == "3":
                    user.view_purchases()
                elif user_choice == "4":
                    break
                else:
                    print("Noto'g'ri tanlov. Qayta urinib ko'ring.")
        elif choice == "3":
            print("Dasturdan chiqildi.")
            break
        else:
            print("Noto'g'ri tanlov. Qayta urinib ko'ring.")

if __name__ == "__main__":
    main_menu()
