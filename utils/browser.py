import os

from selenium import webdriver

def make_chromebrowser(*options) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    

    if options:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')
            
    browser = webdriver.Chrome(options=chrome_options)
    
    return browser

 
if __name__ == '__main__':
    browser = make_chromebrowser()
    
    browser.get('https://www.google.com.br')
    
    input("Pressione Enter no terminal para fechar o navegador...")