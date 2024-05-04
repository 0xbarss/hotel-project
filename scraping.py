import requests
import tkinter as tk
from tkinter import Tk, ttk
from bs4 import BeautifulSoup

from utilities import *


class Scraper:
    def getHotels(city: str, checkIn: str, checkOut: str) -> BeautifulSoup:
        resp = requests.get(URL.format(city, city, city, CITIES[city], checkIn, checkOut, GROUP_ADULTS, NO_ROOMS, GROUP_CHILDREN), headers=HEADERS)
        bs = BeautifulSoup(resp.text, 'html.parser')
        hotels = bs.findAll('div', {'data-testid': 'property-card'})
        return hotels

    def createDataframe(hotels: BeautifulSoup) -> pd.DataFrame:
        data = []
        for hotel in hotels:
            name = hotel.find('div', {'data-testid': 'title'})
            name = name.text.strip() if name else NOTGIVEN
            address = hotel.find('span', {'data-testid': 'address'})
            address = address.text.strip() if address else NOTGIVEN
            distance = hotel.find('span', {'data-testid': 'distance'})
            distance = distance.text.strip() if distance else NOTGIVEN
            rating = hotel.find('span', {'class': 'a3332d346a'})
            rating = rating.text.strip() if rating else NOTGIVEN
            price = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
            price = int(price.text.strip().replace("TL\xa0", "").replace(",", "")) if price else NOTGIVEN
            data.append({TITLE: name,
                         ADDRESS: address,
                         DISTANCE: distance,
                         RATING: rating,
                         PRICE: price,
                         })
        return sortHotelData(pd.DataFrame(data).head(HOTEL_SCRAPING_COUNT)).head(HOTEL_DISPLAY_COUNT)
        
    def run(city: str, checkIn: str, checkOut: str) -> pd.DataFrame:
        hotels = Scraper.getHotels(city, checkIn, checkOut)
        df = Scraper.createDataframe(hotels)
        createCSVFile(df)
        return df
        

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Hotel Program")
        self.root.geometry("1024x768")

        ttk.Style().theme_use('clam')
        
        self.cities = list(CITIES.keys())
    
    def search(self):
        city = self.cityVar.get()
        checkIn = self.checkInVar.get()
        checkOut = self.checkOutVar.get()
        if not (city and checkIn and checkOut):
            self.warningVar.set(WARNING_MESSAGE_1)
            return
        if not (isDate(checkIn) and isDate(checkOut)):
            self.warningVar.set(WARNING_MESSAGE_1)
            return
        df = Scraper.run(city, checkIn, checkOut)
        if df.shape[0] == 0:
            self.warningVar.set(WARNING_MESSAGE_2)
            return
        self.warningVar.set("")
        for row in self.results.get_children():
            self.results.delete(row)
        for index in range(df.shape[0]):
            row = df.iloc[index]
            self.results.insert("", tk.END, iid=index, values=(row[TITLE], row[ADDRESS], row[DISTANCE], row[RATING], row[PRICE] if self.currencyVar.get() == TL else str(int(row[PRICE]/30))))
            self.results.column(index, anchor='center')

    def run(self):
        self.cityLabel = tk.Label(self.root, text="City:")
        self.cityLabel.grid(row=0, column=0, padx=5, pady=5)
        self.cityVar = tk.StringVar(value=self.cities[0])
        self.cityMenu = ttk.Combobox(self.root, textvariable=self.cityVar, values=self.cities)
        self.cityMenu.grid(row=0, column=1, padx=5, pady=5)

        self.checkInLabel = tk.Label(self.root, text="Check In:")
        self.checkInLabel.grid(row=1, column=0, padx=5, pady=5)
        self.checkInVar = tk.StringVar(self.root)
        self.checkInEntry = tk.Entry(self.root, textvariable=self.checkInVar)
        self.checkInEntry.grid(row=1, column=1, padx=5, pady=5)

        self.checkOutLabel = tk.Label(self.root, text="Check Out:")
        self.checkOutLabel.grid(row=2, column=0, padx=5, pady=5)
        self.checkOutVar = tk.StringVar(self.root)
        self.checkOutEntry = tk.Entry(self.root, textvariable=self.checkOutVar)
        self.checkOutEntry.grid(row=2, column=1, padx=5, pady=5)

        self.currencyVar = tk.StringVar(value=TL)
        self.tlButton = tk.Radiobutton(self.root, text=TL, variable=self.currencyVar, value=TL)
        self.euButton = tk.Radiobutton(self.root, text=EU, variable=self.currencyVar, value=EU)
        self.tlButton.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.euButton.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.warningVar = tk.StringVar(value="")
        self.warningLabel = tk.Label(self.root, textvariable=self.warningVar)
        self.warningLabel.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        self.searchButton = tk.Button(self.root, text="Search", command=self.search)
        self.searchButton.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.resultsFrame = tk.Frame(self.root)
        self.resultsFrame.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.results = ttk.Treeview(self.resultsFrame, show='headings', columns=(TITLE, ADDRESS, DISTANCE, RATING, PRICE), height=20)
        self.results.heading(TITLE, text=TITLE)
        self.results.heading(ADDRESS, text=ADDRESS)
        self.results.heading(DISTANCE, text=DISTANCE)
        self.results.heading(RATING, text=RATING)
        self.results.heading(PRICE, text=PRICE)
        self.results.grid(row=0, column=0, sticky="nsew")

        self.root.mainloop()
