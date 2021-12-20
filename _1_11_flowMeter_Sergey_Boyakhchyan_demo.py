import  time
amount = 0
while True:
    file = open("flowMeter.txt",'w')
    file.write(str(amount))
    file.close()
    time.sleep(1)
    amount +=20
