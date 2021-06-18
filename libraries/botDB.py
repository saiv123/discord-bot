import re
import ast
import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('botDB.db')