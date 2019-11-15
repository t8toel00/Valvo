import time
y = 1
while y is 1:
    print("y on 1")
    time.sleep(2)
    y = 2

while y is 2:
    print("y on 2")
    time.sleep(2)
    y = 0

while y is not 1:
    print("y ei ole 1")
    y = 0