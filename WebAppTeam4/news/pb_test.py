from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Send an HTTP GET request to the URL
url = 'https://kurs.com.ua/bank/10-privatbank'
driver.get(url)

# Extract the page source after JavaScript has loaded
page_source = driver.page_source

# Parse the HTML content
soup = BeautifulSoup(page_source, 'html.parser')

# Find the table that contains the currency rates
table = soup.find('table', class_='table-course')

if table:
    # Initialize lists to store currency names, buy rates, and sell rates
    currencies = []
    buy_rates = []
    sell_rates = []

    # Find all table rows in the table body (excluding the header row)
    rows = table.find('tbody').find_all('tr')

    # Loop through the rows to extract data for the first 5 currencies
    for row in rows[:5]:
        # Find all table data cells in the row
        cells = row.find_all('td')

        if len(cells) >= 4:
            # Extract currency name, buy rate, and sell rate
            currency = cells[0].find('a').text.strip()
            buy_rate = cells[2].find('div', class_='course').text.strip()
            sell_rate = cells[3].find('div', class_='course').text.strip()

            # Append data to respective lists
            currencies.append(currency)
            buy_rates.append(buy_rate)
            sell_rates.append(sell_rate)

    # Print the results
    for i in range(5):
        print(f"Currency: {currencies[i]}")
        print(f"Buy Rate: {buy_rates[i]}")
        print(f"Sell Rate: {sell_rates[i]}")
        print()

else:
    print("Table not found on the webpage.")

# Close the WebDriver
driver.quit()
