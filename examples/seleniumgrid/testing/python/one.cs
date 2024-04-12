static void CheckBrowser(string browser)
{
    IWebDriver driver = null;
    try
    {
        Uri commandExecutorUri = new Uri("http://dualstack.ad02e777ace904a4fb81187be3ebc4da-937370949.us-east-1.elb.amazonaws.com:4444/wd/hub");

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
