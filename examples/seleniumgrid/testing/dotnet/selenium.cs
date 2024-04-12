using System;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Remote;

namespace SeleniumDotNetExample
{
    class Program
    {
        static void Main(string[] args)
        {
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
            CheckBrowser("CHROME");
        }
        static void CheckBrowser(string browser)
        {
            IWebDriver driver = null;
            try
            {
                Uri commandExecutorUri = new Uri("http://internal-af7ff2c7641ca4ca1b421a0a2bfeefc5-677996714.us-east-1.elb.amazonaws.com:4444");

                if (browser.Equals("CHROME", StringComparison.OrdinalIgnoreCase))
                {
                    ChromeOptions options = new ChromeOptions();
                    driver = new RemoteWebDriver(commandExecutorUri, options);
                }
                else if (browser.Equals("FIREFOX", StringComparison.OrdinalIgnoreCase))
                {
                    FirefoxOptions options = new FirefoxOptions();
                    driver = new RemoteWebDriver(commandExecutorUri, options);
                }

                driver.Navigate().GoToUrl("http://www.google.com");
                if (!driver.PageSource.Contains("google", StringComparison.OrdinalIgnoreCase))
                {
                    throw new Exception($"Expected 'google' not found in {browser} browser's page source.");
                }

                Console.WriteLine($"Browser {browser} checks out!");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error checking browser {browser}: {ex.Message}");
            }
            finally
            {
                driver?.Quit();
            }
        }
    }
}
