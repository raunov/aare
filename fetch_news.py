# We need a python script to fetch the stock news headlines, attachments and news content urls from a json feed for a specific stock and for a specific time period.
# Then we will need to store the news content and all attachments in /documents folder. The news text file contains: news date, news title, news content, news attachments and news url.
# Naming convention for the files is:
# yyyy-mm-dd-<stock_name>-<news_title>-<attachment_name>-<language_code>.txt|pdf|docx|html
# the url for extracting data is in format: https://api.news.eu.nasdaq.com/news/query.action?displayLanguage=et&timeZone=Europe%2FTallinn&dateMask=yyyy-MM-dd+HH%3Amm%3Ass+Z&limit=25&countResults=true&start=0&fromDate=1682899200000&toDate=1684195200000&company=LHV+Group
# the content for the json file is in format:
"""
{
  "results" : {
    "item" : [ {
      "disclosureId" : 1228103,
      "categoryId" : 301,
      "headline" : "LHV Groupi tulemused aprillis 2023",
      "language" : "et",
      "languages" : [ "et", "en" ],
      "company" : "LHV Group",
      "cnsCategory" : "Börsiteade",
      "messageUrl" : "https://view.news.eu.nasdaq.com/view?id=bb8c766b961aa06099edab43bee31861e&lang=et&src=listed",
      "releaseTime" : "2023-05-16 08:00:00 +0300",
      "published" : "2023-05-16 08:00:00 +0300",
      "market" : "Main Market, Tallinn",
      "cnsTypeId" : "25",
      "attachment" : [ {
        "mimetype" : "application/pdf",
        "fileName" : "LHV Group 2023-04-ET.pdf",
        "attachmentUrl" : "https://attachment.news.eu.nasdaq.com/a8a6a0ce34a0f4d647a74a41270a22184"
      } ]
    } ]
  },
  "count" : 1
}

"""

import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup
import html2markdown
import htmltabletomd

