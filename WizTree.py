#!/usr/bin/env python

import pandas as pd
import os
import glob

#variables
path = os.getcwd()
files=glob.glob(os.path.join(path, "*.csv"))
WT_Read_Col_List =["Extension","Allocated"]
base_total=0
end_total=0
base_all_removed=0
DRR_none=0
#DRR_1=0
#DRR_2=0
#DRR_3=0
DRR_4=0 

#15 categories
    #no drr
DRR_video=[".f4v",".3g2",".3gp",".avi",".flv",".h264",".h265",".m4v",".mkv",".mov",".mp4",".mpg",".mpeg",".rm",".swf",".vob",".wmv"]
DRR_audio=[".aif",".cda",".mid",".midi",".mp3",".mpa",".ogg",".wav",".wma",".wpl",".flac"]
DRR_compressed=[".7z",".arj",".deb",".pkg",".rar",".rpm",".tar.gz",".z",".zip"]
DRR_pdf=[".pdf"]

    #valid drr
DRR_disc_image=[".bin",".dmg",".iso",".toast",".vcd"]
DRR_datafile=[".csv",".dat",".db",".dbf",".log",".mdb",".sav",".sql",".tar",".xml"]
DRR_email=[".email",".eml",".emlx",".msg",".oft",".ost",".pst",".vcf"]
DRR_exe=[".apk",".bat",".bin",".cgi",".pl",".com",".exe",".gadget",".jar",".msi",".py",".wsf"]
DRR_images=[".ai",".bmp",".gif",".ico",".jpeg",".jpg",".png",".ps",".psd",".svg",".tif",".tiff"]
DRR_internet=[".asp",".aspx",".cer",".cgi",".pl",".htm",".html",".js",".jsp",".part",".php",".py",".rss",".xhtml"]
DRR_presentation=[".key",".odp",".pps",".ppt",".pptx"]
DRR_programming=[".c",".cgi",".pl",".class",".cpp",".cs",".h",".java",".php",".py",".sh",".swift",".vb"]
DRR_spreadsheet=[".ods",".xls",".xlsm",".xlsx"]
DRR_system=[".bak",".cab",".cfg",".cpl",".cur",".dll",".dmp",".drv",".icns",".ini",".lnk",".msi",".sys",".tmp"]
DRR_word=[".doc",".docx",".odt",".rtf",".tex",".txt",".wpd"]

#read csvs with matching columns in files dir, skip first row
reduce_csv = pd.concat([pd.read_csv(f,usecols=(WT_Read_Col_List),skiprows=(1)) for f in files])
print("Read CSV")
#change column names 
reduce_csv.columns = ["Extension", "Allocated Filesize GB"]

#add identifier for non recognized extension
reduce_csv["Extension"] = reduce_csv["Extension"].fillna(".NoValidExtension")

#divide to GB, add *1024 for TB
reduce_csv["Allocated Filesize GB"] = [x/(1024*1024*1024) for x in reduce_csv["Allocated Filesize GB"]]

#sum of identical values
reduce_csv["Allocated Filesize GB"] = reduce_csv.groupby(["Extension"])["Allocated Filesize GB"].transform('sum')

#drop duplicates
reduce_csv.drop_duplicates(subset = "Extension", keep = 'first', inplace = True)

#open writer
writer = pd.ExcelWriter("reduce_csv.xlsx",engine='xlsxwriter')

#sort descending
reduce_csv = reduce_csv.sort_values(by='Allocated Filesize GB', ascending = False)

#write files above 10GB to writer
reduce_csv[reduce_csv["Allocated Filesize GB"] > 10].to_excel (writer, sheet_name="Data",index = False, header=True, encoding='utf-8-sig')

#show total of all
reduce_csv["Total Size GiB"] = reduce_csv["Allocated Filesize GB"].sum()
base_total = reduce_csv["Allocated Filesize GB"].sum()


#validate no DRR, add all numbers and remove added numbers from base total
print("Validate DRR")
for row in DRR_video:
    base_all_removed = base_all_removed+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()
    DRR_none=DRR_none+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()
 
for row in DRR_images:
    base_all_removed = base_all_removed+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()
    DRR_none=DRR_none+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()
    
for row in DRR_audio:
    base_all_removed = base_all_removed+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()
    DRR_none=DRR_none+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()

for row in DRR_compressed:
    base_all_removed = base_all_removed+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()
    DRR_none=DRR_none+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()

for row in DRR_pdf:
    base_all_removed = base_all_removed+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()
    DRR_none=DRR_none+reduce_csv.loc[reduce_csv['Extension']==row,'Allocated Filesize GB'].sum()


#add numbers
end_total=base_total-base_all_removed
DRR_4=end_total
reduce_csv["No DR"]=DRR_none
reduce_csv["DR 4"]=DRR_4


#drop duplicates
reduce_csv.drop_duplicates(subset = "Total Size GiB", keep = 'first', inplace = True)# drop duplicates
reduce_csv.drop_duplicates(subset = "No DR", keep = 'first', inplace = True)# drop duplicates
reduce_csv.drop_duplicates(subset = "DR 4", keep = 'first', inplace = True)# drop duplicates

#DRR logic
reduce_csv["DRR valid+not valid"]=base_total/((end_total/4)+DRR_none)
reduce_csv["DRR only valid"]=(base_total-DRR_none)/(end_total/4)

#create column list
listc = ["Total Size GiB","No DR","DR 4","DRR valid+not valid","DRR only valid"]
colo = reduce_csv[listc]
print("Write")
#write to writer
colo.to_excel(writer, sheet_name="Data Reduction",index = False, header=True, encoding='utf-8-sig')


writer.save()
writer.close()

     
#num = int(input('How many numbers: '))        


   


