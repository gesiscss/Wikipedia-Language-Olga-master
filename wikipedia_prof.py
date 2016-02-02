__author__ = 'babak'
import wikipedia
import MySQLdb
import re
#import pandas as pd
#import xlrd
from wikitools import wiki, api
import csv
import pandas as pd

class professions:
    rows_list=[]
    job_list=[]
    def read_data(self):
        # number of rows = 120212
        # PsID = []

        with open('professions-wikipedia2.csv', 'rb') as f:
            reader = csv.reader(f)
            self.rows_list = list(reader)

        # workbook = xlrd.open_workbook('pantheon.csv')
        #
        # sheet = workbook.sheet_by_index(0)
        # # cell = sheet.cell_value(0,0)
        # # print cell
        # # rows = sheet.nrows
        # self.rows_list = [[sheet.cell_value(row,c) for c in range(sheet.ncols)] for row in range(1,sheet.nrows)]

        print len(self.rows_list)
        print self.rows_list[1][13]
        print ("xls fetched...")
        self.get_image_link()

    def get_image_link(self):
        wiki_image_list=[]
        filename = 'profession_images.txt'
        df = pd.DataFrame(columns=[ 'language_label', 'profession','wikipedia_link', 'image_link'])
        for i in range(1,len(self.rows_list)):

            print "row number =",i
            all_links=[]

            wikipedia.set_lang('en')
            prof = self.rows_list[i][0]
            try:
                page_title = self.rows_list[i][13].split('/')[4]
            except:
                continue
            print page_title

            params = {'action':'query',
                'format':'json',
                'titles':page_title,
                'prop':'langlinks',
                'lllimit':'100',
                'llurl':'',

                'continue':''
            }
            try:


                #---------------------------------- wikitools library ----------------------------------------
                site = wiki.Wiki('http://en.wikipedia.org/w/api.php')
                req = api.APIRequest(site, params)
                res = req.query()
                # pprint.pprint(res)
                #--------------------------------------------------------------------------------------
                #print res
                all_links.append(['en',page_title,prof,self.rows_list[i][13]])
                lang_list = res['query']['pages'].values()[0]['langlinks']
                for lang in lang_list:
                    lang_id = lang['lang']
                    lang_url = lang['url']
                    wiki_name = lang['*']

                    all_links.append([lang_id,wiki_name,prof,lang_url])
                for data in all_links:
                    lang_id = data[0]
                    try :

                        #print data[1]
                        params2 = {'action':'query',
                            'format':'json',
                            'titles':data[1],
                            'generator':'images',
                            'gimlimit':10,
                            'prop':'imageinfo',
                            'iiprop':'url',
                            'continue':''
                        }

                        #---------------------------------- wikitools library ----------------------------------------
                        site2 = wiki.Wiki('http://%s.wikipedia.org/w/api.php' %lang_id)
                        req = api.APIRequest(site2, params2)
                        res = req.query()
                        #--------------------------------------------------------------------------------------
                        for item in  res['query']['pages'].values():
                            #if 'Wiktionary' or 'Ambox' not in item['imageinfo'][0]['url'].split('/')[7]:
                                #print item['imageinfo'][0]['url']
                            wiki_dict={ 'language_label':data[0], 'profession':data[2],'wikipedia_link':data[3], 'image_link':item['imageinfo'][0]['url']}
                            df = df.append(wiki_dict, ignore_index=True)

                    except:
                        wiki_dict={ 'language_label':data[0], 'profession':data[2],'wikipedia_link':data[3], 'image_link':'-'}
                        df = df.append(wiki_dict, ignore_index=True)
                        continue

            except:
                print "error on row : " ,i
                continue
        df.to_csv(filename, sep='\t', encoding='utf-8')

    def search(self):
        counter =0
        for i in range(len(self.rows_list)):
            counter +=1
            print counter
            prof = self.rows_list[i][0][:-1]
            result = wikipedia.search(prof)
            print prof, " : ",result
            for item in result:
                #print prof
                try:
                    if prof in item:
                        print item
                        self.job_list.append(item)
                except:
                    continue
        print len(self.job_list)
if __name__ == '__main__':
    p = professions()

    p.read_data()
    #p.get_data()