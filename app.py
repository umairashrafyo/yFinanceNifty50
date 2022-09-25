from distutils.log import debug
import pickle
from flask import Flask,app,request,jsonify,url_for,render_template
import numpy as np
import pandas as pd
import os

app=Flask(__name__)
#Load the tickers pickle file in read byte mode
tickers=pickle.load(open('yFinanceTickers.pkl','rb'))
symbolsList=['ADANIPORTS.NS',
'APOLLOHOSP.NS',
'ASIANPAINT.NS',
'AXISBANK.NS',
'BAJAJ-AUTO.NS',
'BAJFINANCE.NS',
'BAJAJFINSV.NS',
'BPCL.NS',
'BHARTIARTL.NS',
'BRITANNIA.NS',
'CIPLA.NS',
'COALINDIA.NS',
'DIVISLAB.NS',
'DRREDDY.NS',
'EICHERMOT.NS',
'GRASIM.NS',
'HCLTECH.NS',
'HDFCBANK.NS',
'HDFCLIFE.NS',
'HEROMOTOCO.NS',
'HINDALCO.NS',
'HINDUNILVR.NS',
'HDFC.NS',
'ICICIBANK.NS',
'ITC.NS',
'INDUSINDBK.NS',
'INFY.NS',
'JSWSTEEL.NS',
'KOTAKBANK.NS',
'LT.NS',
'M&M.NS',
'MARUTI.NS',
'NTPC.NS',
'NESTLEIND.NS',
'ONGC.NS',
'POWERGRID.NS',
'RELIANCE.NS',
'SBILIFE.NS',
'SHREECEM.NS',
'SBIN.NS',
'SUNPHARMA.NS',
'TCS.NS',
'TATACONSUM.NS',
'TATAMOTORS.NS',
'TATASTEEL.NS',
'TECHM.NS',
'TITAN.NS',
'UPL.NS',
'ULTRACEMCO.NS',
'WIPRO.NS']

    


#Render the homepage without any stock data
@app.route('/')
def homePage():
    return render_template('home.html')
#Render the homepage with raw stock data
@app.route('/tickers_api',methods=['POST','GET'])
def tickers_api():
    # Page = int(request.form['projectFilepath'])
    Page=int(request.form.get('projectFilepath', "1"))
    print(Page)

    dataList=[]
    for i in range(Page):
        infoDict=dict()
        oneMonthClose=(tickers[symbolsList[i]].history(period='1mo',interval='1mo').iloc[:1,3:4]).to_numpy()[0][0]
        oneMonthopen=(tickers[symbolsList[i]].history(period='1mo',interval='1mo').iloc[:1,:1]).to_numpy()[0][0]
        oneMonthChange=(oneMonthClose-oneMonthopen)/oneMonthopen
        tickerObject=tickers[symbolsList[i]].info
        infoDict['companyName']=symbolsList[i]
        infoDict['1monthChange']=str(oneMonthChange)
        infoDict['52WeekChange']=tickerObject['52WeekChange']
        infoDict['profitMargins']=tickerObject['profitMargins']
        infoDict['earningsGrowth']=tickerObject['earningsGrowth']
        infoDict['currentPrice']=tickerObject['currentPrice']
        
        dataList.append(infoDict)
    return render_template('home.html',data=dataList)
#Render the homepage with percentile ranking of stock data
@app.route('/tickers_api2',methods=['POST','GET'])
def tickers_api2():
    # Pages = int(request.form.get("pages"))
    dataList=[]
    Pages=int(request.form.get('projectFile', "1"))
    # Pages = int(request.form['projectFile'])
    print("Pages",Pages)
    for i in range(Pages):
        infoDict=dict()
        
        keys=["companyName","1monthChange","52WeekChange","profitMargins","earningsGrowth"]
        oneMonthClose=(tickers[symbolsList[i]].history(period='1mo',interval='1mo').iloc[:1,3:4]).to_numpy()[0][0]
        oneMonthopen=(tickers[symbolsList[i]].history(period='1mo',interval='1mo').iloc[:1,:1]).to_numpy()[0][0]
        oneMonthChange=(oneMonthClose-oneMonthopen)/oneMonthopen
        tickerObject=tickers[symbolsList[i]].info
        infoDict['companyName']=symbolsList[i]
        infoDict['1monthChange']=str(oneMonthChange)
        infoDict['52WeekChange']=tickerObject['52WeekChange']
        infoDict['profitMargins']=tickerObject['profitMargins']
        infoDict['earningsGrowth']=tickerObject['earningsGrowth']
        infoDict['Total']=0
        
        dataList.append(infoDict)    
    percentileList=[]
    for k in range(Pages):
        lst=[]  
        perDict=dict()
        for n in dataList[k].keys():
            if n!="companyName":
                rank=0
                value=dataList[k][n]
                total=Pages
                if value!=None:
                    for j in range(Pages):


                        compareWith=dataList[j][n]

                        if compareWith==None:
                            total-=1
                        elif (compareWith!=None):
                            if(value>=compareWith):
                                rank+=1
                        
                else:
                    perDict[n]=str(0)
                if total!=0 and value!=None:
                    perDict[n]=str("{:.2f}".format(round(((rank)/total), 2)))
                elif(value!=None):
                    perDict[n]=str(0)
            else:
                perDict[n]=symbolsList[k]
        percentileList.append(perDict)
    for f in range(Pages):
        percentileList[f]["Total"]=float(percentileList[f]["1monthChange"])+float(percentileList[f]["52WeekChange"])+float(percentileList[f]["profitMargins"])+float(percentileList[f]["earningsGrowth"])
        # percentileList[f]["companyName"]=symbolsList[f]
#         percentileList[f]["Total"]=str(percentileList[f]["Total"])
        print(percentileList[f]["Total"])
#         percentileList.append(perDict)
    percentileList.sort(key=lambda x: x["Total"], reverse=True)
    for f in range(Pages):
        percentileList[f]["Total"]=str(percentileList[f]["Total"])
    
    return render_template('home.html',dataLists=percentileList)


if __name__=='__main__':
    app.run(debug=True)  