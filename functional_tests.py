from selenium import webdriver


browser = webdriver.Firefox()
browser.get('http://localhost:8000')
print('selen')
assert 'GettingStarted' in browser.title
