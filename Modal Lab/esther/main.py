from multiprocessing.pool import ThreadPool

from eval_data_crawler import crawl
from crn_to_name_map.semester_crn import semester_crn
import json

def scrape_courses():
    error_set = set()
    res = {}
    for term in semester_crn.keys():
        print(term)
        res[term] = {}


        def get_data(crn_w_term, iter=0):
            try:
                res[term][crn_w_term[0]] = crawl(crn_w_term)
            except:
                if iter == 10:
                    print(crn_w_term)
                    error_set.add(term)
                else:
                    get_data(crn_w_term, iter + 1)


        with ThreadPool(100) as pool:
            pool.map(get_data, semester_crn[term])

    print(res.keys())
    # print(res)
    print(error_set)

    return res
    # f = open('course_complete_mine.json', 'w')
    # json.dump(res, f, indent=4)
