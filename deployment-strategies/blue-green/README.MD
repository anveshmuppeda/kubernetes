# Blue-Green Deployment Strategy  

## Command to grep the test results   

### Syntax   
```bash
for i in $(seq 1 10); do curl <app-url>; done | grep -o '<span id='\'podName\''>[^<]*' | sed 's/<[^>]*>//g'
```

### Example   
```bash
for i in $(seq 1 10); do curl 146.190.55.322:32266; done | grep -o '<span id='\'podName\''>[^<]*' | sed 's/<[^>]*>//g'
```

