# Canary Deployment  

### Command to grep the test results  

```bash
for i in $(seq 1 10); do curl -s --resolve canary.echo.pod.name.com:80:<Ingress-Controller-IP> canary.echo.pod.name.com; done
```
```bash
for i in $(seq 1 10); do curl -s --resolve canary.echo.pod.name.com:80:24.144.71.37 canary.echo.pod.name.com; done | grep -o '<span id='\'podName\''>[^<]*' | sed 's/<[^>]*>//g'
```
