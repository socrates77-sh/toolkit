# history:
# 2018/09/14  v1.5  initial


import csv
import datetime
import io
import json
import msvcrt
import os
import re
import shutil
import sys

import filetype
import requests

VERSION = '1.0'
URL_TDIS_TOP = 'http://online.hhgrace.com/web/get_treeList_ztree.tdis'
URL = 'http://online.hhgrace.com/web/get_docList_search.tdis?treeNodeId=%s&userId=2c9e498b48a7386f0148ac31c83f0108&description=0.11um/F011Q7E8/Design%20Rule/Platform/'
HEADERS = {
    # 'Cookie': 'JSESSIONID=DjXWtvBZ2bZKxsd-72sEwiWrd1IZvCn9SYO0uh3SPt82hEn2JM3W!1722218088'
    #'Cookie': 'JSESSIONID=zbMpgm6xIXdPWpx-9ld1OX3_omWeFsZ2xY48527ZMcd-DtOIuPSl!1722218088'
    'Cookie': 'JSESSIONID=qRmBkCBljEX4i8eZeGMf5iPb4OQAWu_hpeHlffihNcIUXQ6FQH9m!1722218088'
}
# HEADERS = {
#     'Cookie': 'JSESSIONID=s67aooqxWDzg6H7zkXGgs-ogShQn9xcp0sbf6IhzKZBOHHyBh9qH!1722218088',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
# }
CSV_TITLE = ['Document Name', 'Version', 'Size',
             'Update Date', 'Level', 'Subject', 'Document Path']


def ERR(abbrv):
    return '[Error] ' + {
        'http_err': 'cannot access http',
        'doc_count_mismatch': 'document count mismatch between json field and real rows',
        'leaf_err': 'cannot find leaf'
    }.get(abbrv, 'unknown error')


def print_err(abbrv, param):
    if param == '':
        print(ERR(abbrv))
    else:
        print('%s (%s)' % (ERR(abbrv), param))


def print_version(version):
    print('=' * 70)
    print('%s version: %s' % (os.path.basename(__file__), VERSION))
    print('=' * 70)


def usage():
    print('usage:')
    print('    %s path' % os.path.basename(__file__))


class SinglePageDocs():

    def __init__(self, url, headers):
        self.__json_res = self.__get_docs(url, headers)
        self.__url = url
        self.__docs_info = self.__get_docs_info()

    def __get_docs(self, url, headers):
        try:
            res = requests.post(url, headers=headers)
            return res.json()
        except:
            print_err('http_err', url)
            sys.exit(1)

    def __csv_file_name(self):
        prefix = 'list_'
        ext = '.csv'
        date = datetime.datetime.now().date().strftime('%y%m%d')
        return prefix + date + ext

    def __get_docs_info(self):
        total = int(self.__json_res['total'])
        rows = self.__json_res['rows']
        if(total != len(rows)):
            print_err('doc_count_mismatch', self.__url)
            sys.exit(1)

        docs_info = []
        for row in rows:
            name = row['name']
            version = row['version']
            size = row['fileSize']
            update_date = row['endTime']
            level = row['ipLevel']
            subject = row['subject']
            path = row['description']
            fileid = row['fileId']
            docs_info.append((name, version, size, update_date,
                              level, subject, path, fileid))

        return docs_info

    def list_to_csv(self):
        f = open(self.__csv_file_name(), "w+", newline='')
        w = csv.writer(f)
        w.writerows([CSV_TITLE])
        for doc in self.__docs_info:
            w.writerows([doc[:7]])

        f.close()
        print('[FF] %s' % self.__csv_file_name())

    def __save_a_file(self, doc_info):
        fileid = doc_info[7]
        filename = doc_info[0].split('/')[-1]
        # print(filename)
        url = 'http://online.hhgrace.com/web/downFile.tdis?id=275672&confidentialLevel=D&userId=2c9e498b48a7386f0148ac31c83f0108&fileId=%s&name=%s' % (
            fileid, filename)
        res = requests.get(url, headers=HEADERS, timeout=60)
        size_of_file = open(filename, 'wb').write(res.content)
        # kind = filetype.guess(filename)
        ext = filename.split('.')[-1].lower()

        if ext in ('doc', 'docx'):
            new_filename = filename.split('.')[0] + '.pdf'
            shutil.move(filename, new_filename)
        else:
            new_filename = filename
        print('[save] %s (%d bytes)' % (new_filename, size_of_file))

    def save_all_files(self):
        for doc in self.__docs_info:
            self.__save_a_file(doc)


class DocsTree():

    def __init__(self, url, headers):
        self.__top = self.__get_top(url, headers)
        self.__url = url

    def __get_top(self, url, headers):
        try:
            res = requests.get(url, headers=headers)
            return res.json()
        except:
            print_err('http_err', url)
            print(url)
            sys.exit(1)

    def __find_child(self, all_children, child_name):
        if len(all_children) == 0:
            return None
        for a_child in all_children:
            if a_child['name'].lower() == child_name.lower():
                return a_child['children']
        return None

    def node(self, path):
        hier = path.split('/')
        all_children = self.__top
        for level in hier:
            parrent = all_children
            all_children = self.__find_child(all_children, level)
            if all_children is None:
                print_err('leaf_err', path)
                sys.exit(1)
        return parrent


class Node():

    def __init__(self, node):
        self.__node = node

    def __is_leaf(self):
        return (len(self.__node) == 1 and self.__node[0]['leaf'] == True)

    def getid(self):
        if self.__is_leaf:
            return self.__node[0]['id']
        else:
            return None


def get_url(id, path):
    s = 'http://online.hhgrace.com/web/get_docList_search.tdis?treeNodeId=%s&userId=2c9e498b48a7386f0148ac31c83f0108&description=%s/' % (
        id, path)
    # return s.replace(' ', '%20')
    return s


def main():
    # sys.stdout = io.TextIOWrapper(
    #     sys.stdout.buffer, encoding='gb18030', line_buffering=True)
    print_version(VERSION)
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    # path = '0.11um/FS11Q7E8/Design Rule/Platform'
    path = sys.argv[1]
    docs = DocsTree(URL_TDIS_TOP, HEADERS)
    node = docs.node(path)
    id = Node(node).getid()
    url = get_url(id, path)

    a_page_docs = SinglePageDocs(url, HEADERS)
    a_page_docs.list_to_csv()
    a_page_docs.save_all_files()
    print('\nPress any key to exit ...')
    msvcrt.getch()

    # # url = 'http://online.hhgrace.com/web/downFile.tdis?id=300103&confidentialLevel=D&userId=2c9e498b48a7386f0148ac31c83f0108&fileId=&name=/PDK/release/runset/FAB3/Mentor/0.11um/F011Q7E6/LVS/HG_F011Q7E6_LVS_Cal.cmd'
    # url = 'http://online.hhgrace.com/web/downFile.tdis?id=275672&confidentialLevel=D&userId=2c9e498b48a7386f0148ac31c83f0108&fileId=23178&name=DM-COMM-TLR-1610-0010.docx'
    # res = requests.get(url, headers=HEADERS, timeout=60)
    # file_name = 'a'
    # size_of_file = open(file_name, 'wb').write(res.content)
    # print('[save] %s (%d bytes)' % (file_name, size_of_file))
    # kind = filetype.guess(file_name)
    # print(kind)


if __name__ == '__main__':
    main()
