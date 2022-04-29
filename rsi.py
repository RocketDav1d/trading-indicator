import requests
import csv
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJsZW1vbi5tYXJrZXRzIiwiaXNzIjoibGVtb24ubWFya2V0cyIsInN1YiI6InVzcl9xeUdQUkNDOTlZTEh3blFUbnlscURjblB5ZHpzTnNac0w5IiwiZXhwIjoxNjU2MzE1NzA4LCJpYXQiOjE2NTExMzE3MDgsImp0aSI6ImFwa19xeUdrSzAwODhjc1BQQlcxWFdOODF0YlAxazYwOHFuMmI5IiwibW9kZSI6InBhcGVyIn0.wQeyC2Zot9CxMFpmTOvcTE1mC_RmPJGh5bNo554zkpA"

payload = {
    # change this later so dates are increasing everyday
    # use datetime module from python
}


request = requests.get("https://data.lemon.markets/v1/ohlc/d1/?isin=US0231351067&from=2022-03-01&to=2022-04-26", 
                       headers={"Authorization": "Bearer " + API_KEY})
request = request.json()
results = request["results"]


def sell_stock():
    pass

def buy_stock():
    pass




data = []
window_length = 14
window = []
gains = []
losses = []
output = []

prev_avg_gain = None
prev_avg_loss = None


for dict in results:
    data.append(dict["c"])


#test values
# with open('wilder-rsi-data.csv', 'r') as file:
#     reader = csv.reader(file)
#     header = next(reader)  # skip the header
#     data = [row[1] for row in list(reader)]
# data = list(map(float, data))


for i, price in enumerate(data):
    if i == 0:
        window.append(price)
        output.append([i+1, price, 0, 0, 0, 0, 0])
        continue

    difference = round(data[i] - data[i-1], 2)
    # print(i)
    # print(difference)

    if difference > 0:
        gain = difference
        loss = 0
    elif difference < 0:
        gain = 0
        loss = abs(difference)
    else:
        gain = 0
        loss = 0

    gains.append(gain)
    losses.append(loss)
    # print("gains: ")
    # print(gains)
    # print("losses: ")
    # print(losses)


    if i < window_length:
        window.append(price)
        output.append([i+1, price, gain, loss, 0, 0, 0])
        continue

# calculate  for first gain
    if i == window_length:
        avg_gain = sum(gains) / len(gains)
        avg_loss = sum(losses) / len(losses)

    else:
        avg_gain = (prev_avg_gain * (window_length - 1) + gain) / window_length
        avg_loss = (prev_avg_loss * (window_length - 1) + loss) / window_length

    prev_avg_gain = avg_gain
    prev_avg_loss = avg_loss

    # print("gain")
    # print(i , gain)
    # print("avg_gain")
    # print(i , avg_gain)
    # print("prev_avg_gain")
    # print(i , prev_avg_gain)
    avg_gain = round(avg_gain, 2)
    avg_loss = round(avg_loss, 2)
    prev_avg_gain = round(prev_avg_gain, 2)
    prev_avg_loss = round(prev_avg_loss, 2)


    # calculate RS and RSI (relative strenght index)
    rs = round(avg_gain / avg_loss, 2)
    rsi = round(100 - (100 / (1 + rs)), 2)

    # update window "rolling average"
    window.append(price)
    window.pop(0)
    gains.pop(0)
    losses.pop(0)

    # Save data
    output.append([i+1, price, gain, loss, avg_gain, avg_loss, rsi])
    

# print(output)
rsi_s = []

for stock in output:
    rsi = stock[6]
    rsi_s.append(rsi)

fake_data = 75
rsi_s.append(fake_data)

rsi_score = 0


for i, rsi in enumerate(rsi_s):
    x = rsi_s[i]
    if x > 70:
        if rsi_s[i-1] > rsi_s[i]:
            print(rsi)
            print("Austritt overbought")
            
        if rsi_s[i-1] < rsi_s[i]:
            print(rsi)
            print("Eintritt overbought")
    if x < 30:
        if rsi_s[i-1] > rsi_s[i]:
            print(rsi)
            print("Eintritt oversold")
        if rsi_s[i-1] < rsi_s[i]:
            print(rsi)
            print("Austrit oversold")





# save output in a csv file
with open("wilder-rsi-output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(output)