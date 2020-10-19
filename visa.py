import requests

r = requests.get("https://algeria.blsspainvisa.com/english/book_appointment.php")
print(r.content)
