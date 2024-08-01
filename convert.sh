#!/usr/bin/env bash

FINANCE_FOLDER="/mnt/DATA/Sebastian/Finanzen" # This folder contains subfolders for each P2P site
REPOS_FOLDER="/home/sebastian/repos" # This folder contains all relevant code repositories


### PARSE SCRIPT FLAGS
dry_run=false

while getopts "dh" opt; do
  case $opt in
    h)
      echo "Usage: $0 [-h] [-d]"
      exit 0
      ;;
    d)
      dry_run="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG"
      exit 1
      ;;
  esac
done


### FIND ALL RELEVANT INPUT FILES
bondora_file=$(find "${FINANCE_FOLDER}/Bondora" -type f -iname 'AccountStatement_*.csv' -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
estateguru_file=$(find "${FINANCE_FOLDER}/EstateGuru" -type f -iname 'payments_*.csv' -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
lande_file=$(find "${FINANCE_FOLDER}/Lande" -type f -iname '*-transactions.csv' -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
mintos_file=$(find "${FINANCE_FOLDER}/Mintos" -type f -iname '*-account-statement.csv' -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
swaper_file=$(find "${FINANCE_FOLDER}/Swaper" -type f -iname 'excel-storage_*.csv' -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
trine_file=$(find "${FINANCE_FOLDER}/Trine" -type f -iname 'trine-transactions-*.csv' -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
viainvest_file=$(find "${FINANCE_FOLDER}/ViaInvest" -type f -iname 'transactions_statement_*.csv' -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)

echo "Detected Bondora file: $bondora_file"
echo "Detected EstateGuru file: $estateguru_file"
echo "Detected Lande file: $lande_file"
echo "Detected Mintos file: $mintos_file"
echo "Detected Swaper file: $swaper_file"
echo "Detected Trine file: $trine_file"
echo "Detected ViaInvest file: $viainvest_file"


### PERFORM CONVERSION
if $dry_run; then
  echo "... DRY-RUN ..."
else
  echo "... PARSING ..."
  # https://github.com/ChrisRBe/PP-P2P-Parser
  pushd "$REPOS_FOLDER/PP-P2P-Parser/" || exit 1
  source ./venv/bin/activate
  python parse-account-statements.py --type bondora "$bondora_file"
  python parse-account-statements.py --type bondora_go_grow "$bondora_file"
  python parse-account-statements.py --type estateguru_en "$estateguru_file"
  python parse-account-statements.py --type lande "$lande_file"
  python parse-account-statements.py --type mintos "$mintos_file"
  python parse-account-statements.py --type swaper "$swaper_file"
  python parse-account-statements.py --type viainvest "$viainvest_file"
  popd || exit 1

  # Trine has a special format and needs to be parsed differently using a dedicated script
  # https://github.com/StegSchreck/PP-Trine-Parser
  pushd "$REPOS_FOLDER/PP-Trine-Parser/" || exit 1
  source ./venv/bin/activate
  python3 main.py -d "${FINANCE_FOLDER}/Trine" -f "$trine_file"
  popd || exit 1

  # Auxmoney offers no export and needs to be crawled from the webpage using a dedicated script
  # https://github.com/StegSchreck/PP-Auxmoney-Parser
  pushd "$REPOS_FOLDER/PP-Auxmoney-Parser/" || exit 1
  source ./venv/bin/activate
  previous_month=$(date -d '-1 month' +%Y-%m-01)
  today=$(date +%Y-%m-%d)
  python3 main.py --username "$AUXMONEY_USERNAME" --password "$AUXMONEY_PASSWORD" -d /mnt/DATA/Sebastian/Finanzen/Auxmoney --earliest "$previous_month" --latest "$today" -x
  popd || exit 0
fi

