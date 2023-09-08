
from bs4 import BeautifulSoup

import requests

cookies = {
    'TESTID': 'set',
    'SESSID': 'UThTVlE1NTQ3NTEy',
    '_gcl_au': '1.1.1767509021.1651183245',
    '_fbp': 'fb.1.1651183245160.1783288854',
    '_rdt_uuid': '1651183245241.ace3f805-ad2b-4858-9ad7-68845547f753',
    'LPVID': 'QwMDA0ODIyNzVmZmY3MzA5',
    '_hjSessionUser_2310211': 'eyJpZCI6IjUwODQyOGQ4LTVhM2EtNThiYy04NmFkLThiMzJmMWM4OTlhMiIsImNyZWF0ZWQiOjE2NTEyMDI4MTA1MzAsImV4aXN0aW5nIjp0cnVlfQ==',
    '_gac_UA-2249859-26': '1.1651888115.CjwKCAjwjtOTBhAvEiwASG4bCICs3_rCxChBTR6ek4gUI_Kau3bIfkGrJK5TH7Y8gkOa089odkGCARoCy9oQAvD_BwE',
    '_gac_UA-2249859-47': '1.1651888115.CjwKCAjwjtOTBhAvEiwASG4bCICs3_rCxChBTR6ek4gUI_Kau3bIfkGrJK5TH7Y8gkOa089odkGCARoCy9oQAvD_BwE',
    '_gac_UA-2249859-27': '1.1651888115.CjwKCAjwjtOTBhAvEiwASG4bCICs3_rCxChBTR6ek4gUI_Kau3bIfkGrJK5TH7Y8gkOa089odkGCARoCy9oQAvD_BwE',
    '_ce.s': 'v~726b2530e53605905672812b5e86607bcd1fb739~vpv~2~v11.rlc~1655346245977',
    '_gcl_dc': 'GCL.1655346359.Cj0KCQjwhqaVBhCxARIsAHK1tiOGjsiOrN2qS5ZVTnPXI6L41BJpg3_kv9NrBsIhhXj4JtZDEgijtjEaAqstEALw_wcB',
    '_gcl_aw': 'GCL.1655346359.Cj0KCQjwhqaVBhCxARIsAHK1tiOGjsiOrN2qS5ZVTnPXI6L41BJpg3_kv9NrBsIhhXj4JtZDEgijtjEaAqstEALw_wcB',
    '_gac_UA-66594374-45': '1.1655346359.Cj0KCQjwhqaVBhCxARIsAHK1tiOGjsiOrN2qS5ZVTnPXI6L41BJpg3_kv9NrBsIhhXj4JtZDEgijtjEaAqstEALw_wcB',
    '_gac_UA-66594374-40': '1.1655346359.Cj0KCQjwhqaVBhCxARIsAHK1tiOGjsiOrN2qS5ZVTnPXI6L41BJpg3_kv9NrBsIhhXj4JtZDEgijtjEaAqstEALw_wcB',
    '_uetvid': 'a7623dd0c73e11ec8e76b75560f6f838',
    '_ga_06DPPK50R3': 'GS1.1.1651683233.9.0.1651683246.0',
    '_ga_8MQ8ENB89P': 'GS1.1.1651683233.9.0.1651683246.0',
    '_ga': 'GA1.2.763195444.1650819931',
    'citrix_ns_id': '0baZmteLbXRF20hKAUMd5jOjayU0002',
    '_gid': 'GA1.2.168471155.1659056157',
    '_gat': '1'
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Chromium";v="103", "Google Chrome";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Origin': 'https://esther.rice.edu',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://esther.rice.edu/selfserve/swkscmt.main',
    'Accept-Language': 'en-US,en;q=0.9,zh-US;q=0.8,zh;q=0.7,zh-CN;q=0.6',
}


