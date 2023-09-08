from main import scrape_courses

import json
import re
import uuid
import modal

stub = modal.Stub(name="link-scraper")
image = modal.Image.debian_slim().pip_install("langchain", "supabase", "openai", "tiktoken", "python-dotenv")

if stub.is_inside():
    from supabase import create_client, Client
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.text_splitter import MarkdownHeaderTextSplitter
    from langchain.vectorstores import SupabaseVectorStore


if modal.is_local():
    from dotenv import load_dotenv
    load_dotenv()
    stub.data_dict = modal.Dict({
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_SERVICE_KEY": os.getenv("SUPABASE_SERVICE_KEY")
    })

@stub.function()
def get_course():
    print("scraping courses...")
    course = scrape_courses()

    return course
    # f = open('course_complete_mine.json', 'w')
    # json.dump(courses, f, indent=4)
    # f.close()

# def get_instr_eval():
#     print("scraping instructor evaluations...")
#     instr_eval = main_eval_instr.eval_instr_run()
#     f = open('all_evals_instr.json', 'w')
#     json.dump(instr_eval, f, indent=4)
#     f.close()

@stub.function()
def write_to_md(courses, path):
    with open(path, "w", encoding="utf-8") as f:
        for term in courses:
            for course in courses[term]:
                print(courses[term][course]['name'])
                f.write(f"# {courses[term][course]['name'].strip()}\n")
                f.write(f"course name: {courses[term][course]['name'].strip()}\n")
                f.write(f"subject: {courses[term][course]['cField']}\n")
                f.write(f"course number: {courses[term][course]['cNum']}\n")
                f.write(f"instructor: {courses[term][course]['instructor']}\n")
                f.write(f"term: {term}\n")
                f.write(f"Organization - Class Mean: {courses[term][course]['Organization']['Class Mean']} Rice Mean: {courses[term][course]['Organization']['Rice Mean']} Responses: {courses[term][course]['Organization']['Responses']} Distribution: {courses[term][course]['Organization']['Distribution']}\n")
                f.write(f"Assignment - Class Mean: {courses[term][course]['Assignment']['Class Mean']} Rice Mean: {courses[term][course]['Assignment']['Rice Mean']} Responses: {courses[term][course]['Assignment']['Responses']} Distribution: {courses[term][course]['Assignment']['Distribution']}\n")
                f.write(f"Overall Quality - Class Mean: {courses[term][course]['Overall Quality']['Class Mean']} Rice Mean: {courses[term][course]['Overall Quality']['Rice Mean']} Responses: {courses[term][course]['Overall Quality']['Responses']} Distribution: {courses[term][course]['Overall Quality']['Distribution']}\n")
                f.write(f"Challenge - Class Mean: {courses[term][course]['Challenge']['Class Mean']} Rice Mean: {courses[term][course]['Challenge']['Rice Mean']} Responses: {courses[term][course]['Challenge']['Responses']} Distribution: {courses[term][course]['Challenge']['Distribution']}\n")
                f.write(f"Workload - Class Mean: {courses[term][course]['Workload']['Class Mean']} Rice Mean: {courses[term][course]['Workload']['Rice Mean']} Responses: {courses[term][course]['Workload']['Responses']} Distribution: {courses[term][course]['Workload']['Distribution']}\n")
                f.write(f"Why take this course - Class Mean: {courses[term][course]['Why take this course']['Class Mean']} Rice Mean: {courses[term][course]['Why take this course']['Rice Mean']} Responses: {courses[term][course]['Why take this course']['Responses']} Distribution: {courses[term][course]['Why take this course']['Distribution']}\n")
                f.write(f"Expected Grade - Class Mean: {courses[term][course]['Expected Grade']['Class Mean']} Rice Mean: {courses[term][course]['Expected Grade']['Rice Mean']} Responses: {courses[term][course]['Expected Grade']['Responses']} Distribution: {courses[term][course]['Expected Grade']['Distribution']}\n")
                f.write(f"Expected P/F - Class Mean: {courses[term][course]['Expected P/F']['Class Mean']} Rice Mean: {courses[term][course]['Expected P/F']['Rice Mean']} Responses: {courses[term][course]['Expected P/F']['Responses']} Distribution: {courses[term][course]['Expected P/F']['Distribution']}\n")
                f.write(f"comments: {courses[term][course]['comments']['comments']}\n")

                f.write("\n")

@stub.function()
def add_uuid_to_headers(markdown_file):
    with open(markdown_file, 'r') as file:
        content = file.readlines()

    updated_content = []
    for line in content:
        if re.match(r'^#[^#]', line):
            unique_id = str(uuid.uuid4())
            line = line.rstrip() + f" [{unique_id}]\n"
        updated_content.append(line)

    with open(markdown_file, 'w') as file:
        file.writelines(updated_content)

@stub.function(image=image)
def get_pages(path):
    pages = []
    with open(path, 'r') as f:
        contents = f.read()

        headers_to_split_on = [
            ("#", "course name"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(contents)

        print(len(md_header_splits))

        pages.extend(md_header_splits)
    return pages

@stub.function(schedule=modal.Period(days=30), image=image)
def timed_scrape():
    courses = get_course()
    fp = "courses.md"
    write_to_md(courses, fp)
    add_uuid_to_headers(fp)
    pages = get_pages(fp)
    print("Pages:", len(pages))
    client: Client = create_client(stub.app.data_dict["SUPABASE_URL"], stub.app.data_dict["SUPABASE_SERVICE_KEY"])
    embeddings = OpenAIEmbeddings(openai_api_key=stub.app.data_dict["OPENAI_API_KEY"])
    vector_store = SupabaseVectorStore(client=client,
                                       embedding=embeddings,
                                       table_name='courses')
    client.table('courses').delete().neq("content", "0").execute()
    vector_store.add_documents(pages)
    print("Courses updated successfully!")

