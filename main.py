# %%
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pickle
from datetime import datetime
import selenium.common.exceptions as exce
import sys
from flask import Flask,jsonify,Response
from flask_cors import CORS
import json
import pandas as pd
from flask import render_template , redirect , url_for ,request



# %%


xlsxFile = ""
baseUrl = r"https://ant.aliceblueonline.com/dashboard"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

try:
    driver = Chrome("./chromedriver.exe",chrome_options=options)
except exce.WebDriverException:
    driver = Chrome(chrome_options=options)
actions = ActionChains(driver)



driver.get("https://ant.aliceblueonline.com/dashboard")



try:
    user_id = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/main/div[1]/form/div[1]/div/input')
    password = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/main/div[1]/form/div[2]/div/input')
    login_button = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/main/div[1]/form/button')
    user_id.send_keys('AB017549')
    password.send_keys('bnm@1234')
    login_button.click()

    wait = WebDriverWait(driver,60).until(EC.invisibility_of_element((By.XPATH,'//*[@id="root"]/div/div[2]/main/div[1]/form/div[2]/div/input')))
    dob = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/main/div[1]/form/div/div/input')
    submit_button = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/main/div[1]/form/button')
    dob.send_keys('1981')
    submit_button.click()
    
    wait = WebDriverWait(driver,60).until(EC.invisibility_of_element((By.XPATH,'//*[@id="root"]/div/div[2]/main/div[1]/form/div/div/input')))
    pickle.dump( driver.get_cookies() , open("./cookies.pkl","wb"))
except exce.NoSuchElementException:
    pass




def openAllTabs():
    for i in range(10):
        try:
            global all_symbol_elements
            wait = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]')))
            market_watch_container_div = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]')
            all_symbol_elements = market_watch_container_div.find_elements(By.CLASS_NAME,'instruments')
            
            break
        except exce.TimeoutException:
            driver.get("https://ant.aliceblueonline.com/dashboard")
            continue
    for idx,symbol in enumerate(all_symbol_elements,1):
        # actions.move_to_element(symbol).perform()
        driver.execute_script("arguments[0].scrollIntoView();", symbol)
        market_depth_button = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/li/div[2]/div[3]/button')   
                                                           
                                                        
        market_depth_button.click()
        sleep(0.4)

try:
    openAllTabs()
except :
    pass



bought_scripts = []





# %%


# %%
def buyPL(current_price,bought_price):
     current_price = getInteger(current_price)
     bought_price = getInteger(bought_price)
     return (current_price-bought_price)/bought_price*100
    
def sellPL(current_price,sold_price):
     current_price = getInteger(current_price)
     sold_price = getInteger(sold_price)
     return (sold_price-current_price)/current_price*100

def compareOpenWithHighLow(_open,high,low):
    _open = "".join(_open.split(','))
    high = "".join(high.split(','))
    low = "".join(low.split(','))
    if((_open)==(high)):
        return "(Open = High)"
    elif((_open)==(low)):
        return "(Open = Low)"
    else:
        return "-"

def compareTBQandTSQ(tbq,tsq):
    try:    
         div = int(tbq)-int(tsq)
         diff=int(int(div)/int(tbq)*100)
         return str(diff)+"%"
    except ZeroDivisionError:
        return "-"
    


def getInteger(val):
    return int("".join(str(val).split(",")).split('.')[0])

def scrapeData(idx):
    try:
        name    = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/li/div[1]/span/div/div[1]/h6').text
        current = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/li/div[1]/span/div/div[2]/p' ).text
        _open   = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/div/ul/li/div/div[1]/table/tbody[1]/tr/td/h6').text
        high    = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/div/ul/li/div/div[1]/table/tbody[2]/tr/td/h6').text
        low     = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/div/ul/li/div/div[2]/table/tbody[2]/tr/td/h6').text
        close   = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/div/ul/li/div/div[2]/table/tbody[1]/tr/td/h6').text
        tbq     = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/div/ul/li/div/div[2]/table/tbody[3]/tr/td/h6').text
        tsq     = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/div/ul/li/div/div[2]/table/tbody[4]/tr/td/h6').text
        return name,current,_open,high,low,close,tbq,tsq
    except exce.NoSuchElementException:
        driver.refresh()
        openAllTabs()
    
