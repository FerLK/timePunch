
from datetime import datetime, timedelta

x = datetime.now()

a = x.strftime("%B") + " " + str(x.day)

b = datetime.now().strftime("%x")

print(x.hour)
print(x)
print("isso", x.strftime("%x"))
print(x.day)
print(x.time())
print(x.strftime("%A"))
print(x.strftime("%B"))

print(a)

print(datetime.utcnow)

print(str(datetime.now()))
print(str(datetime.now().strftime("%x")))
print(str(datetime.now().strftime("%X")))

now = datetime.now()
now = now - timedelta(hours=8, minutes=23, seconds=10)
print(x - now)

print((datetime.now().strftime("%x")))

print(str(datetime.now().strftime("%X")))

time = datetime.now() - timedelta(hours=8, minutes=23, seconds=10)
print(time.strftime("%X"))
