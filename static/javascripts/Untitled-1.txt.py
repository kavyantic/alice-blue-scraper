def buyPL(current_price,bought_price):
     current_price = getInteger(current_price)
     bought_price = getInteger(bought_price)
     return (current_price-bought_price)/bought_price*100
    
def sellPL(current_price,sold_price):
     current_price = getInteger(current_price)
     sold_price = getInteger(sold_price)
     return (current_price-sold_price)/current_price*100

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
    return int("".join(val.split(",")).split('.')[0])

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
    try
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

to_take_entry = {}
entered = {}
