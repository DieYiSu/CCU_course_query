# remind
# pip install requests
# pip install beautifulsoup4
# pip install lxml
# set the windows system global variable : PYTHONIOENCODING=UTF8

# import
import requests
import json
from bs4 import BeautifulSoup

# const variable
CONST_ccu_course_list_url = 'https://kiki.ccu.edu.tw/~ccmisp06/Course/'
CONST_college_array = []
CONST_college_dict = {}
CONST_encoding = 'UTF-8'
CONST_all_course_dict = []

# function
def crawler(url):
    r = requests.get(url)
    r.encoding = CONST_encoding
    return BeautifulSoup(r.text, 'lxml')


def get_college():
    BS = crawler(CONST_ccu_course_list_url)
    college_list = BS.select('table')[1].select('tr')[0].select('font')

    for college in college_list:
        CONST_college_array.append(college.text)
        CONST_college_dict[college.text] = {}
    write_json_data("source/data.json", CONST_college_array)
    # read_json_data("source/data.json")


def get_department_information():
    counter = 0

    BS = crawler(CONST_ccu_course_list_url)
    college = BS.select('table')[1].select('tr')[1].select('td')

    for college_indivisual in college:
        college_name = CONST_college_array[counter]

        for department in college_indivisual.select('a'):
            #     # 跨領域學程's herf will have the '..' string, strip it
            if department.get('href').strip('..').endswith('html'):
                department_herf = f"/{department.get('href')}"
                CONST_college_dict[college_name][
                    department.text] = f"https://kiki.ccu.edu.tw/~ccmisp06/Course{department_herf}"
            else:
                department_herf = department.get('href').strip('..')
                CONST_college_dict[college_name][
                    department.text] = f"https://kiki.ccu.edu.tw/~ccmisp06/{department_herf}"
        counter += 1
    write_json_data("source/college_dict.json", CONST_college_dict)


def get_course_detail():

    for college_index, college in enumerate(CONST_college_array):
        for department in CONST_college_dict[college]:

            department_URL = CONST_college_dict[college][department]
            BS = crawler(department_URL)

            course_dict = {}
            course_dict_array = []

            for tr_index, tr_html in enumerate(BS.select('tr')): 

                if(tr_index == 0):
                    for th_index, th_html in enumerate(tr_html.select('th')):
                        course_dict[th_html.text] = 0
                        course_dict_array.append(th_html.text)
                else:
                    for td_index, td_html in enumerate(tr_html.select('td')):
                        if(td_html.select('a')):
                            if(td_html.select('a')[0].text == 'link'):
                                course_dict[course_dict_array[td_index]] = td_html.select('a')[0].get('href')
                        else:
                            course_dict[course_dict_array[td_index]] = td_html.text
                    
                    course_dict['College'] = college
                    course_dict['Department'] = department
                    course_dict['URL'] = department_URL

                    CONST_all_course_dict.append(course_dict)
                    course_dict = {}
    write_json_data('source/all_course_dict.json', CONST_all_course_dict)


def write_json_data(file, data):
    with open(file, 'w', encoding=CONST_encoding) as f:
        json.dump(data, f)


def read_json_data(file):
    with open(file, 'r', encoding=CONST_encoding) as f:
        data = json.load(f)
    print(data)

# main
get_college()
print('get_college() completed')

get_department_information()
print('get_department_information() completed')

get_course_detail()
print('get_course_detail() completed')