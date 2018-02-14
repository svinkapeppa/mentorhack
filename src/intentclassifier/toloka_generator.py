import csv
with open('toloka_numbers.tsv', 'w') as f:
    c = csv.writer(f, delimiter='\t')
    c.writerow(['INPUT:idnumber'])
    for i in range(700):
        c.writerow([i+1])
