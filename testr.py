import sqlite3
import requests

#create database and tables

def init_db():     
    with sqlite3.connect('assets.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS trans (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          coin_name TEXT,
                          quantity REAL,
                          purchase_price REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS balances (
                          coin_name TEXT PRIMARY KEY,
                          total_quantity REAL)''')
        conn.commit()

#add transaction to the database and update balances

def add_trans(coin_name, quantity, purchase_price):
    with sqlite3.connect('assets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trans (coin_name, quantity, purchase_price) VALUES (?, ?, ?)",
                       (coin_name, quantity, purchase_price))
        conn.commit()
        update_balances()

# balances function

def update_balances():
    with sqlite3.connect('assets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT coin_name, SUM(quantity) FROM trans GROUP BY coin_name")
        balances= cursor.fetchall()

        for coin, total_quantity in balances:
            cursor.execute("INSERT OR REPLACE INTO balances (coin_name, total_quantity) VALUES (?, ?)",
                           (coin, total_quantity))          
        conn.commit()

#list all transactions function

def get_trans():
    with sqlite3.connect('assets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trans")
        return cursor.fetchall()

#total balance

def get_total_balance():
    with sqlite3.connect('assets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT coin_name, SUM(quantity) FROM trans GROUP BY coin_name")
        balances = cursor.fetchall()
        return balances

#get balances function"""

def get_balances():
    with sqlite3.connect('assets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM balances")
        balances = cursor.fetchall()
        return balances if balances else []


#get average price of coins

def get_avg():
    with sqlite3.connect('assets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT coin_name, SUM(quantity * purchase_price) / SUM(quantity) FROM trans GROUP BY coin_name")
        avg_price = cursor.fetchall()
        return avg_price if avg_price else []
    
#check balances function
def check_balances():       
    with sqlite3.connect('assets.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM balances")
        balances = cursor.fetchall()
        if balances:
            print("\nbalans:")
            for row in balances:
                print(row)
        else:
            print("\nFU") 

# GET ACTUAL PRICES COINGECKO API
def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,trust-wallet-token,solana,thorchain,the-open-network", 
        "vs_currencies": "usd"  
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    prices = {}
    for coin_id in data:
        price = data[coin_id]['usd']
        prices[coin_id] = price
    return prices

# GET TOTAL BALANCE AND PRICES
def get_balance_and_prices():
    balances = get_total_balance()  
    prices = get_prices()  

    print("\nОбщий баланс по криптовалютам:")
    for balance in balances:
        coin = balance[0] 
        total_quantity = balance[1]  
        coin_id = coin.lower()


        if coin == "BTC":
            coin_id = "bitcoin"
        elif coin == "RUNE":
            coin_id = "thorchain"
        elif coin == "SOL":
            coin_id = "solana"
        elif coin == "TON":
            coin_id = "the-open-network"
        elif coin == "TWT":
            coin_id = "trust-wallet-token"

        price = prices.get(coin_id)  # GET PRICE FROM coingecko
        if price is not None:
            total_value = total_quantity * price
            print(f"{coin.capitalize()}: {total_value:.2f} USD (Баланс: {total_quantity:.2f} монет, Цена: ${price:.2f})")

def main():
    init_db()
    while True:
        print("\n1. Add new transaction")
        print("2. Show all transactions")
        print("3. Show coin balances")
        print("4. Show balance and prices")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            coin_name = input("Enter coin name: ")
            quantity = float(input("Enter quantity: "))
            purchase_price = float(input("Enter purchase price: "))
            add_trans(coin_name, quantity, purchase_price)
            print("Transaction added successfully.")

        elif choice == '2':
            transaction = get_trans() 
            print(transaction)
        
        elif choice == '3':
            balances = get_balances()
            avg_price = get_avg()
            if balances:
                print("\nCurrent balance by coins:")
                for coin, total in balances:
                    print(f"{coin}: {total}")
            else:
                print("No transactions yet.")
            if avg_price:   
                print("\nAverage purchase price:")
                for coin, avg in avg_price:
                    print(f"{coin}: {avg}")
            else:
                print("No transactions yet.")

        elif choice == '4':
            get_balance_and_prices()

        elif choice == '6':
            print("Exiting...")
            break

if __name__ == '__main__':
    main()