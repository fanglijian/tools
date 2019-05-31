# -*- coding: utf-8  -*-
import csv
import os

ignoreFieldList = ["saved", "created", "updated","gain_point", "lon"]
def ignoreField(fieldName):
	return fieldName in ignoreFieldList

ignoreValueList = ["null", "Null", "NULL"]
def ignoreValue(value):
	return value in ignoreValueList

tableNames = {"order_num" : "orders", 
				"receivable" : "one_order", 
				"final_price" : "order_item", 
				"payment_id" : "order_payment", 
				"paid_score" : "payment", 
				"expect_time" : "order_delivery",
				"order_delivery_id" : "order_delivery_process", 
				"task_consume" : "staff_performance"}
def getTableName(tableName, keyStr):
	for fieldName in keyStr:
		s = tableNames.get(fieldName, "")
		if len(s) > 0:
			return s
	return tableName

filePath = "data/"
def fix(fileName, tableName):
	f = open(filePath + fileName,mode='r',encoding='utf-8',newline='')
	csc_file = csv.reader(f)
	keyStr = None
	valueList = []
	outputStr = "";
	if csc_file ==  None:
		print(fileName +  "is empty")
		f.close()
		return  ""
	for line in csc_file:
		if line ==  None:
			print("data is null, file name : " +  fileName)
			continue
		if keyStr == None:
			keyStr = line
		else:
			valueList.append(line)
	if keyStr == None:
		print("keyStr is null, file name : " +  fileName)
		f.close()
		return ""
	keyLength = len(keyStr)
	tableName = getTableName(tableName, keyStr)
	for values in valueList:
		index = 0
		for value in values:
			if index == 0:
				outputStr += tableName + "\n"
			if index >= keyLength:
				continue
			if ignoreValue(value) or ignoreField(keyStr[index]):
				index += 1
				continue
			outputStr+=("	" + keyStr[index]  + "=" + value +  "\n")
			index += 1
	f.close()
	return outputStr



def main():
	dataFiles = os.listdir("data")
	outputFile = open("output.txt","w")
	for fileName in dataFiles:
		index = fileName.rfind('.')
		tableName = fileName[:index]
		fileType  =  fileName[index:]
		if not fileType == ".csv":
			print("this file not support fileName :  " + fileName)
			continue
		outputStr = fix(fileName,tableName)
		outputFile.write(outputStr)
	outputFile.close()

if __name__ == '__main__':
    main()

