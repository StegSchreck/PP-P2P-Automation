#!/usr/bin/env bash

FINANCE_FOLDER="/mnt/DATA/Sebastian/Finanzen" # This folder contains subfolders for each P2P site
REPOS_FOLDER="/home/sebastian/repos" # This folder contains all relevant code repositories

viainvest_file=$(find "${FINANCE_FOLDER}/ViaInvest" -type f -iname 'transactions_statement_*.csv' -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
echo "Detected ViaInvest file: $viainvest_file"

echo "Fixing ViaInvest CSV file: $viainvest_file"
python3 fix_viainvest_csv.py "$viainvest_file" viainvest_fixed.csv
mv viainvest_fixed.csv "$viainvest_file"
rm -rf viainvest_fixed.csv

pushd "$REPOS_FOLDER/PP-P2P-Parser/" || exit 1
source ./venv/bin/activate
echo "Parsing ViaInvest file: $viainvest_file"
python parse-account-statements.py --type viainvest "$viainvest_file"
popd
