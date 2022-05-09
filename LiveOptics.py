#!/usr/bin/env python

import pandas as pd
import os
import glob



path = os.getcwd()
files = glob.glob(os.path.join(path, "*.xlsx"))
Read_Col_List =["Category","Size of Files Bytes","Compressed Files Size Bytes"]



#test if LODOS or WizTree


#read xlsx with matching columns from dir
new_xls = pd.concat([pd.read_excel(f, usecols= (Read_Col_List),sheet_name ='FileCategory') for f in files])

#change column names
new_xls.columns = ["Category", "Size of Files GiB","Compressed Files Size GiB"]

#from byte to Gib, add extra *1024 for TiB
new_xls["Size of Files GiB"] = [x/(1024*1024*1024) for x in new_xls["Size of Files GiB"]]
new_xls["Compressed Files Size GiB"] = [x/(1024*1024*1024) for x in new_xls["Compressed Files Size GiB"]]

#sum of identical values
new_xls["Size of Files GiB"] = new_xls.groupby(["Category"])["Size of Files GiB"].transform('sum')
new_xls["Compressed Files Size GiB"] = new_xls.groupby(["Category"])["Compressed Files Size GiB"].transform('sum')


#drop duplicates
new_xls.drop_duplicates(subset = "Category", keep = 'first', inplace = True)

#sort descending
new_xls = new_xls.sort_values(by='Size of Files GiB', ascending = False)

#show  files above 20GB and write to new xlsx
new_xls[new_xls["Size of Files GiB"] > 20].to_excel( "new_xls.xlsx", index=False, encoding='utf-8-sig', sheet_name = 'category')


