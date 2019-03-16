import re


def txt_to_csv(txt_fname, csv_fname=None, quote=False, delimiter=','):
    ''' helper to copy a text file with format "x y" into a csv with "x,y"

    csv_fname name of csv file
    quote if true then encapulate 2nd datum in quotes
    '''
    if csv_fname is None:
        csv_fname = txt_fname.replace('txt', 'csv')

    f_txt = open(txt_fname)
    f_csv = open(csv_fname, 'w')
    line = f_txt.readline()
    while line:
        if quote:
            # split on first space and quote second part
            datum1, datum2 = line.split(" ", 1)
            datum2 = datum2.replace("\n", "")  # wierd
            datum2 = datum2.replace('"', '""')
            line = datum1 + delimiter + '"' + datum2 + '"\n'
        else:
            line = line.replace(' ', delimiter, 1)
        f_csv.write(line)
        line = f_txt.readline()
    f_txt.close()
    f_csv.close()
    return csv_fname


def get_category_names(txt_fname, csv_fname=None):
    f_txt = open(txt_fname)
    f_csv = open(csv_fname, 'w')
    count = 0
    line = f_txt.readline()
    while line:
        search = re.search('.*:(.*);.*', line)
        name = search.group(1)
        # skip if no match
        if name:
            name = name.replace("_", " ")
            f_csv.write("{},{}\n".format(count, name))
        else:
            raise Exception("no match - {}".format(line))
        line = f_txt.readline()
        count += 1
    f_txt.close()
    f_csv.close()
    return csv_fname