def buy(idx,qty):
    try:
        wait = WebDriverWait(driver,60).until(EC.invisibility_of_element((By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div')))
        buy_button = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/li/div[2]/div[1]/button')   
        driver.execute_script("arguments[0].scrollIntoView();", buy_button)
        buy_button.click()
        qty_input =  WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/div/div/input')))
        qty_input.send_keys(Keys.CONTROL,"a",Keys.BACK_SPACE)
        qty_input.send_keys(qty)
        final_buy_button = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[4]/div/div/div/div[1]/div/div[3]/div[2]/button[1]')
        final_buy_button.click()
    except exce.TimeoutException:
        pass
    
def sell(idx,qty):
    try:
        wait = WebDriverWait(driver,60).until(EC.invisibility_of_element((By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div')))
        sell_button = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[{idx}]/div/ul/li/div[2]/div[2]/button')
        driver.execute_script("arguments[0].scrollIntoView();", sell_button)
        sell_button.click()
        qty_input =  WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div[4]/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/div/div/input')))
        qty_input.send_keys(Keys.CONTROL,"a",Keys.BACK_SPACE)
        qty_input.send_keys(qty)
        final_sell_button = driver.find_element(By.XPATH,f'//*[@id="root"]/div/div[4]/div/div/div/div[1]/div/div[3]/div[2]/button[1]')
        final_sell_button.click()
    except exce.TimeoutException:
        pass
    
def timeFormat(time):
    if(len(str(time))<2):
        return "0"+str(time)
    return str(time)

to_take_entry = {}
entered = {}
averaging_entries = {}


# %%


app = Flask(__name__)



@app.route('/logs',methods=['POST'])
def sendlog():
    try:
        name = request.form['scripcode']
        averaging_action = ""
        if(name in averaging_entries):
            averaging_action = averaging_entries[name]
        return render_template('logs.html',actions=entered[name],averaging_entries=averaging_action,name=name)
    except KeyError:
        return jsonify({"message":"No entries"})

        

@app.route('/editaction',methods=['POST'])
def editaction():
    try:
        name = request.form['scripcode']
        return render_template('editaction.html',actions=to_take_entry[name],name=name)
    except KeyError:
        return jsonify({"message":"No action to be taken"})

    
    
@app.route('/removeaction',methods=['POST'])    
def removeaction():
     name = request.form['scripcode']
     action_idx = request.form['action_index']
     to_take_entry[name].pop(int(action_idx))
     if(not len(to_take_entry[name])):
            to_take_entry.pop(name)
     return  Response(status=200)

     

    
    
@app.route('/addaction',methods=["POST"])
def addaction():
    now = datetime.now()
    current_hour = timeFormat(now.hour)+":"+timeFormat(now.minute)
    if(request.form['time']<current_hour):
        return jsonify({"status":"faild"})
    if request.method == 'POST':
      name = request.form['scripcode']
      time = request.form['time']
      action_ = request.form['action']
      breakprice = request.form['breakprice']
      averaging = float(request.form['averaging'])
      qty = request.form['qty']
      new_action = {"time":time,"action":action_,"breakprice":breakprice,"qty":qty,"averaging":averaging}
      try:
          to_take_entry[name].append(new_action)
      except KeyError:
          to_take_entry[name] = [new_action]
      return redirect('/home')
    

@app.route('/home')
def home():
    return render_template('home.html',scrips=[e for e,ele in enumerate(all_symbol_elements) ])


@app.route('/getdata')
def sendata():
    now = datetime.now()
    current_hour = str(now.hour)+":"+str(now.minute)
    all_scripts = []
    for idx,symbol in enumerate(all_symbol_elements,1):
        name,current ,_open,high,low ,close,tbq ,tsq   = scrapeData(idx)            
        try:
            actions = to_take_entry[name]
            for action in actions:
                if(action['time'] == current_hour):
                    if(action['action']=="B"):
                        if(getInteger(current)<=int(action['breakprice'])):
                            buy(idx,action['qty'])
                            to_take_entry.pop(name)
                            if(action["averaging"]):
                                averaging_entries[name] = {"live":True,"price":getInteger(current),"qty":action["qty"],"break":action["averaging"],"action":"B","time":now,"entries":[]}
                            try:
                                entered[name].append({"action":"bought","time":now,"price":current})
                            except KeyError:
                                entered[name] = [{"action":"bought","time":now,"price":current}]
                    elif(action['action']=="S"):
                        if(getInteger(current)>=int(action['breakprice'])):
                            sell(idx,action['qty'])
                            to_take_entry.pop(name)
                            if(action["averaging"]):
                                averaging_entries[name] = {"live":True,"price":getInteger(current),"qty":action["qty"],"break":action["averaging"],"action":"S","time":now,"entries":[]}
                            try:
                                entered[name].append({"action":"sold","time":now,"price":current})
                            except KeyError:
                                entered[name] = [{"action":"sold","time":now,"price":current}]
        except KeyError:
            pass
        
        
        
            
        open_comparision = compareOpenWithHighLow(_open=_open,high=high,low=low)
        tbq_tsq = compareTBQandTSQ(tbq=tbq,tsq=tsq)
        stock = {"name":name,"current":current,"open" : _open,"high":high,"low":low,"close":close,"tbq":tbq,"tsq":tsq,"open_comparision":open_comparision,"tbq_tsq":tbq_tsq}
        
            
        if(name in averaging_entries):
            averaging_action = averaging_entries[name]
            if(averaging_action['live']): 
                action = averaging_action["action"]
                break_ = float(averaging_action["break"])
                price = (getInteger(averaging_action["entries"][-1] if averaging_action["entries"] else averaging_action['price']))

                quantity = averaging_action['qty']
                current_int = getInteger(current)

                if(action == "S"):
                    if(current_int>=float(price+price*break_/100)):
                       print(current_int,"-",float(price+price*break_/100))
                       sell(idx,quantity)
                       averaging_entries[name]["entries"].append(current_int)

                elif(action=="B"):
                    if(current_int<=float(price-price*break_/100)):
                       print(current_int,"-",float(price+price*(break_)/100))
                       buy(idx,quantity)
                       averaging_entries[name]["entries"].append(current_int)

        if(name in entered):
            stock[entered[name][-1]["action"]]=True
            all_entries = entered[name]
            profit_loss = 0
            for entry in all_entries:
               if(entry["action"]=="sold"):
                    profit_loss+=sellPL(current,entry["price"])
               elif(entry["action"]=="bought"):
                    profit_loss+=buyPL(current,entry["price"])
            profit_loss/=len(all_entries)
            stock['profit_loss'] = f'{profit_loss:.2f}'+"%"
        all_scripts.append(stock)
    return json.dumps(all_scripts)

  
@app.route('/opentab')
def opentab():
    driver.get('https://ant.aliceblueonline.com/dashboard')
    sleep(4)
    openAllTabs() 
    return  Response(status=200)

print("created")

# %%
       
if __name__ == "__main__":
    CORS(app)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.config['JSON_SORT_KEYS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=3000)



# %%
print(averaging_entries)

# %%


# %%



