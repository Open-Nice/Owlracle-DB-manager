from main_comment_instr import scrape_instr_comment

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
def get_instr_comment():
    print("scraping instructor comments...")
    instr_comment = scrape_instr_comment()
    f = open('all_comments_instr.json', 'w')
    json.dump(instr_comment, f, indent=4)
    f.close()
    return instr_comment

@stub.function()
def write_to_md(instr_comment, path):
    with open(path, "w", encoding="utf-8") as f:
        for idx in range(len(instr_comment)):
            f.write(f"# {instr_comment[idx]['instructor'].strip()}\n")
            for course in instr_comment[idx]['course comments']:
                f.write(f"course name: {course['name']}\n")
                f.write(f"crn: {course['crn']}\n")
                f.write(f"term: {course['year']}_{course['semester']}\n")
                f.write(f"comments: {course['comments']}\n")
                f.write("\n")
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

    instr_comment = get_instr_comment()
    fp = "instr_comment.md"
    write_to_md(instr_comment,fp)
    add_uuid_to_headers(fp)
    pages = get_pages(fp)
    print("Pages:", len(pages))
    client: Client = create_client(stub.app.data_dict["SUPABASE_URL"], stub.app.data_dict["SUPABASE_SERVICE_KEY"])
    embeddings = OpenAIEmbeddings(openai_api_key=stub.app.data_dict["OPENAI_API_KEY"])
    vector_store = SupabaseVectorStore(client=client,
                                       embedding=embeddings,
                                       table_name='instructor_comment')
    client.table('instructor_comment').delete().neq("content", "0").execute()
    vector_store.add_documents(pages)
    print("Instructor comments updated successfully!")
