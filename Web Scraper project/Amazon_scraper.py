import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Scrape karo
print("Loading...")
url = "https://books.toscrape.com/"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

books = []
for book in soup.find_all("article", class_="product_pod"):
    name = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    rating = book.p["class"][1].split("-")[-1]
    books.append([name, price, rating])

df = pd.DataFrame(books, columns=["Book Name", "Price", "Rating"])
df.to_csv("products.csv", index=False)

# Statistics
total = len(df)
five = len(df[df['Rating']=='Five'])
four = len(df[df['Rating']=='Four'])
three = len(df[df['Rating']=='Three'])
two = len(df[df['Rating']=='Two'])
one = len(df[df['Rating']=='One'])

# Popup message
msg = f"""
╔════════════════════════════════════════╗
║     ✅ SCRAPING COMPLETE! ✅           ║
╠════════════════════════════════════════╣
║  📚 Total Books: {total}                         ║
║                                          ║
║  ⭐ RATINGS:                             ║
║     ★★★★★ : {five} books                      ║
║     ★★★★  : {four} books                      ║
║     ★★★   : {three} books                      ║
║     ★★    : {two} books                       ║
║     ★     : {one} books                       ║
║                                          ║
║  💾 Saved to: products.csv              ║
╚════════════════════════════════════════╝

📖 FIRST 5 BOOKS:
"""

for i in range(min(5, total)):
    msg += f"\n{i+1}. {books[i][0][:40]}"
    msg += f"\n   💰 {books[i][1]}  ⭐ {books[i][2]}"
    msg += f"\n   {'-'*40}"

# Show popup
root = tk.Tk()
root.withdraw()
messagebox.showinfo("📊 Web Scraping Results", msg)
root.destroy()

print("✅ Done! Popup window mein result dikhega")
print(f"📊 Total {total} books scraped")
print("💾 CSV file saved!")