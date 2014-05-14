

def dialect(fp):
    'Guess the dialect of a CSV file.'
    pos = fp.tell()
    dialect = csv.Sniffer().sniff(fp.read(1024))
    csvfile.seek(pos)
    return dialect
