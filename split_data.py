import sys
import argparse
import gzip

ID,FORM,LEMMA,UPOS,XPOS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

def read_documents(f):
    doc_lines=[]
    for line in f:
        line=line.strip()
        if line.startswith("###C: doc_id ="): # new document
            yield doc_lines
            doc_lines = []
            doc_lines.append(line)
            continue
        doc_lines.append(line)
    else:
        if doc_lines:
            yield doc_lines




def split_data(args):

    file_counter = 0
    doc_counter = 0

    print("Creating a new file {}{:02d}.txt.gz".format(args.outname, file_counter), file=sys.stderr)
    out_file = gzip.open("{}{:02d}.txt.gz".format(args.outname, file_counter), "wt", encoding="utf-8")

    with gzip.open(args.plaintext, "rt", encoding="utf-8") as in_file:
        for doc_lines in read_documents(in_file):
            for line in doc_lines:
                print(line, file=out_file)
            doc_counter += 1

            # need for a new file?
            if doc_counter >= args.max:
                out_file.close()
                file_counter += 1
                print("Creating a new file {}{:02d}.txt.gz".format(args.outname, file_counter), file=sys.stderr)
                out_file = gzip.open("{}{:02d}.txt.gz".format(args.outname, file_counter), "wt", encoding="utf-8")
                doc_counter = 0

    out_file.close()


    








if __name__=="__main__":

    argparser = argparse.ArgumentParser(description='Split Suomi24 plain text into smaller pieces (or any other parser input plain text with document level structure)')
    argparser.add_argument('--plaintext', default="/usr/share/ParseBank/Suomi24/Suomi24_2001-2017/Suomi24-2017H2.txt.gz", help='A plain text file extracted from the Kielipankki zipfile')
    argparser.add_argument('--max', type=int, default=10000000, help='How many documents each part should have')
    argparser.add_argument('--outname', type=str, default="/usr/share/ParseBank/Suomi24/Suomi24_2001-2017/Suomi24-2017H2-part", help='Output file name')
    args = argparser.parse_args()

    split_data(args)
