# eksctl setup on Windows  
## Using Chocolatey  
```bash
    choco install eksctl
```  

## OR   

Direct download (latest release): [AMD64/x86_64](https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_windows_amd64.zip) -[ARMv6](https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_windows_armv6.zip) - [ARMv7](https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_windows_armv7.zip) - [ARM64](https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_windows_arm64.zip)  

Make sure to unzip the archive to a folder in the PATH variable.  

Optionally, verify the checksum:  

1. Download the checksum file: [latest](https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt)  
2. Use Command Prompt to manually compare CertUtil's output to the checksum file downloaded.  
```bash
    REM Replace amd64 with armv6, armv7 or arm64
    CertUtil -hashfile eksctl_Windows_amd64.zip SHA256
```  
3. Using PowerShell to automate the verification using the -eq operator to get a True or False result:  

```bash
# Replace amd64 with armv6, armv7 or arm64
 (Get-FileHash -Algorithm SHA256 .\eksctl_Windows_amd64.zip).Hash -eq ((Get-Content .\eksctl_checksums.txt) -match 'eksctl_Windows_amd64.zip' -split ' ')[0]
 ```

#### Using Git Bash: 
```sh
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=windows_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.zip"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

unzip eksctl_$PLATFORM.zip -d $HOME/bin

rm eksctl_$PLATFORM.zip
```  

The `eksctl` executable is placed in `$HOME/bin`, which is in `$PATH` from Git Bash.  




