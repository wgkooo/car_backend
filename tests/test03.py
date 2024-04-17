import datetime
import arrow
import calendar
# current_date = datetime.datetime.now().strftime("%Y-%m-%d")
# print(current_date)

now = arrow.now()

for i in range(0, 12):
    last_month = now.shift(months = 0 - i).strftime("%Y-%m-%d")
    print(last_month + ' ' + last_month[0:4] + ' ' + last_month[5:7] + ' ' + calendar.month_abbr[int(last_month[5:7])])


brand = 'bmw%'
print(brand[0: -1])
