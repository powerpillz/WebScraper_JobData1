from bs4 import BeautifulSoup as bs
import requests
import xlsxwriter
import re
''' Web scraper to get job information from Local Government Assist website
    written by James Beamish                                                '''

#######################################Todo!!!!#############################################
#Still todo! Solve for Job Reference Field that is in some pages but not in others! 28/01/22
#First job scrape is a double up!
#Todo! Scrape job title!



urls = []
data = []

url_list = ["https://www.lgassist.com.au/western-australia-wa",
            "https://www.lgassist.com.au/western-australia-wa/1",
            "https://www.lgassist.com.au/western-australia-wa/2"]

for site in url_list:
    r = requests.get(site)

    soup = bs(r.content, features = "html.parser")
    result = soup.find_all('div', attrs = {"premiumBlock", "s-res s-res-odd s-res-first", "s-res", "s-res s-res-odd"})
    #result = soup.find_all('div', attrs = {"s-res s-res-odd s-res-first"})
    print(len(result))

    for details in result:
        entry = details.find('a', tabindex = '40')
        job_title = entry.text.strip()
        pattern = re.compile(r"(\/+career\/)+(\d{6,}\/)+((\w+)-)*(\w+)")
        str_entry = str(entry)
        #print(job_title)
        result = pattern.search(str_entry)


        #print(result[0])
        url_extension = str(result[0])
        url_complete = str(f'https://www.lgassist.com.au{url_extension}')
        #print(url_complete)
        urls.append(url_complete)
        #print(entry)

#print(urls)
    #name = soup.find_all("a", tabindex = "40")
    #print(name)



for url in urls:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}
    spec = requests.get(url, headers=headers)
    #print(spec)
    soup_spec = bs(spec.content, features = "html.parser")

    tr_list = []

    #Employer Information in TBody Tag
    employer_info = soup_spec.find('tbody')
    #print(employer_info)
    #count = 0
    
    employer_cleaned = ""
    job_type_cleaned = ""
    location_cleaned = ""
    salary_cleared = ""
    post_date_cleaned = ""

    #JOB REFERENCE


    #EMPLOYER NAME
    for tr in employer_info:
        tr = soup_spec.find_all('tr')[1].text
        #print(tr)
        pattern = re.compile(r"(Shire of |City of |Town of ).*(\w)")
        str_tr = str(tr)
        result = pattern.search(tr)
        if result == None:
            break
        employer = str(result[0])
        #print(employer)
        #count = count + 1
        employer_cleaned = employer
        #tr_list.append(employer)

    #JOB TYPE
    for tr in employer_info:
        tr = soup_spec.find_all('tr')[2].text
        #print(tr)
        pattern = re.compile(r"Permanent Full Time|Fixed Term Full Time|Full Time|Casual|Contract|Temporary|Permanent Part Time")
        str_tr = str(tr)
        result = pattern.search(tr)
        if result == None:
            break
        job_type = str(result[0])
        job_type_cleaned = job_type
        

    #LOCATION
    for tr in employer_info:
        tr = soup_spec.find_all('tr')[3].text
        #print(tr)
        pattern = re.compile(r"^(?!.*City:.*).*(\w)", re.MULTILINE)
        #pattern = re.compile(" City:")
        str_tr = (tr)
        result = pattern.search(tr)
        if result == None:
            break
        #print(result)
        location = result[0]
        location_cleaned = location


    #SALARY
    for tr in employer_info:
        tr = soup_spec.find_all('tr')[4].text
        #print(tr)
        pattern = re.compile(r"\$\d{0,3},\d{0,3}.\d{0,2}.*(\w)|\$\d{2}.\d{2}.*(\w)", re.MULTILINE)
        #pattern = re.compile(" City:")
        str_tr = (tr)
        result = pattern.search(tr)
        #print(result)
        
        if result == None:
            salary_cleaned = "Not Specified"
            for tr in employer_info:
                tr = soup_spec.find_all('tr')[4].text
                #print(tr)
                pattern = re.compile(r"\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}")
                str_tr = (tr)
                result = pattern.search(tr)
                if result == None:
                    break
                #print(result)
                post_date = result[0]
                post_date_cleaned = post_date
        else:
            salary = result[0]
            salary_cleaned = salary
            for tr in employer_info:
                tr = soup_spec.find_all('tr')[5].text
                #print(tr)
                pattern = re.compile(r"\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}")
                str_tr = (tr)
                result = pattern.search(tr)
                if result == None:
                    break
                #print(result)
                post_date = result[0]
                post_date_cleaned = post_date

    #POST DATE
    #for tr in employer_info:
        #tr = soup_spec.find_all('tr')[5].text
        #print(tr)
        #pattern = re.compile("\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}")
        #str_tr = (tr)
        #result = pattern.search(tr)
        #print(result)
        #post_date = result[0]
        #post_date_cleaned = post_date


    #print(count)
    #print(tr_list)
    print("\n")
    
    print(employer_cleaned)
    print(job_type_cleaned)
    print(location_cleaned)
    print(salary_cleaned)
    print(post_date_cleaned)
    

    #print(employer_info)
'''
    data.append([{'employer':employer_cleaned, 'job title':job_title, 'job type':job_type_cleaned, 'location':location_cleaned, 'salary':salary_cleaned, 'post date':post_date_cleaned, 'url':url_complete}])    

# Create an excel file
workbook = xlsxwriter.Workbook('lg_assist.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Employer')
worksheet.write('B1', 'Job Title')
worksheet.write('C1', 'Job Type')
worksheet.write('D1', 'Location')
worksheet.write('E1', 'Salary')
worksheet.write('F1', 'Post Date')
worksheet.write('G1', 'Url')

counter = 2
for data in data:
    worksheet.write(f'A{counter}', data[0]['employer'])
    worksheet.write(f'B{counter}', data[0]['job title'])
    worksheet.write(f'C{counter}', data[0]['job type'])
    worksheet.write_url(f'D{counter}', data[0]['location'])
    worksheet.write_url(f'D{counter}', data[0]['salary'])
    worksheet.write(f'E{counter}', data[0]['post date'])
    worksheet.write_url(f'F{counter}', data[0]['url'])
    counter += 1
workbook.close()

'''