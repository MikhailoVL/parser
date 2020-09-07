import browser_digger

if __name__ == "__main__":
    company = [
        "PD",
        "ZUO",
        "PINS",
        "ZM",
        "PVTL",
        "DOCU",
        "CLDR",
        "RUN"
    ]
    dig = browser_digger.Digger()
    for firm in company:
        ddd = dig.find_company(firm)
        if ddd:

            dig.download_his_data(firm)
            dig.news_last_to_file(firm)
            dig.add_new_column(firm)
        else:
            print("no such  cmpany")
            dig.url_()
