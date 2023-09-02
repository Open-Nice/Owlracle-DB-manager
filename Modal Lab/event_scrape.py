from datetime import date
import json
import re
import uuid
import urllib.request
import os

import modal

CLEANER = re.compile("<.*?>")

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



@stub.function(image=image)
def get_events(curDate):
    url = f"https://owlnest.rice.edu/api/discovery/event/search?endsAfter={curDate}&orderByField=endsOn&orderByDirection=ascending&status=Approved&take=10000&query="
    response = urllib.request.urlopen(url)
    evts = json.loads(response.read().decode('utf8'))["value"]
    return evts

@stub.function()
def write_to_md(evts, path):
    with open(path, "w", encoding="utf-8") as f:
        for evt in evts:
            id = evt["id"]
            website = "https://owlnest.rice.edu/event/" + id
            f.write(f"# {evt['name'].strip()}\n")
            f.write(f"Event name: {evt['name'].strip()}\n")
            descrip = re.sub(CLEANER, '', evt['description']).replace('\r', '').replace('\n', ' ').replace('&nbsp;',
                                                                                                           '').strip()
            f.write(f"Description: {descrip}\n")
            f.write(f"Location: {evt['location']}\n")
            f.write(f"Start time: {evt['startsOn']}\n")
            f.write(f"End time: {evt['endsOn']}\n")
            f.write(f"Website: {website}\n")
            f.write(f"Theme: {evt['theme']}\n")
            if len(evt['categoryNames']) != 0:
                f.write(f"Event category: {', '.join(evt['categoryNames'])}\n")
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
            ("#", "Event Name"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(contents)

        print(len(md_header_splits))

        pages.extend(md_header_splits)
    return pages

@stub.function(schedule=modal.Period(days=1), image=image)
def timed_scrape():
    curDate = date.today()
    recent_evts = get_events(curDate)
    fp = "latest_events.md"
    write_to_md(recent_evts, fp)
    add_uuid_to_headers(fp)
    pages = get_pages(fp)
    print("Pages:", len(pages))
    client: Client = create_client(stub.app.data_dict["SUPABASE_URL"], stub.app.data_dict["SUPABASE_SERVICE_KEY"])
    embeddings = OpenAIEmbeddings(openai_api_key=stub.app.data_dict["OPENAI_API_KEY"])
    vector_store = SupabaseVectorStore(client=client,
                                       embedding=embeddings,
                                       table_name='events')
    client.table('events').delete().neq("content", "0").execute()
    vector_store.add_documents(pages)
    print("Events updated successfully!")
