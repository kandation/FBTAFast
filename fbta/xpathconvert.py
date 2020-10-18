from parsel import Selector

x = Selector('')
k = x.xpath('//div[contains(@id, "month_") and not(contains(@id, "_more_"))]')
print(k.)