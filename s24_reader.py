# Try to construct original plain text back from Kielipankki VRT files. Include metadata as '###C:' comment lines.
# Comment:
# each post treated as a separate documents, paragraph boundaries (\n\n)  inside a post are included (exracted from <paragraph> tags), detokenized using SpaceAfter=No, but does not preserve other spacing (i.e. single new lines etc...)
# documents are not guaranteed to be in any particular order

import zipfile
import argparse
import sys
import re
import ftfy


FORM, LEMMA, UPOS, FEATS, ID, HEAD, DEPREL, MISC, _ = range(9) # corresponding UD columns

def fix_encoding(text):
    return ftfy.fix_text(text, uncurl_quotes=False)


meta_regex = re.compile('([a-z]+)="([^"]+)"', re.UNICODE)

def extract_meta(line):

    # <text comment="1520" date="2001-06-27" datetime="2001-06-27 13:51:00" nick="pois pois" parent="1456" quote="1519" signed="0" thread="173" time="13:51:00" title="taxiautoilijan keskisormi" topics="3220,10,2" type="comment">

    title = ""
    meta_lines = []
    metadata_fields = meta_regex.findall(line)
    for key, value in metadata_fields:
        if key == "title":
            title = fix_encoding(value)
            meta_lines.append(key + " = " + title)
            continue
        meta_lines.append(key + " = " + value)

    return title, meta_lines


def read_s24(f):

    meta = []
    text = ""
    title = ""

    for line in f:
        line=line.decode("utf-8").strip()
        if not line:
            continue
        if line.startswith("<text comment"): # new post starts
            if len(text) > 0:
                yield title, meta, text
            meta = []
            text = ""
            title = ""
            title, meta = extract_meta(line)
            continue
        if line == "</paragraph>": # end of paragraph, means \n\n in original text
            text += "\n\n"
            continue
        if line.startswith("<paragraph") or line.startswith("</paragraph") or line.startswith("<sentence") or line.startswith("</sentence") or line.startswith("<!--") or line.startswith("</text"):
            # these I don't care because I want to compile original raw text back
            continue
        # must be an actual token line
        cols = line.split("\t")
        if len(cols) != 9:
            print("Weird line, skipping...", line, file=sys.stderr)
            continue
        if cols[MISC] == "SpaceAfter=No":
            text += cols[FORM]
        else:
            text += cols[FORM]+" "

    else:
        if len(text) > 0:
            yield title, meta, text



def main(args):
    zip_=zipfile.ZipFile(args.zipfile)
    fnames = zip_.namelist()
    counter = 0
    for fname in fnames:
        print(fname, file=sys.stderr)
        with zip_.open(fname) as f:
            for title, meta, text in read_s24(f):
                counter += 1
                print("###C: doc_id =", counter)
                print("###C: filename =", fname)
                for m in meta:
                    print("###C:", m)
                print(fix_encoding(text))
                print("")
                




if __name__=="__main__":

    argparser = argparse.ArgumentParser(description='Suomi24 VRT reader')
    argparser.add_argument('--zipfile', default="/usr/share/ParseBank/Suomi24/Suomi24_2001-2017/Suomi24-2017H2.zip", help='zipfile downloaded from kielipankki')
    args = argparser.parse_args()

    main(args)


