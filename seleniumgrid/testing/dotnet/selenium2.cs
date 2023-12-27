using System;
using System.Collections.Generic;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Remote;
using Xunit;

namespace SeleniumDotNetEksGrid
{
    public class GoogleTest
    {
        private IWebDriver _webDriver;

        public GoogleTest()
        {
            var browserName = Environment.GetEnvironmentVariable("browserName"); // Assuming you set this as an environment variable.
            _webDriver = GetWebDriver(browserName);
        }

        private IWebDriver GetWebDriver(string browserName)
        {
            DesiredCapabilities capabilities = new DesiredCapabilities();
            if (browserName.Equals("chrome", StringComparison.OrdinalIgnoreCase))
            {
                capabilities.SetCapability(CapabilityType.BrowserName, "chrome");
                return new RemoteWebDriver(new Uri("http://afbf78fd168e443d2af9932857f730b9-373658744.us-east-1.elb.amazonaws.com:4444/wd/hub"), capabilities);
            }
            else if (browserName.Equals("firefox", StringComparison.OrdinalIgnoreCase))
            {
                capabilities.SetCapability(CapabilityType.BrowserName, "firefox");
                return new RemoteWebDriver(new Uri("http://afbf78fd168e443d2af9932857f730b9-373658744.us-east-1.elb.amazonaws.com:4444/wd/hub"), capabilities);
            }
            throw new ArgumentException($"Unsupported browser: {browserName}");
        }

        [Fact]
        public void PrintPageTitle()
        {
            _webDriver.Navigate().GoToUrl("https://www.google.com/");
            Console.WriteLine(_webDriver.Title);
            _webDriver.Quit();
        }
    }
}
