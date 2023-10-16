from multiprocessing.pool import ThreadPool
import json
from eval_data_crawler import crawl_comment_instr
from crn_to_name_map.semester_crn import semester_crn

def scrape_instr_comment():
    res = []
    for term in semester_crn.keys():
        idx = next(iter(semester_crn[term]))[1]
        print(term,idx)

        src = []
        for i in range(1, 3000):
            src.append((idx, i))

        def get_data(p_instr_w_term, iter=0):
            try:
                res.append(crawl_comment_instr(p_instr_w_term))
            except:
                if iter == 5:
                    return
                else:
                    get_data(p_instr_w_term, iter+1)

        with ThreadPool(100) as pool:
            pool.map(get_data, src)

    print(len(res))
    return res