def fetch(crn_with_term):
    crn = crn_with_term[0]
    term = crn_with_term[1]
    response = requests.post('https://esther.rice.edu/selfserve/swkscmt.main', headers=headers, cookies=cookies, data={
        'p_commentid': '',
        'p_confirm': '1',
        'p_term': term,
        'p_crn': crn,
        'p_type': 'Course',
        'as_ffc_field': 'AAAAAAV8BiKMhA5a3nxLQJpJIiX8XLWM1Fv_liBmQtMTY4WrsaSRq0RVCeBAIwtf0p8Ld50NIvzwxdgwWaPN6-6HsBJm5Nm8sNWTrTbyqC8ttRje6M0WfECT2kLwiSJ9_nlE1xq0kgPX_GO4GrDkzlr70NPO9McfAMZh5NGT3tJ87iUxKKK-olkyEPjAgUxAg5iU0CFKFmZCVnCKKOawcS4-h-KpDz05X3hH4-G1zxwf-Pp33ayqBs-OED--Asewdb3DCf2nvX9p2CU9BWUVHYD7FqTZmwHkFXCLXrpBjKesxf9Ec4HnmaWogLz8-gzY3zOVCmtehc8GM9dvSNTaO-9IQDpFskb-AeOFHUfGPGlutGz2nRzY8G2EjINF5fDj0r9m1En4iIGQeBHnWmfiIIfvib7OrGqiS6r6Zab4-dpw_FJbVJEuQ1Pd7Al0dSdfPHka1VzLRto-3yw8R1h14J2zA9PMKaeBlDNTYqzTjlE4_3WCXhF1nhHJAKD_MwaKHk2O9mgzOFTxdsWNvlCON0FKi-AbrTKvgKtPrunfOCdtlDAqvqrUzyKzpsNQF-YTyFWF4-Y=',
        'as_fid': 'bb3f81abdbe56b36e25f4b369215759978ef9f91',
    })
    # print(BeautifulSoup(response.content, 'html.parser'))
    return {"crn": crn, "html": response}


def parse_instr(html):
    html_parsed = BeautifulSoup(html.content, 'html.parser')
    info = [i.text for i in html_parsed.find_all(
        "td", {"class": "headerrowtext"})]
    # print({"name": info[3], "instructor": info[-1]})
    return {"name": info[3], "cField": info[3].split()[0], "cNum": info[3].split()[1], "instructor": info[-1]}


def parse(html):
    html_parsed = BeautifulSoup(html.content, 'html.parser')
    charts = html_parsed.find_all("div", {"class": "filler"})
    evaluations = parse_instr(html)
    distr = ocr_graphs(parse_graphs(html))
    eval_title = ["Organization", "Assignment", "Overall Quality", "Challenge", "Workload", "Why take this course",
                  "Expected Grade", "Expected P/F"]
    for i in range(len(eval_title)):
        nums = charts[i].find_all("div", {"class": "third"})
        evaluations[eval_title[i]] = {}
        evaluations[eval_title[i]]['Class Mean'] = float(nums[0].text[12:])
        evaluations[eval_title[i]]['Rice Mean'] = float(nums[1].text[11:])
        try:
            evaluations[eval_title[i]]['Responses'] = int(nums[3].text[10:])
        except ValueError:
            evaluations[eval_title[i]]['Responses'] = 0
        evaluations[eval_title[i]]['Distribution'] = distr[eval_title[i]]
    evaluations['comments'] = parse_comments(html)
    return evaluations


def parse_comments(html):
    html_parsed = BeautifulSoup(html.content, 'html.parser')
    comment_divs = html_parsed.find_all("div", {"class": "cmt"})
    comments = []
    for comment_div in comment_divs:
        # comment time
        t = comment_div.find_next('div').find_next_sibling(
            'div').find_next('div').text
        # print(t)
        comments.append(comment_div.find_next("div").find_next(
            "div").text.replace('\n', ' ') + " " + t)
    res = parse_instr(html)
    res['comments'] = comments
    return res


