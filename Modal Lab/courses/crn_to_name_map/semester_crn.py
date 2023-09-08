import requests
from bs4 import BeautifulSoup

cookies = {
    'TESTID': 'set',
    'SESSID': 'QlYwUk5JNTQ3NTEy',
    '_gcl_au': '1.1.951756867.1645388057',
    '_fbp': 'fb.1.1645388057597.700770990',
    '_hjSessionUser_2310211': 'eyJpZCI6ImU3YWUwOWZkLWYwMjktNTI3ZC04ODBmLTg1NDRmNjkyMzg0NSIsImNyZWF0ZWQiOjE2NDUzODgwNTc0MzAsImV4aXN0aW5nIjp0cnVlfQ==',
    '_rdt_uuid': '1646196522440.0741efa9-462d-4447-8002-758e9206d011',
    'LPVID': 'Y1MzQwOGE1NWY5MWY5ZjVj',
    '_gcl_dc': 'GCL.1646196556.CjwKCAiApfeQBhAUEiwA7K_UH_R2pdM05Ctrz6UTPZiKN9cUQujNCx0HAYZJ1CwBQdkqVSB9L-SJ0BoCd8AQAvD_BwE',
    '_gac_UA-66594374-45': '1.1646196556.CjwKCAiApfeQBhAUEiwA7K_UH_R2pdM05Ctrz6UTPZiKN9cUQujNCx0HAYZJ1CwBQdkqVSB9L-SJ0BoCd8AQAvD_BwE',
    '_gac_UA-66594374-40': '1.1646196556.CjwKCAiApfeQBhAUEiwA7K_UH_R2pdM05Ctrz6UTPZiKN9cUQujNCx0HAYZJ1CwBQdkqVSB9L-SJ0BoCd8AQAvD_BwE',
    '_gid': 'GA1.2.198699051.1647570618',
    'cebs': '1',
    '_gcl_aw': 'GCL.1647790821.CjwKCAjwoduRBhA4EiwACL5RPzglwBhvdhCIwzDHIlm7kLO-WokubhS38rerdE4TRWGCzoY8WM0t-xoCNTcQAvD_BwE',
    '_gac_UA-2249859-53': '1.1647790821.CjwKCAjwoduRBhA4EiwACL5RPzglwBhvdhCIwzDHIlm7kLO-WokubhS38rerdE4TRWGCzoY8WM0t-xoCNTcQAvD_BwE',
    'hubspotutk': 'e551c433a9d1bd5a29170e21844fc682',
    '__hssrc': '1',
    '_gac_UA-45347247-2': '1.1647821867.CjwKCAjwoduRBhA4EiwACL5RP4CXG8Nh0jNIhSInbGQuR_vudKHHnPb7W5MHzD-6FfXJXuwTThX7nhoCgxEQAvD_BwE',
    'smartrfi_external_id': 'undefined',
    '__hstc': '95890179.e551c433a9d1bd5a29170e21844fc682.1647790821083.1647790821083.1648260737912.2',
    '_ga_GXMHQZBLXZ': 'GS1.1.1648567549.1.1.1648567692.0',
    '_ga': 'GA1.2.1526291539.1645132294',
    '_ga_934XKRXT4Y': 'GS1.1.1648998578.3.1.1648999095.0',
    'smartrfi_prospect_id': 'Rice-1',
    '_clck': 'mvrgj1|1|f0d|0',
    '_uetvid': 'ae55ffb0928911eca53ac39afc65783c',
    '_ce.s': 'v11.rlc~1649556207737~v~ec3d28851ac9ca69bb69a8e68042e9ca9baad9ef~vpv~1~ir~1~gtrk.la~l12y2dmn',
    'citrix_ns_id': 'e0AyExb9LC//10BM6UAQ+OyUo9o0003',
    'IDMSESSID': '1107BE322FBBB55FC6068DE3584A49E252990B7346755BF8139249F0FBB54C052B3C9E986F947729C0C532B6CD6B6951',
    '_gat': '1',
}
headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'Accept': 'application/xml, text/xml, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://esther.rice.edu/selfserve/swkscmt.main',
    'Accept-Language': 'en-US,en;q=0.9',
}

semester_crn = {}
semester_crn_name = {}
for term in range(2008, 2024):
    p_term_fall = str(term) + '10'
    params = (
        ('p_data', 'COURSES'),
        ('p_term', p_term_fall),
    )
    response = requests.get('https://esther.rice.edu/selfserve/!swkscmp.ajax', headers=headers, params=params,
                            cookies=cookies)
    html_parsed = BeautifulSoup(response.content, 'html.parser')
    course_list = html_parsed.find_all("course")
    semester_crn[str(term-1) + '_Fall'] = {(course['crn'], p_term_fall) for course in course_list}
    semester_crn_name[str(term - 1) + '_Fall'] = {}
    for course in course_list:
        semester_crn_name[str(term-1) + '_Fall'][course['crn']] = course['subj']+' '+course['numb']
    # semester_crn_name[str(term-1) + '_Fall'] = {[course['subj']+' '+course['numb'], course['crn']] for course in course_list}

    p_term_spring = str(term) + '20'
    params = (
        ('p_data', 'COURSES'),
        ('p_term', p_term_spring),
    )
    response = requests.get('https://esther.rice.edu/selfserve/!swkscmp.ajax', headers=headers, params=params,
                            cookies=cookies)
    html_parsed = BeautifulSoup(response.content, 'html.parser')
    course_list = html_parsed.find_all("course")
    semester_crn[str(term) + '_Spring'] = {(course['crn'], p_term_spring) for course in course_list}
    semester_crn_name[str(term) + '_Spring'] = {}
    for course in course_list:
        semester_crn_name[str(term) + '_Spring'][course['crn']] = course['subj']+' '+course['numb']
    # semester_crn_name[str(term) + '_Spring'] = {[course['subj']+' '+course['numb'], course['crn']] for course in course_list}


    p_term_summer = str(term) + '30'
    params = (
        ('p_data', 'COURSES'),
        ('p_term', p_term_summer),
    )
    response = requests.get('https://esther.rice.edu/selfserve/!swkscmp.ajax', headers=headers, params=params,
                            cookies=cookies)
    html_parsed = BeautifulSoup(response.content, 'html.parser')
    course_list = html_parsed.find_all("course")
    semester_crn[str(term) + '_Summer'] = {(course['crn'], p_term_summer) for course in course_list}
    semester_crn_name[str(term) + '_Summer'] = {}
    for course in course_list:
        semester_crn_name[str(term) + '_Summer'][course['crn']] = course['subj']+' '+course['numb']

for i in range(2008, 2014):
    semester_crn.pop(f'{i}_Summer')
    semester_crn_name.pop(f'{i}_Summer')

