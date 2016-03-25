import MyLibs as libs
from bs4 import NavigableString


urls = libs.readcsv("round2.csv")

patient_leaflet_out = "/home/vhdang/CBG/PIL/"
smpc_file_out = "/home/vhdang/CBG/SmPC/"

# libs.write_data("CMG_Med_Info.csv", ["Authorisation Number", "ATC", "Product Name" , "Active substance (EN)", "Active substances", "Excipients", "Pharmaceutical form",
#                 "Route of Administration", "Marketing authorisation number", "Country of origin" , "Authorisation date",
#                 "Marketing authorisation holder", "Patient Information Leaflet File", "SmPC File", "URL"], 'w')
i = 1
for r in urls[1:]:
    link = r[3]
    product_name = r[1]
    auth_no = r[0]
    print(auth_no)
    print(str(i) + ". " + link)
    i +=1
    data = libs.fetch_data(link)
    if data is None:
        libs.write_data("ignore.csv", r)
        continue
    soup = libs.html_parser(data)

    first_tab = soup.find("div", id="first")

    active_substance = None
    excipients = None
    pharmaceutical_form = None
    route_of_administration = None
    patient_info_leaflet = None
    patient_leaflet_filename = None
    smpc = None
    smpc_filename = None

    if not isinstance(first_tab, NavigableString):
        if first_tab.findAll("div", attrs={"class": "downloads"}) is not None:

            for a in first_tab.find("div", attrs={"class": "downloads"}).findAll("a"):
                #print(a.getText())
                if a.getText().strip() == 'Patiëntenbijsluiter' or a.getText().strip() == 'Patient information leaflet':
                    patient_info_leaflet = a['href']
                    patient_leaflet_filename = patient_info_leaflet.split("/")[-1]
                    libs.download_file(patient_info_leaflet, patient_leaflet_out)
                if a.getText().strip() == 'Samenvatting van de productkenmerken (SmPC)' or a.getText().strip() == 'Summary of the Product Characteristics (SmPC)':
                    smpc = a["href"]
                    smpc_filename = smpc.split("/")[-1]
                    libs.download_file(smpc, smpc_file_out)

        info = first_tab.find("div", attrs={'class': 'info hidden-xs'}).find("tbody")
        for tr in info.findAll("tr"):

            if tr.findAll("td")[0].getText().strip() == 'Active substance:' or tr.findAll("td")[0].getText().strip() == 'Werkzame stof:':
                active_substance = tr.findAll("td")[1].getText().split("\n")
                active_substance = '#'.join([x for x in active_substance if x != ''])

            if tr.findAll("td")[0].getText().strip() == 'Excipients:' or tr.findAll("td")[0].getText().strip() == 'Hulpstoffen:':
                excipients = tr.findAll("td")[1].getText().split("\n")
                excipients = '#'.join([x for x in excipients if x != ''])

            if tr.findAll("td")[0].getText().strip() == 'Pharmaceutical form:' or tr.findAll("td")[0].getText().strip() == 'Farmaceutische vorm:':
                pharmaceutical_form = tr.findAll("td")[1].getText().split("\n")
                pharmaceutical_form = '#'.join([x for x in pharmaceutical_form if x != ''])

            if tr.findAll("td")[0].getText().strip() == 'Route of Administration:' or tr.findAll("td")[0].getText().strip() == 'Toedieningsweg:':
                route_of_administration = tr.findAll("td")[1].getText().split("\n")
                route_of_administration = '#'.join([x for x in route_of_administration if x != ''])

    second_tab = soup.find("div", id="second")
    procedure_number = None
    authorisation_number = None
    county_of_origin = None
    atc = []
    authorisation_date = None
    authorisation_holder = None
    if not isinstance(second_tab, NavigableString):
        for tr in second_tab.find("table").findAll("tr"):
            if tr.findAll('td')[0].getText().strip() == 'Procedure number:' or tr.findAll('td')[0].getText().strip() == 'Procedurenummer:':
                procedure_number = tr.findAll('td')[1].getText().strip()

            if tr.findAll('td')[0].getText().strip() == 'Marketing authorisation number:' or tr.findAll('td')[0].getText().strip() == 'Registratienummer:':
                authorisation_number = tr.findAll('td')[1].getText().strip()

            if tr.findAll('td')[0].getText().strip() == 'ATC:':
                s_atc = tr.findAll("td")[1].getText().split("\n")
                s_atc = [x for x in s_atc if x != '']
                for x in s_atc:
                    atc.append([x.split("-")[0].strip(), x.split("-")[1].strip()])

            if tr.findAll('td')[0].getText().strip() == 'Country of origin:' or tr.findAll('td')[0].getText().strip() ==  'Land van herkomst:':
                county_of_origin = tr.findAll("td")[1].getText().strip()

            if tr.findAll('td')[0].getText().strip() == 'Authorisation date:' or tr.findAll('td')[0].getText().strip() ==  'Datum verstrekking handelsvergunning:':
                authorisation_date = tr.findAll("td")[1].getText().strip()

            if tr.findAll('td')[0].getText().strip() == 'Marketing authorisation holder:' or tr.findAll('td')[0].getText().strip() == 'Handelsvergunning houder:':
                authorisation_holder = tr.findAll("td")[1].getText().strip()

            if len(tr.findAll("td")[0].getText()) == 0:
                authorisation_holder += " # " + tr.findAll("td")[1].getText().strip()

    if len(atc) > 0:
        for x in atc:
            libs.write_data("CMG_Med_Info.csv", [auth_no, x[0], product_name, x[1], active_substance, excipients, pharmaceutical_form,
                route_of_administration, authorisation_number, county_of_origin, authorisation_date,
                authorisation_holder, patient_leaflet_filename, smpc_filename, link])
    else:
        libs.write_data("CMG_Med_Info.csv", [auth_no, None, product_name, None, active_substance, excipients, pharmaceutical_form,
            route_of_administration, authorisation_number, county_of_origin, authorisation_date,
            authorisation_holder, patient_leaflet_filename, smpc_filename, link])