def parse_graphs(html):
    html_parsed = BeautifulSoup(html.content, 'html.parser')
    charts = html_parsed.find_all("div", {"class": "filler"})
    graphs = []
    for chart in charts:
        graph = chart.find_next('img')
        graphs.append(graph)
    # graphs = html_parsed.find_all("img")
    return graphs


def crawl(crn_with_term):
    response = fetch(crn_with_term)
    return parse(response["html"])


def crawl_comment(crn_with_term):
    response = fetch(crn_with_term)
    return parse_comments(response["html"])


def crawl_graphs(crn_withterm):
    response = fetch(crn_withterm)
    return parse_graphs(response['html'])


def parse_graph_url(src):
    idx1 = src.find('&sampleValues=') + 14
    idx2 = src.find('&sampleLabels')
    return src[idx1:idx2]


def ocr_graphs(graphs):
    res = {}
    for i in range(len(graphs)):
        src = 'https://esther.rice.edu' + graphs[i]['src']
        src = src.replace(" ", "")
        nums = [int(x) for x in parse_graph_url(src).split(',')]
        if i == 0:
            res['Organization'] = nums
        elif i == 1:
            res['Assignment'] = nums
        elif i == 2:
            res['Overall Quality'] = nums
        elif i == 3:
            res['Challenge'] = nums
        elif i == 4:
            res['Workload'] = nums
        elif i == 5:
            res['Why take this course'] = nums
        elif i == 6:
            res['Expected Grade'] = nums
        elif i == 7:
            res['Expected P/F'] = nums
        # else: nums.insert(0, 'Error')
        # res.append(nums)
    return res
    # for line in res:
    #     print(line)


# print(crawl_comment(('20984', '202120')))


def fetch_instructor(p_term, p_instr):
    # crn = crn_with_term[0]
    # term = crn_with_term[1]
    response = requests.post('https://esther.rice.edu/selfserve/swkscmt.main', headers=headers, cookies=cookies, data={
        'p_commentid': '',
        # 'p_confirm': '1',
        'p_term': p_term,
        # 'p_crn': crn,
        # 'p_instr_ini': 'U',
        'p_instr': p_instr,
        'p_type': 'Instructor',
        'p_confirm': '1',
        'as_ffc_field': 'AAAAAAU7UtVqgTu2QBdri1Eds4kRr70sBLFpFCi-K8e2Nfn37srKCdM8fRyEKaIfF-Wd8FcSJxHk9YuTvzN51X9z_hP7f6rttViKW8Rkikda6koWr7xpoXXqV2BDZlwSw33C4jql48RABQzgUBsC6SCeFTwaGXMnXfs7Yd5ULTORd_2JGLOOvhGLnWeKy5ms0Acr3V9Jpp8NQUhxQtVKwo5WB4oJvdNPHArv3_95-JZzC2fboTjCtWBTWgM_yh6dhHvVvAqznhBfzhtajuQQF5YNF4StqbRmWTKhwNWXO_nw_mAu8DzeLTSH2hBhcUTuLAzmKsdqh34k65y0Bs-MFOzjcYu9aMlw6jFf5rg-50Vu39ZiWk-FQUQ7Fscwi5y_-p1s_hb8VMjcrx7jNeO7V70N7UnVuMEFg42O--ymVvWZcoaxi8zkaVSoNZzTnuPqTk-UUl5wFxa2QGl3IlGrVU2NVhH2R62xUZJ_WTB1AycYE63FJjP5EukbKaxm1ZV0tq6zWcf5JZHpJlMU4g3T-qv6CXSkCVdOcAPAUKCuXoxnbBWL50f9Q3elZjnLTHuKiS95ZPg=',
        'as_fid': 'bb3f81abdbe56b36e25f4b369215759978ef9f91',
    })
    return response

def parse_info_instr(crn_html):
    info = crn_html.find_all("td", {"class": "headerrowtext"})
    return {'year': info[1].text.split(' ')[2], 'semester': info[1].text.split(' ')[0], 'crn': crn_html['data-crn'], 'name': info[3].text, 'instructor': info[-1].find_all('b')[0].text}


