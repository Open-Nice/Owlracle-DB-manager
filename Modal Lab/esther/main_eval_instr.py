from multiprocessing.pool import ThreadPool
import json
from eval_data_crawler import crawl_eval_instr
from crn_to_name_map.semester_crn import semester_crn

def scrape_instr_eval():
    res = []
    for term in semester_crn.keys():
        iterator = iter(semester_crn[term])
        idx = next(iterator)[1]
        print(idx,term)
        src = []
        for i in range(1, 3000):
            src.append((idx, i))

        def get_data(p_instr_w_term, iter=0):
            try:
                res.append(crawl_eval_instr(p_instr_w_term))
            except:
                if iter == 3:
                    print("Error: ", p_instr_w_term)
                else:
                    get_data(p_instr_w_term, iter+1)

        with ThreadPool(100) as pool:
            pool.map(get_data, src)

    print(len(res))
    return res
