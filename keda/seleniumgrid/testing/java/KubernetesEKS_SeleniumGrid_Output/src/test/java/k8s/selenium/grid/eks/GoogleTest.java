package k8s.selenium.grid.eks;


import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.Browser;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.testng.ITestContext;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.Map;

public class GoogleTest {

    private WebDriver webDriver;

    @BeforeTest
    public void setUp(ITestContext iTestContext) throws MalformedURLException {
        Map<String, String> map = iTestContext.getCurrentXmlTest().getAllParameters();
        System.out.println(map);
        this.webDriver = getWebDriver(map.get("browserName"));

    }

    private WebDriver getWebDriver(String browserName) throws MalformedURLException {
        DesiredCapabilities capabilities = new DesiredCapabilities();
        if ("chrome".equalsIgnoreCase(browserName)) {
            capabilities.setBrowserName(Browser.CHROME.browserName());
        } else if ("firefox".equalsIgnoreCase(browserName)) {
            capabilities.setBrowserName(Browser.FIREFOX.browserName());
        }
        return new RemoteWebDriver(new URL("http://ad02e777ace904a4fb81187be3ebc4da-937370949.us-east-1.elb.amazonaws.com:4444"), capabilities);
    }

    @Test
    public void printPageTitle() {
        this.webDriver.navigate().to("https://www.google.com/");
        System.out.println(this.webDriver.getTitle());
        this.webDriver.quit();
    }


    @AfterClass(alwaysRun = true)
    public void tearDown() {
        this.webDriver.quit();
    }
}
