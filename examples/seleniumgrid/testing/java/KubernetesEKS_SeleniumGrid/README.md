# Kubernetes EKS SeleniumGrid Testing  
This repo demonstrated how to set up Selenium Grid on EKS Cluster. This repo also demonstrated how to scale the grid using KEDA

## Steps to setup the project  
1. Copy this java code  
2. Upload the java directory into the Eclipse  
3. Go to Help > Eclipse Marketplace.  
4. Search for "TestNG" and install the TestNG plugin.  
5. Update the end point(i.e., RemoteWebDriver URL) in below path
    ```/src/test/java/k8s/selenium/grid/eks/GoogleTest.java```

## Steps to run:  
1. Open your project in Eclipse.  
2. In the Project Explorer or Package Explorer, locate your testng.xml file.  
3. Right-click on testng.xml.  
4. Select Run As > TestNG Suite.  
