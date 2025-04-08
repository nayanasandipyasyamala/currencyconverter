from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "458c2bf9af278a9f7ed4372e"
API_URL = "https://v6.exchangerate-api.com/v6/{458c2bf9af278a9f7ed4372e}/latest/{USD}"

currency_names = {
    "USD": "US Dollars", "INR": "Indian Rupees", "CAD": "Canadian Dollars", "EUR": "Euros", 
    "GBP": "British Pounds", "AUD": "Australian Dollars", "JPY": "Japanese Yen", "CNY": "Chinese Yuan", 
    "SGD": "Singapore Dollars", "CHF": "Swiss Francs", "BRL": "Brazilian Real", "MXN": "Mexican Peso", 
    "ZAR": "South African Rand", "KRW": "South Korean Won", "RUB": "Russian Ruble", "AED": "UAE Dirham", 
    "SEK": "Swedish Krona", "NZD": "New Zealand Dollar", "NOK": "Norwegian Krone", "DKK": "Danish Krone", 
    "MYR": "Malaysian Ringgit", "THB": "Thai Baht", "IDR": "Indonesian Rupiah", "PHP": "Philippine Peso", 
    "PLN": "Polish Zloty", "HUF": "Hungarian Forint", "CZK": "Czech Koruna", "TRY": "Turkish Lira", 
    "HKD": "Hong Kong Dollar", "ILS": "Israeli Shekel"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        amount = request.form["amount"]

        if from_currency != "select" and to_currency != "select" and amount:
            response = requests.get(API_URL.format(API_KEY, from_currency))
            if response.status_code == 200:
                exchange_rates = response.json()["conversion_rates"]
                converted_amount = float(amount) * exchange_rates.get(to_currency, 1)

                from_currency_name = currency_names.get(from_currency, from_currency)
                to_currency_name = currency_names.get(to_currency, to_currency)

                converted_text = f"Given {amount} {from_currency_name} is equal to {converted_amount:.2f} {to_currency_name}."
                return render_template("py.html", converted_text=converted_text, from_currency=from_currency, to_currency=to_currency, amount=amount)

    return render_template("py.html", converted_text=None, from_currency="select", to_currency="select", amount="")

if __name__ == "__main__":
    app.run(debug=True)