def fetch_nasdaqbaltic_news(company, fromDate, toDate):
    # Convert fromDate and toDate to Unix timestamps
    fromDate_unix = int(fromDate.timestamp() * 1000)
    toDate_unix = int(toDate.timestamp() * 1000)

    # Fetch JSON data from the URL
    url = f"https://api.news.eu.nasdaq.com/news/query.action?displayLanguage=et&timeZone=Europe%2FTallinn&dateMask=yyyy-MM-dd+HH%3Amm%3Ass+Z&limit=25&countResults=true&start=0&fromDate={fromDate_unix}&toDate={toDate_unix}&company={company}"
    response = requests.get(url)
    data = response.json()

    # Create /documents folder if it doesn't exist
    if not os.path.exists("documents"):
        os.makedirs("documents")

    # Iterate through the items in the JSON data
    for item in data["results"]["item"]:
        # Extract relevant information
        date = datetime.strptime(item["published"], "%Y-%m-%d %H:%M:%S %z").strftime("%Y-%m-%d")
        stock_name = item["company"].replace(" ", "_")
        news_title = item["headline"].replace(" ", "_")
        language_code = item["language"]
        message_url = item["messageUrl"]
        disclosure_id = item["disclosureId"]

        # get the message content from the messageUrl.
        # get only the text from the message contentm, which is between <p> and </p> tags
        # example:                 <h3 class='gnw_heading'>LHV Groupi tulemused aprillis 2023</h3><h4 class='gnw_subhead'></h4><p>LHV jaoks iseloomustasid aprillikuud kasvanud intressitulud ja kindlustuse jõudmine kasumisse, aga ka tihe konkurents pangandusturul ning ebaselgus majanduskeskkonna edasise arengu osas.</p>       <p>AS-i LHV Group konsolideeritud hoiused vähenesid aprillis 70 miljoni euro võrra maksevahendajate hoiuste vähenemise tõttu. Tavaklientide hoiused kasvasid 59 miljoni euro võrra. Konsolideeritud laenuportfell kasvas kuuga 18 miljoni euro võrra, sealhulgas ettevõtete laenud 13 miljoni euro võrra ning jaelaenud 5 miljoni euro võrra. LHV juhitud fondide maht kasvas aprillis 7 miljoni euro võrra. Aprillis töödeldi 3,5 miljonit finantsvahendajatest klientidega seotud makset.</p>       <p>AS LHV Groupi konsolideeritud puhaskasum oli aprillikuus 12,0 miljonit eurot. AS LHV Pank teenis 11,4 miljonit eurot puhaskasumit. AS-i LHV Varahaldus kahjum oli 15 tuhat eurot. AS LHV Kindlustus jõudis kasumisse, teenides 110 tuhat eurot puhaskasumit, ning LHV Ühendkuningriigi tütarettevõtte puhaskasum ulatus 0,7 miljoni euroni.</p>       <p>Pangaklientide arv kasvas aprillis 3600 võrra, laenuklientide puhul on märgata mõningast aktiveerumist. Samal ajal kui intressitulud ületasid plaanitut, püsis laenuportfelli kvaliteet endiselt heal tasemel. Aprillis tuli LHV turule kampaaniapakkumisega energiatõhusatele kodudele mõeldud Rohelisele kodulaenule, mis on aidanud kasvatada Rohelise kodulaenu osakaalu 20%-ni uutest lepingutest. Pank on pannud fookuse ka hoiustele ning maksab tähtajalistele hoiusele keskpanga intressimäärale sarnast intressi, aprillis tõstis pank intressi ka suuremate nõudmiseni hoiuste summadega ettevõtete jaoks. Panga kulusid mõjutas plaanitust kõrgem hoiuse tagatisfondi maksemäär.</p>       <p>LHV Ühendkuningriigi tütarettevõtte jaoks kulges aprill ettevalmistuste tähe all pangaks saamisel. 2. mail sai ettevõte ÜK finantsjärelevalve asutuselt PRA pangalitsentsi, mis võimaldab äritegevuse üleviimise plaanidega hoogsalt edasi liikuda. Tulevikus tegutseb ettevõte uue nimega LHV Bank Limited litsentseeritud pangana. Kui hetkel on LHV Banki klientideks finantsvahendajad ja VKE laenukliendid, siis juba aasta jooksul plaanib ettevõte asuda kaasama hoiuseid ja tulla välja pakkumisega e-kaupmeestele.</p>       <p>Varahaldus sai aprillis juurde 300 aktiivset pensioni II samba klienti. Kuigi turgudel oli tegemist tagasihoidliku kuuga, püsis suuremate fondide tootlus kerges plussis. Suurimate fondide M, L ja XL tootluseks kujunes aprillis vastavalt 0,4%, 0,1% ja 0,4%. Pensionifond Indeks alanes 0,8%, pensionifond Roheline kaotas väärtuses 4,6%.</p>       <p>LHV Kindlustuse tugev kindlustustehniline tulemus toetas ettevõtte puhaskasumisse jõudmist. Aprilli lõpu seisuga on kindlustusel 221 tuhat kehtivat kindlustuspoliisi ning enam kui 158 tuhat klienti. Aprillis sõlmiti 12 600 kindlustuslepingut mahuga 3,4 miljonit eurot ning kahjujuhtumeid hüvitati summas 1,1 miljonit eurot. Paranenud efektiivsusnäitajad toetavad finantsplaanis püsimist.</p>       <p>LHV Groupi kapitaliseeritus on rekordtaseme lähedal ning finantsplaan püsib. Samas on majanduskeskkonna edasiste arengute nähtavus keskmisest madalam.</p>       <p>AS-i LHV Group aruanded on saadaval aadressil: <a href="https://www.globenewswire.com/Tracker?data=BHAWl-DdBYuNxHrxlJxGFEY9mGrmniMti0inLwa3n_eL8BKrLKk6Z9y9QOJ8bGQfx-8nW5GXbgI52azA4Cv3N5TfD35ke1j5MxiZNrltmklaqLQOFnMsyzvN4njDOozo" rel="nofollow" target="_blank">https://investor.lhv.ee/aruanded</a>.</p>       <p><em>LHV Group on suurim kodumaine finantskontsern ja kapitali pakkuja Eestis. LHV Groupi peamised tütarettevõtted on LHV Pank, LHV Varahaldus ja LHV Kindlustus. Grupi ettevõtetes töötab üle 930 inimese. LHV pangateenuseid kasutab aprilli lõpu seisuga 394 000 klienti, LHV hallatavatel pensionifondidel on 131 000 aktiivset klienti ja LHV Kindlustusega on kaitstud 158 000 klienti. Groupi tütarettevõte LHV Bank omab Ühendkuningriigi pangalitsentsi ning pakub pangateenuseid rahvusvahelistele finantstehnoloogia ettevõtetele ja laenusid väike- ja keskmise suurusega ettevõtetele. </em></p>    <p><em><br /></em> </p>    <p>Priit Rum<br />LHV kommunikatsioonijuht<br />Telefon: 502 0786<br />E-post: <a href="https://www.globenewswire.com/Tracker?data=Je_zD_MfLPboesDtfid2h84mo1PO-YAf9WafuKsiKRpO-vYokSX07GVU8dYp8ZGd0eF6L2k3edK3LJCHKtSlcw==" rel="nofollow" target="_blank">priit.rum@lhv.ee</a> </p>
        message_response = requests.get(message_url)
        soup = BeautifulSoup(message_response.text, "html.parser")
        
        # Create a text file with the extracted information
        file_name = f"{date}-{stock_name}-{news_title}-{disclosure_id}-{language_code}.md"
        file_path = os.path.join("documents", file_name)

        # Check if the file already exists, and skip downloading if it does
        if os.path.exists(file_path):
            continue

        # Write the extracted information to the utf8 compatible text file
        with open(file_path, "w", encoding="utf8") as f:
            f.write(f"**Ettevõte:** {item['company']}\n")
            f.write(f"**Avaldatud:** {date}\n")
            f.write(f"**URL:** {message_url}\n\n")
            f.write(f"## {item['headline']}\n\n")
            # message content is in the table id=previewTable, and in the third tr tag after h3 and h4, and includes paragraphs and tables
            content_p_tags = soup.find("table", id="previewTable").find_all("tr")[2].find_all(["p","table"])
            
            content = ''
            for content_p_tag in content_p_tags:
                # Remove links within the text
                for a_tag in content_p_tag.find_all('a'):
                    a_tag.unwrap()

                # Convert tables using htmltabletomd library
                if content_p_tag.name == 'table':
                    markdown_element = htmltabletomd.convert_table(str(content_p_tag), content_conversion_ind=True)
                else:
                    markdown_element = html2markdown.convert(str(content_p_tag))
                markdown_element = markdown_element.replace('&nbsp;', ' ')
                content += f"{markdown_element}\n\n"
            f.write(content)

            # Download and save attachments
            if item["attachment"]:
                for attachment in item["attachment"]:
                    attachment_name = attachment["fileName"]
                    attachment_url = attachment["attachmentUrl"]
                    attachment_ext = os.path.splitext(attachment_name)[1]

                    # Save the attachment with the naming convention
                    attachment_file_name = f"{date}-{stock_name}-{news_title}-{attachment_name}-{disclosure_id}-{language_code}{attachment_ext}"
                    attachment_file_path = os.path.join("documents", attachment_file_name)

                    response = requests.get(attachment_url)
                    with open(attachment_file_path, "wb") as af:
                        af.write(response.content)

# Example usage
from_date = datetime.strptime("2023-04-01", "%Y-%m-%d")
to_date = datetime.strptime("2023-05-30", "%Y-%m-%d")
fetch_nasdaqbaltic_news("LHV+Group", from_date, to_date)
