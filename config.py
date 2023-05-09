import json

BOT_TOKEN = '5184253039:AAFVk7T8jKedgqu36N5E3bIELcYrnByfnFg'
admin_id = '484502159'

with open("faq.json", "r", encoding='utf8') as read_file:
    data = json.load(read_file)
    categories = []
    for el in data['faq']:
        categories.append(el['category'])