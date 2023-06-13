Fróðskaparrit - Faroese Scientific Journal
==

This directory contains the Python code used to scrape [the Fróðskaparrit - Faroese Scientific Journal online archives](https://ojs.setur.fo/index.php/frit/issue/archive/1).
The resulting JSON file contains the metadata of all the articles found.

### How to run it

Set it up:

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

And run it:

```
$ ./scrape.py
(...)
INFO:scrape:Done, 665 articles found
INFO:root:Saving articles to /Users/macbre/git/faroese-resources/frodskaparrit/articles.json ...
INFO:root:Done
```

```yaml
$ less articles.json
{
    "title": "Eitt sindur um tuberklasmittuna",
    "url": "https://ojs.setur.fo/index.php/frit/article/view/229",
    "pdf": "https://ojs.setur.fo/index.php/frit/article/download/229/293",
    "author": null,
    "abstract": "This paper is part of a treatise dealing with the clinical features of primary tuberculous infection, and the purpose of the present work is to contribute to the clinic of primary tuberculosis. Some literature about the theme is surveyed. The material used has been collected at the Tuberculosis Station of the Faroe Islands at Hoydal during the author's time of service there from 1939 to 1947. An account is given of the working plan of this tuberculosis station, where besides ordinary station work special attention is paid to the tuberculin register. The tuberculin reaction used has been Pirquet 's test. The material comprises a total of 430 cases of initial fever.\nThe fever curve for adults was typically continual, while with children it vas irregular; the duration of the fever was similar for children and adults, generally 2 or 3 weeks; in l/4 of the cases it lasted more than one month. Maximum temperature generally about 39 degrees C might, however, be higher, especially with children. The duration and height of the fever had no prognostic significance. Slow pulse was a constant symptom witli adults, but was seldom noticed with children. This relative bradycardiagenerally lasted till the middle of ihe fever period. Krythema nodosum was a frequent symptom ot' initial fever and occurred 76 times among the 430 cases of initial fever.\nSedimentation rate practically always increased, as a rule moderately, and decreased as the fever fell, but more slowly. X-rays examinations have been made during initial fever in 146 cases. X-rays changes were stated in all the children and in more than % of the adults. The changes stated were chifly enlarged hilar shadows, some had also infiltrations. Rather more than *4 had subjective symptoms, a number which is undoubtedly too low. The most frequent symptoms where retrosternal pain and soreness of the lower end of sternum, a stitch in the side, and pain between the shoulderblades. The mentioned symptoms must be supposed to bi' caused by tlie pathologic anatomic changes.",
    "published": "2022-11-25"
}
```

You can also scrape [the books published by Fróðskapur - Faroe University Press](https://ojs.setur.fo/index.php/frodskapur).

```
$ ./books.php
(...)

```

```yaml
$ less books.json
{
    "title": "The Rise of Faroese Separatism.",
    "url": "https://ojs.setur.fo/index.php/frodskapur/article/view/189",
    "pdf": "https://ojs.setur.fo/index.php/frodskapur/article/download/189/275",
    "author": "Hans Andrias S\u00f8lvar\u00e1",
    "abstract": "Hetta er ein stytt og naka\u00f0 umskriva\u00f0 ensk \u00fatg\u00e1va av b\u00f3kini&amp;nbsp;Fr\u00e1 sj\u00e1lvst\u00fdri m\u00f3ti loysing, sum kom \u00fat \u00ed desember 2014. Enska \u00fatg\u00e1van hevur harumframt eitt n\u00fdtt brot vi\u00f0 perspektivering fram til 1950ini. &amp;nbsp;\r\nT\u00ed\u00f0arskei\u00f0i\u00f0 1906-1925 er eitt serstakt t\u00ed\u00f0arskei\u00f0 \u00ed politisku s\u00f8gu F\u00f8roya. Ta\u00f0 var \u00ed hesum t\u00ed\u00f0arskei\u00f0inum, at f\u00f8royskur politikkur t\u00f3k seg upp, og lunnarnir v\u00f3r\u00f0u lagdir undir teir str\u00ed\u00f0sspurningar, sum framvegis merkja politiska l\u00edvi\u00f0 \u00ed F\u00f8royum. \u00cd b\u00f3kunum ver\u00f0ur greitt fr\u00e1, hvussu tveir politiskir flokkar, sum spruttu burtur\u00far t\u00ed somu r\u00f8rsluni, \u00ed \u00e1runum aftan\u00e1 1906 l\u00f8gdu hv\u00f8r s\u00edna k\u00f3s \u00ed spurninginum um vi\u00f0urskiftini millum F\u00f8royar og Danmark.\r\n\u00cd 1925 v\u00f3ru b\u00e1\u00f0ir flokkarnir - serliga J\u00f3annes Patursson og Oliver Effers\u00f8e - vor\u00f0nir so \u00f3samdir um politisku lei\u00f0ina, at eingin m\u00f8guleiki t\u00f3ktist vera fyri eini politiskari semju um f\u00f8roysku k\u00f3sina m\u00f3tvegis Danmark.\r\nGreitt ver\u00f0ur fr\u00e1, at royndir v\u00f3r\u00f0u gj\u00f8rdar at finna eina semju um vi\u00f0urskiftini millum F\u00f8royar og Danmark, og at eitt einm\u00e6lt L\u00f8gting \u00ed 1922 var komi\u00f0 \u00e1samt um eitt uppskot, sum skuldi sl\u00f3\u00f0a fyri eini f\u00f8royskari semju um hendan spurningin, men hetta miseydna\u00f0ist. \u00cd 1923 v\u00f3ru sj\u00e1lvst\u00fdrisf\u00f3lk farin at ivast \u00ed, um sj\u00e1lvst\u00fdrisspurningurin kundi loysast innanfyri karmarnar \u00e1 donsku grundl\u00f3gini. \u00cd b\u00f3kini ver\u00f0ur vi\u00f0 st\u00f8\u00f0i \u00ed eini greining av trimum \u00edt\u00f8kiligum politiskum str\u00ed\u00f0sspurningum grundgivi\u00f0 fyri, at ta\u00f0 \u00ed st\u00f3ran mun v\u00f3ru r\u00edkispolitiskir samanhangir, sum f\u00f8royskur politikkur gj\u00f8rdist partur av \u00ed hesum t\u00ed\u00f0arskei\u00f0inum, i\u00f0 v\u00f3ru vi\u00f0 til at seta f\u00f8roysku flokkarnar upp \u00edm\u00f3ti hv\u00f8rjum \u00f8\u00f0rum og s\u00ed\u00f0an Sj\u00e1lvst\u00fdrisflokkin upp \u00edm\u00f3ti r\u00edkismyndugleikunum.\r\nRadikaliseringin av sj\u00e1lvst\u00fdrisspurninginum hekk \u00ed st\u00f3ran mun saman vi\u00f0 st\u00f8rri r\u00edkispolitiskum t\u00fddningssamanhangum, sum ikki h\u00f8vdu so n\u00f3gv vi\u00f0 tann \u00edt\u00f8kiliga f\u00f8royska politikkin at gera.",
    "published": "2016-02-20"
}
```

### Fetching articles

`articles.json` has the information on all the publications scraped from [the Journal archive](https://ojs.setur.fo/index.php/frit).

```
$ jq .[].pdf -r articles.json | head
https://ojs.setur.fo/index.php/frit/article/download/139/239
https://ojs.setur.fo/index.php/frit/article/download/143/244
https://ojs.setur.fo/index.php/frit/article/download/140/567
https://ojs.setur.fo/index.php/frit/article/download/144/245
https://ojs.setur.fo/index.php/frit/article/download/304/414
https://ojs.setur.fo/index.php/frit/article/download/126/pdf_1
https://ojs.setur.fo/index.php/frit/article/download/131/pdf
https://ojs.setur.fo/index.php/frit/article/download/136/pdf_1
https://ojs.setur.fo/index.php/frit/article/download/127/pdf
https://ojs.setur.fo/index.php/frit/article/download/109/213
```

Combine URLs for both publications and books:

```
$ jq .[].pdf -r articles.json | grep -v null > urls.txt
$ jq .[].pdf -r books.json | grep -v null >> urls.txt
$ wc -l urls.txt 
     717 urls.txt
```

And mass-fetch it with `wget`:

```
$ wget --user-agent="faroese-resources/frodskaparrit scrapper" --input-file=urls.txt 
```
