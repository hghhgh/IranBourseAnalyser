# calculating Profit should be corrected later
def getSingleNamadProfitValue(Dates, ClosePrice, LastPrice, buyidx, sellidx):
    # TODO

    # به نرخ تورم هم بستگی داره در اصل
    # به کارمزد کارگزاری بستگی داره

    ProfitPrice = ClosePrice[buyidx + sellidx] - ClosePrice[buyidx]
    ProfitPercent = int(round(ProfitPrice / ClosePrice[buyidx] * 100))

    return ProfitPrice, ProfitPercent


# calculating Profit should be corrected later
def getBascketOfSharesProfitValue(Dates, ClosePrice, LastPrice, buyidx, sellidx):
    # TODO

    # به نرخ تورم هم بستگی داره در اصل
    # به کارمزد کارگزاری بستگی داره

    ProfitPrice = 0
    ProfitPercent = 0

    return ProfitPrice, ProfitPercent
