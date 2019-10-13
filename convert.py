import csv
import sys

# Redirect STDOut
sys.stdout = open('converted.csv', 'w')

# Open CSV File
file = open('TransactionExport.csv', mode='r')
csv_file = csv.DictReader(file)

# Print Header
print("date;paymode;info;payee;memo;amount;category;tags")

# Parse out the statment
for row in csv_file:
        
        # Description of the transaction
        description=""

        # Was it Point of Sale?
        POS = 0
       
        # Amount of transaction
        amount = 0

        # Ignore invalid lines
        if(not len(row["Date"])):
            continue
        

        # Parse out the POS details
        if str(row["Details"]).startswith("POS"):
                subs = str(row["Details"]).split(" ", 1)
                POS = 6
                description = subs[1].lstrip()
        else:
                description = row["Details"].lstrip()


        # Convert from Debit/Credit to abs amount
        if(not len(row["Credit"])):
            amount= 0 - float(row["Debit"])
        else:
            amount= row["Credit"]

        # Print to homebank format
        print(row["Date"]+";"+str(POS)+";;"+ description+";;"+str(amount)+";;")
