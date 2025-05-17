const { execSync } = require('child_process');
const fs = require('fs');

const repoUrl = 'https://github.com/anveshmuppeda/aws.git';
const targetDir = './aws-guides';

if (fs.existsSync(targetDir)) {
  console.log('Removing existing aws-guides folder...');
  fs.rmSync(targetDir, { recursive: true, force: true });
}

console.log('Cloning AWS Guides repository...');
execSync(`git clone ${repoUrl} ${targetDir}`, { stdio: 'inherit' });

console.log('AWS Guides repository cloned successfully!');