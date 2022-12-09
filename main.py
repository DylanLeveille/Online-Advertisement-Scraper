import pandas as pd
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from adblockparser import AdblockRules
import time
from io import StringIO
import lxml.etree
import re
import sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary



csvPath = "top-1m-2022-10-22.csv/top-1m.csv"
easyListPathEN = "EasyList/easylist-en.txt" #Canada
easyListPathPT = "EasyList/easylist-pt.txt" #Brazil
easyListPathDE = "EasyList/easylist-de.txt" #Germany
easyListPathIN = "EasyList/easylist-in.txt" #India
easyListPathAR = "EasyList/easylist-ar.txt" #Egypt

options = {
    "third-party" : True,
    "script" : True,
    "object": True,
    "subdocument": True,
    "document": True,
    "image": True,
    "xmlhttprequest": True,
    "stylesheet": True,
    "media": True
}

rowsToUse = 1000

with open(easyListPathAR, 'rb') as f:
    raw_rules = f.read().decode('utf8').splitlines()

f.close()

rules = AdblockRules(raw_rules)

def runExperiment():
    dfTop = pd.read_csv(csvPath, nrows=rowsToUse, header=None)

    dfMiddle = pd.read_csv(csvPath, skiprows=500000, nrows=rowsToUse, header=None)

    dfBottom = pd.read_csv(csvPath, skiprows=1000000 - rowsToUse, nrows=rowsToUse, header=None)

    binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')

    df = pd.concat([ dfTop, dfMiddle, dfBottom])



    open('adURLs.csv', 'w').close() #clear contents of this document


    print(rules.should_block("https://googleads.g.doubleclick.net/aclk?sa=l&ai=CtNP362VVY_iPLfCSwNYPzv2B2AuW3peDbN3BvJmDD_rQ8tCIARABILqEwDNgyYaAgICA2A-gAfLcmOUCyAEG4AIAqAMBqgSlAk_QqumaFKrCZvkNAloxivhHoaW5abMk0QYLX21HBFuK8CbgFbPsO7a4MEgxj92JjfnnIE_pyv5CMrSgNGC9RHo-mggOJv6LnmLw8AcHv8mOz24tfy1lC6zaDnPU0SpEI6jnMxX28VWGJxrjDgIR9iyypjjKPygJEBMY0wxRs4RrrHADB9L0Ul9D6OnJcmjJgmLxvj4JzGgSBGQaWTQ2pSNeLxGTql1xqrnjNbCUEdDGQ2X3CXHnoVQBFW7zI6nYsjibVo8BQ6aivsfHGbytpUAgvJzT_ZTuYTOnNpe8l6ZIVHLKYzu8-_PyoN8AiromqSQ_B4lzhMBXGPsZfDP8D20vlxPJSg7KkcbeUgn_ex60fQ-Vp5EomJ2aJ9vJ0mBubN99Pg0BwATCh_nl7gPgBAGAB_ai55oBqAeOzhuoB5PYG6gH7paxAqgH_p6xAqgHpKOxAqgH1ckbqAemvhuoB5oGqAfz0RuoB5bYG6gHqpuxAqgH_56xAqgH35-xAtgHAdIIDwiAYRABGB0yAooCOgKAQPIIG2FkeC1zdWJzeW4tOTYxMTc2MDEyMTEyMDEyNLEJGn4NS9TitEeACgOYCwHICwG4DAHYEw2IFAHQFQGYFgH4FgGAFwE&ae=1&num=1&cid=CAQSOwDq26N9e3H84nfO3Ugo6iMkiPtF6-_PVQhSXzIOgv_-d7GgKr4QB7a6SA1jPujoXvVI437MPKvm3aziGAEgDg&sig=AOD64_0Q9VZxWQEeHWCnCnQZLspfVeGzJA&client=ca-pub-8933329999391104&nb=1&adurl=https://mattermost.com/guide-to-developer-productivity-download/%3Futm_source%3Dgoogle%26utm_medium%3Dcpc%26utm_campaign%3DGoogle_Display_DevProdGuide_NA_01devsites%26utm_term%3D%26utm_placement%3Dwww.javatpoint.com%26gclid%3DEAIaIQobChMIuLHBk932-gIVcAnQBB3OfgC7EAEYASAAEgJ6wfD_BwE", {'third-party': True}))
    print(rules.should_block("https://www.googleadservices.com/pagead/aclk?sa=L&ai=CN4DoWPVWY8LpHIPk48APopaWyAKW3peDbN3BvJmDD_rQ8tCIARABILqEwDNg_biUgegDoAHy3JjlAsgBBuACAKgDAaoEnwJP0Lc4ouUqXingX1APBR2z_m0z1IwvLGdpQePm1fTPHY7oKh3ciWar1pEaIAX_Z0oXcNzoO0anrIXLUWR7wm4EEFYY-SU6JdYz4_LeRtCd31HEQoExZHCR7OC2e98OGB5Qh9uFm4rO250PF1XiCNHN9OyoNWevgeOwMN6as9uH19zIiMJlXgLy8dFea2goUifq19Twagc7SKNXLCkPCRi0nM6EOMzJqcGYW8DC9d2E1EtI7BjDlT1wAVgWJSp-T9zzSJGiCeyCAbvsbzH_zvlnRA1OyGIm8XtrxoUiw7mrNKc0mX_qYjP-jBupTIheHbh8IcxnuY7QSPvQwr4fdvY01pid4aY48sMMBhf_4jCxTp0ZzYfTTli8u5OX-g1ldMAEwof55e4D4AQBgAf2oueaAagHjs4bqAeT2BuoB-6WsQKoB_6esQKoB6SjsQKoB9XJG6gHpr4bqAeaBqgH89EbqAeW2BuoB6qbsQKoB_-esQKoB9-fsQLYBwHSCA8IgGEQARgdMgKKAjoCgEDyCBthZHgtc3Vic3luLTk2MTE3NjAxMjExMjAxMjSxCRp-DUvU4rRHgAoDmAsByAsBuAwB2BMNiBQB0BUBmBYB-BYBgBcB&ae=1&num=1&cid=CAQSOwDq26N95gfhRsezSiieMIMbjqYXzaDQ9jCUwwGrebdKHvQT8J4t2upGBbsl1vMUSRlRB78_JXhF6w88GAEgDg&sig=AOD64_32M8PxGXIQwo2eME2mx6OnBWg2OA&client=ca-pub-8933329999391104&nb=1&adurl=https://mattermost.com/guide-to-developer-productivity-download/%3Futm_source%3Dgoogle%26utm_medium%3Dcpc%26utm_campaign%3DGoogle_Display_DevProdGuide_NA_01devsites%26utm_term%3D%26utm_placement%3Dwww.javatpoint.com%26gclid%3DEAIaIQobChMIwvW0idr5-gIVA_IYAh0iiwUpEAEYASAAEgJfCfD_BwE", options))


    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  # Do not wait for full page load

    driver = webdriver.Firefox(firefox_binary=binary, executable_path="C:\\Users\\dylan\\Downloads\\geckodriver-v0.32.0-win32\\geckodriver.exe")#webdriver.Chrome(executable_path="C:\\Users\\dylan\\Downloads\\chromedriver_win32\\chromedriver.exe")
    driver.set_page_load_timeout(60*2) #timeout is 2 minutes


    driver.command_executor.set_timeout(10)

    driver.get("https://google.com")

    driver.execute_script('''window.open("http://bings.com","_blank");''')
    driver.switch_to.window(driver.window_handles[0])

    parser = lxml.etree.HTMLParser()

    for index, row in df.iterrows():
        print(row[1])

        try:
            url = row[1]# "www.javatpoint.com/selenium-python" for testing is good

            driver.delete_all_cookies()
            try:
                driver.get("http://" + url)
            except selenium.common.exceptions.TimeoutException:
                driver.execute_script("window.stop();")


            driver.execute_script("setTimeout(function(){ debugger }, 5000)")
            time.sleep(5)



            file = open("test", "w")

            tree = lxml.etree.parse(StringIO(driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")), parser)
            file.write(lxml.etree.tostring(tree, pretty_print=True).decode("utf-8"))
            #print(lxml.etree.tostring(tree, pretty_print=True))
            #iframes = tree.findall(".//iframe")
            #print(iframes)
           # print(lxml.etree.tostring(iframes, pretty_print=True))
            linksToSave = getElements(driver, 0, url, False)

            ratings = []

            driver.switch_to.window(driver.window_handles[1])
            for link in linksToSave:
                print("linked to save: ")
                print(link)
                driver.get("https://www.urlvoid.com/")
                time.sleep(3)
                urlEntry = driver.find_element(By.ID, "hf-domain")
                driver.execute_script("arguments[0].setAttribute('value',arguments[1])", urlEntry, link)
                driver.find_elements(By.CLASS_NAME, "btn-success")[0].click()
                time.sleep(10)

                try:

                    # selenium.webdriver.support.ui.WebDriverWait(driver, 60*5).until(EC.url_contains("scan"))
                    driver.find_elements(By.CLASS_NAME, "label-warning")[0].text

                    time.sleep(60 * 60)  # sleep 1 hour to reset and try again
                    driver.get("https://www.urlvoid.com/")
                    time.sleep(3)
                    urlEntry = driver.find_element(By.ID, "hf-domain")
                    driver.execute_script("arguments[0].setAttribute('value',arguments[1])", urlEntry, link)
                    driver.find_elements(By.CLASS_NAME, "btn-success")[0].click()
                    time.sleep(10)

                except IndexError: #means there is no need for URLvoid to "reset"
                    try:
                        ratings.append(str(driver.find_elements(By.CLASS_NAME, "label-success")[0].text))
                    except IndexError:
                        try:
                            ratings.append(str(driver.find_elements(By.CLASS_NAME, "label-danger")[0].text))
                        except IndexError:
                            ratings.append("N/A")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])

            time.sleep(1)
            if len(linksToSave) > 0:
                data = pd.DataFrame({"href": linksToSave, "rating": ratings})
                data["Website Source"] = url

                data.to_csv("adURLs.csv", mode='a', index=False, header=False)

        except Exception as e:
            print(e, file=sys.stderr)
            time.sleep(2)
    driver.close()
    driver.quit()


