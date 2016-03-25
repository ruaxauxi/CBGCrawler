import MyLibs as libs
from bs4 import NavigableString


def get_med_link():
    url_base = "http://db.cbg-meb.nl/ords/f?p=111:2:0:SEARCH:NO:RP:P2_AS_PROD,P2_AS_RVGNR,P2_AS_EU1,P2_AS_EU2,P2_AS_ACTSUB,P2_AS_INACTSUB,P2_AS_NOTINACT,P2_AS_ADDM,P2_AS_APPDATE,P2_AS_APPDATS,P2_AS_ATC,P2_AS_PHARM,P2_AS_MAH,P2_AS_ROUTE,P2_AS_AUTHS,P2_AS_TGTSP,P2_AS_INDIC,P2_AS_TXTF,P2_AS_TXTI,P2_AS_TXTC,P2_OPTIONS,P2_RESPAGE,P2_RESCOUNT,P2_SORT,P2_RESPPG:,,,,,,N,N,,,,,,,,,,,,,,"

    for page in range(1, 30):
        print("processing page " + str(page) + '...')
        url = url_base + str(page) + ",21705,PRODA,1000"
        data = libs.fetch_data(url)
        soup = libs.html_parser(data)
        result = soup.find("table", id="report_R10876586154639965")
        if result is not None:
            for tr in result.findAll("tr"):
                if len(tr.findAll("td")) >2:
                    tds = tr.findAll("td")
                    libs.write_data("CBG_Med_Links.csv", [tds[0].getText().strip(), tds[1].getText().strip(),
                                    tds[2].getText().strip(), "http://db.cbg-meb.nl/ords/" + tds[1].find("a")['href']])


libs.write_data("CBG_Med_Links.csv", ["Authorisation Number", "Product name", "ATC", "Link"], "w")
get_med_link()