def parse_comments_instr(crn_html):
    comment_divs = crn_html.find_all("div", {"class": "cmt"})
    comments = []
    for comment_div in comment_divs:
        # comment time
        t = comment_div.find_next('div').find_next_sibling(
            'div').find_next('div').text
        comments.append(comment_div.find_next("div").find_next(
            "div").text.replace('\n', ' ') + " " + t)
    return comments


def parse_all_comments_instr(crn_lst):
    cmts = []
    for i in crn_lst:
        cmt = parse_info_instr(i)
        cmt['comments'] = parse_comments_instr(i)
        cmts.append(cmt)
    res = {}
    res['year'] = cmts[0]['year']
    res['semester'] = cmts[0]['semester']
    res['instructor'] = cmts[0]['instructor']
    res['course comments'] = cmts
    return res


def ocr_graphs_instr(graphs):
    res = {}
    for i in range(len(graphs)):
        src = 'https://esther.rice.edu' + graphs[i]['src']
        src = src.replace(" ", "")
        nums = [int(x) for x in parse_graph_url(src).split(',')]
        if i == 0:
            res['Organization'] = nums
        elif i == 1:
            res['Presentation'] = nums
        elif i == 2:
            res['Responsiveness'] = nums
        elif i == 3:
            res['Class Atmosphere'] = nums
        elif i == 4:
            res['Independence'] = nums
        elif i == 5:
            res['Stimulation'] = nums
        elif i == 6:
            res['Knowledge'] = nums
        elif i == 7:
            res['Effectiveness'] = nums
        elif i == 8:
            res['Responsibility'] = nums
    return res


def parse_score_instr(crn_html):
    evaluations = parse_info_instr(crn_html)
    charts = crn_html.find_all("div", {"class": "filler"})
    eval_title = ["Organization", "Presentation", "Responsiveness", "Class Atmosphere", "Independence", "Stimulation",
                  "Knowledge", "Effectiveness", "Responsibility"]
    graphs = []
    for chart in charts:
        graph = chart.find_next('img')
        graphs.append(graph)
    distr = ocr_graphs_instr(graphs)
    for i in range(len(eval_title)):
        nums = charts[i].find_all("div", {"class": "third"})
        evaluations[eval_title[i]] = {}
        evaluations[eval_title[i]]['Class Mean'] = float(nums[0].text[12:])
        evaluations[eval_title[i]]['Rice Mean'] = float(nums[1].text[11:])
        try:
            evaluations[eval_title[i]]['Responses'] = int(nums[3].text[10:])
        except ValueError:
            evaluations[eval_title[i]]['Responses'] = 0
        evaluations[eval_title[i]]['Distribution'] = distr[eval_title[i]]
    return evaluations


def parse_all_score_instr(crn_lst):
    scores = []
    for i in crn_lst:
        score = parse_info_instr(i)
        score['distribution'] = parse_score_instr(i)
        scores.append(score)
    res = {}
    res['year'] = scores[0]['year']
    res['semester'] = scores[0]['semester']
    res['instructor'] = scores[0]['instructor']
    res['course evaluations'] = scores
    return res


def get_crn_lst(soup):
    return soup.findAll(lambda tag: tag.name == 'div' and 'data-crn' in tag.attrs)


def crawl_comment_instr(p_instr_w_term):
    response = fetch_instructor(p_instr_w_term[0], p_instr_w_term[1])
    return parse_all_comments_instr(get_crn_lst(BeautifulSoup(response.content, 'html.parser')))


def crawl_eval_instr(p_instr_w_term):
    response = fetch_instructor(p_instr_w_term[0], p_instr_w_term[1])
    return parse_all_score_instr(get_crn_lst(BeautifulSoup(response.content, 'html.parser')))


def crawl_all_eval(p_instr_w_term):
    res = crawl(p_instr_w_term)
    res['instructor_evaluations'] = crawl_eval_instr(p_instr_w_term)['course evaluations']
    return res
