# PP-P2P-Automation

This bash script is a handy little helper to convert the performance statement CSV files from multiple P2P sites 
into the appropriate format for importing them into [Portfolio Performance](https://www.portfolio-performance.info/).

## Usage
- Define `REPOS_FOLDER` and `FINANCE_FOLDER` according to your folder structure
- Check which P2P sites you are using and adopt the script accordingly
- Check that you have downloaded the code from the relevant repos into `REPOS_FOLDER`
  - https://github.com/ChrisRBe/PP-P2P-Parser 
  - Trine: https://github.com/StegSchreck/PP-Trine-Parser
  - Auxmoney: https://github.com/StegSchreck/PP-Auxmoney-Parser
- Download the statement export from each P2P sites you are using into the appropriately named subfolders of `FINANCE_FOLDER`
- Make sure that you convert Excel files into CSV files (e.g. Bondora, Swaper, ...)
- If you are using Auxmoney, you should pass in the credentials as environment variables as `AUXMONEY_USERNAME` and `AUXMONEY_PASSWORD`
  - One possibility is to use them like this: `AUXMONEY_USERNAME='your@email.de' AUXMONEY_PASSWORD='password' ./convert.sh`
- Execute this script `./convert.sh`
- Import the resulting files into Portfolio Performance