def getElements(driver, depth, url, isParentAd):
    iframes = driver.find_elements(By.TAG_NAME, "iframe")

    print(iframes)
    linksToSave = []


    for iframe in iframes:
        try:
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(iframe))
            depth = depth + 1

            links = driver.find_elements(By.TAG_NAME, "a")

            tmpLinksToSave = []
            isAd = False
            for link in links:
                href = link.get_attribute("href")

                if href is not None:
                    print("before split")
                    print(href)
                    isAd = isAd or rules.should_block(href, options)
                    splits =  re.split("https://|http://", href)[1::]
                    if (len(splits) > 1):  # if url is composed of multiple links, remove first as this is just the adserver (e.g. googleads)
                        splits = splits[1::]

                    for e in splits:
                        if "adssettings.google.com/whythisad" not in e:
                            print("splitted")
                            print(e)
                            tmpLinksToSave.append(e)

            if isParentAd or isAd: #save links if ad, or if parent iframe was an ad
                linksToSave += tmpLinksToSave
                if (depth < 7) :
                    linksToSave += getElements(driver, depth, url, True)


        except Exception as e:
            print(e, file=sys.stderr)

        driver.switch_to.parent_frame()
    print("get Elements link to save")
    print(linksToSave)
    return linksToSave



if __name__ == '__main__':
    runExperiment()

