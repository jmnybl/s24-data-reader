# s24-data-reader
A python reader for processing Suomi24 data (http://urn.fi/urn:nbn:fi:lb-2019021101)

Usage: `python3 s24_reader.py --zip Suomi24-2017H2.zip | gzip -c > Suomi24-2017H2.txt.gz`

Reads Suomi24 VRT files from the zip, and returns plain text, where metadata lines are marked with `###C:`. Text is detokenized using the SpaceAfter=No tags and paragraph boundaries are preserved, but other whitespace tokens are not included. Each post is a new document with all metadata preserved. Posts are not guaranteed to be in any particular order.

Example of the output:
```
###C: doc_id = 9
###C: filename = Suomi24-2017H2/comments2003a.vrt
###C: comment = 9
###C: date = 2001-07-10
###C: datetime = 2001-07-10 15:00:00
###C: nick = opelisti
###C: parent = 0
###C: quote = 0
###C: signed = 0
###C: thread = 5
###C: time = 15:00:00
###C: title = Käyttömaksu
###C: topics = 3220,10,2
###C: type = comment
On näitä erilaisia käyttömaksuja muuallakin. Ne on vain järjestelty eri tyyppisiksi maksuiksi. Esimerkiksi Ranskassa ja Sveitsissä peritään tiemaksuja yms. 

Täytyy vain muistaa, että muualla autot ja bensa ovat yleensä melko paljon halvempia. Suomessahan on ennätyskorkea autovero ja käyttömaksu ja sikakallis bensa. 

Eli eihän tuo käyttömaksu yksistään mikään paha ole, mutta tämä kokonaisverotus tappaa!
```
