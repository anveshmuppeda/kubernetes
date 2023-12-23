from selenium import webdriver

def check_browser(browser):
  if browser == "CHROME":
    options = webdriver.ChromeOptions()
  elif browser == "FIREFOX":
    options = webdriver.FirefoxOptions()
  driver = webdriver.Remote(
    command_executor='http://dualstack.ad02e777ace904a4fb81187be3ebc4da-937370949.us-east-1.elb.amazonaws.com/:4444/wd/hub',
    options=options
  )
  driver.get("http://www.google.com")
  assert "google" in driver.page_source
  driver.quit()
  print("Browser %s checks out!" % browser)


check_browser("FIREFOX")
check_browser("CHROME")
