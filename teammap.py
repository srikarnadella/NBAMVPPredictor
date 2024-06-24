import requests
import time
from bs4 import BeautifulSoup
from openpyxl import Workbook

years = list(range(100, 2022))

url_temp = "https://www.basketball-reference.com/awards/awards_{}.html"

# Data to write into Excel
data = [
    {"Abbreviation": "ATL", "Name": "Atlanta Hawks"},
    {"Abbreviation": "BRK", "Name": "Brooklyn Nets"},
    {"Abbreviation": "BKN", "Name": "Brooklyn Nets"},
    {"Abbreviation": "BOS", "Name": "Boston Celtics"},
    {"Abbreviation": "CHA", "Name": "Charlotte Bobcats"},
    {"Abbreviation": "CHH", "Name": "Charlotte Hornets"},
    {"Abbreviation": "CHO", "Name": "Charlotte Hornets"},
    {"Abbreviation": "CHI", "Name": "Chicago Bulls"},
    {"Abbreviation": "CLE", "Name": "Cleveland Cavaliers"},
    {"Abbreviation": "DAL", "Name": "Dallas Mavericks"},
    {"Abbreviation": "DEN", "Name": "Denver Nuggets"},
    {"Abbreviation": "DET", "Name": "Detroit Pistons"},
    {"Abbreviation": "GSW", "Name": "Golden State Warriors"},
    {"Abbreviation": "HOU", "Name": "Houston Rockets"},
    {"Abbreviation": "IND", "Name": "Indiana Pacers"},
    {"Abbreviation": "LAC", "Name": "Los Angeles Clippers"},
    {"Abbreviation": "LAL", "Name": "Los Angeles Lakers"},
    {"Abbreviation": "MEM", "Name": "Memphis Grizzlies"},
    {"Abbreviation": "MIA", "Name": "Miami Heat"},
    {"Abbreviation": "MIL", "Name": "Milwaukee Bucks"},
    {"Abbreviation": "MIN", "Name": "Minnesota Timberwolves"},
    {"Abbreviation": "NJN", "Name": "New Jersey Nets"},
    {"Abbreviation": "NOH", "Name": "New Orleans Hornets"},
    {"Abbreviation": "NOP", "Name": "New Orleans Pelicans"},
    {"Abbreviation": "NOK", "Name": "New Orleans/Oklahoma City Hornets"},
    {"Abbreviation": "NYK", "Name": "New York Knicks"},
    {"Abbreviation": "OKC", "Name": "Oklahoma City Thunder"},
    {"Abbreviation": "ORL", "Name": "Orlando Magic"},
    {"Abbreviation": "PHI", "Name": "Philadelphia 76ers"},
    {"Abbreviation": "PHX", "Name": "Phoenix Suns"},
    {"Abbreviation": "PHO", "Name": "Phoenix Suns"},
    {"Abbreviation": "POR", "Name": "Portland Trail Blazers"},
    {"Abbreviation": "SEA", "Name": "Seattle SuperSonics"},
    {"Abbreviation": "SAC", "Name": "Sacramento Kings"},
    {"Abbreviation": "SAS", "Name": "San Antonio Spurs"},
    {"Abbreviation": "TOR", "Name": "Toronto Raptors"},
    {"Abbreviation": "UTA", "Name": "Utah Jazz"},
    {"Abbreviation": "VAN", "Name": "Vancouver Grizzlies"},
    {"Abbreviation": "WAS", "Name": "Washington Wizards"},
    {"Abbreviation": "WSB", "Name": "Washington Bullets"}
]

# Create a new Workbook and select the active sheet
wb = Workbook()
ws = wb.active

# Set the column headers
ws.append(["Abbreviation", "Name"])

# Iterate over the data and write to the spreadsheet
for item in data:
    ws.append([item["Abbreviation"], item["Name"]])

# Save the workbook
wb.save("teamabr.csv")

print("Excel file 'teams.xlsx' has been successfully created.")