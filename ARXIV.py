import urllib.request
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import csv
import codecs
import pymysql
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

headers = {'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Cache-Control': 'no-cache',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
           'Connection': 'keep-alive'
        }


def downloadPDF(url):
    # print("downloading" + fileName)
    # with open(fileName, "wb") as file:
    #     response = requests.get(url, headers)
    #     s = requests.session()
    #     s.keep_alive = False
    #     file.write(response.content)
    book_name ='C://Users//215//file//' + url.split('/')[-1]
    print('Downloading book: %s' % book_name)  # 开始下载
    # url = url.replace('?'+ url.split('?')[-1] , "")
    urllib.request.urlretrieve(url, book_name)
    print('Finish downloading book: %s' % book_name)  # 完成下载

def get_conn():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='paper', charset='utf8')
    return conn


def insert(cur, sql, args):
    cur.execute(sql, args)


def read_csv_to_mysql(filename):
    with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        head = next(reader)
        conn = get_conn()
        cur = conn.cursor()
        sql = 'insert into paper values(%s,%s,%s,%s,%s,%s,%s)'
        for item in reader:
            args = tuple(item)
            print(args)
            insert(cur, sql=sql, args=args)

        conn.commit()
        cur.close()
        conn.close()


if __name__ == "__main__":
    item = input('请输入要查找的论文主题（英文）：')
    max_result = input('请输入要查找的最多论文数目（不超过30000条）：')
    url = 'http://export.arxiv.org/api/query?search_query=all:' + item + '&start=0&max_results=' + max_result
    req = urllib.request.Request(url=url, headers=headers)
    data = urllib.request.urlopen(req).read()
    i = 0

    with open('../paper.xml', 'wb') as f:
        f.write(data)

    # with open('../paper.csv','w',newline='') as f:
    #     csv_write = csv.writer(f)
    #     csv_write.writerow(['title', 'published','author','id','summary'])

    xmlfilepath = os.path.abspath("../paper.xml")
    DOMTree = xml.dom.minidom.parse(xmlfilepath)
    collection = DOMTree.documentElement
    papers = collection.getElementsByTagName("entry")

    for paper in papers:
        title = paper.getElementsByTagName('title')[0]
        published = paper.getElementsByTagName('published')[0]
        author = paper.getElementsByTagName('author')[0]
        name = author.getElementsByTagName('name')[0]
        id = paper.getElementsByTagName('id')[0]
        summary = paper.getElementsByTagName('summary')[0]
        with open('../paper.csv','a',encoding='utf-8',newline='') as f:
            csv_write = csv.writer(f)
            data_row = [i,title.childNodes[0].data, published.childNodes[0].data, name.childNodes[0].data, id.childNodes[0].data, summary.childNodes[0].data,id.childNodes[0].data.split('/')[-1]]
            csv_write.writerow(data_row)
        i = i+1

    read_csv_to_mysql('../paper.csv')

    # with open('../paper.csv', 'r') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         downint = row['id'].replace('abs', 'pdf') + '.pdf'
    #         PDFtitle = row['title'].replace("\n","") + '.pdf'
    #         with open('../' + 'book.txt', 'a') as f:
    #             f.write(downint + '\n')
    #
    # start_time = time.time()
    #
    # file_path = '../book.txt'
    # with open(file_path, 'r') as f:
    #     urls = f.readlines()
    # urls = [_.strip() for _ in urls]
    #
    # executor = ThreadPoolExecutor(len(urls))
    # future_tasks = [executor.submit(downloadPDF, url) for url in urls]
    # wait(future_tasks, return_when=ALL_COMPLETED)
    #
    # end_time = time.time()
    # print('Total cost time:%s' % (end_time - start_time))
