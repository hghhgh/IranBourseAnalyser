# calculating Profit should be corrected later
def getProfitValue(Maximum, Minimum, ClosePrice, LastPrice, buyidx, sellidx):
    # TODO

    # به نرخ تورم هم بستگی داره در اصل
    # به کارمزد کارگزاری بستگی داره

    ProfitPrice = ClosePrice[buyidx + sellidx]['v'] - ClosePrice[buyidx]['v']
    ProfitPercent = int(round(ProfitPrice / ClosePrice[buyidx]['v'] * 100))

    return ProfitPrice, ProfitPercent
