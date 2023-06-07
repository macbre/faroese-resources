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
./scrape.py
(...)
INFO:scrape:Done, 665 articles found
INFO:root:Saving articles to /Users/macbre/git/faroese-resources/frodskaparrit/articles.json ...
INFO:root:Done
```

```yaml
less articles.json
{
    "title": "Eitt sindur um tuberklasmittuna",
    "url": "https://ojs.setur.fo/index.php/frit/article/view/229",
    "pdf": "https://ojs.setur.fo/index.php/frit/article/download/229/293",
    "author": null,
    "abstract": "This paper is part of a treatise dealing with the clinical features of primary tuberculous infection, and the purpose of the present work is to contribute to the clinic of primary tuberculosis. Some literature about the theme is surveyed. The material used has been collected at the Tuberculosis Station of the Faroe Islands at Hoydal during the author's time of service there from 1939 to 1947. An account is given of the working plan of this tuberculosis station, where besides ordinary station work special attention is paid to the tuberculin register. The tuberculin reaction used has been Pirquet 's test. The material comprises a total of 430 cases of initial fever.\nThe fever curve for adults was typically continual, while with children it vas irregular; the duration of the fever was similar for children and adults, generally 2 or 3 weeks; in l/4 of the cases it lasted more than one month. Maximum temperature generally about 39 degrees C might, however, be higher, especially with children. The duration and height of the fever had no prognostic significance. Slow pulse was a constant symptom witli adults, but was seldom noticed with children. This relative bradycardiagenerally lasted till the middle of ihe fever period. Krythema nodosum was a frequent symptom ot' initial fever and occurred 76 times among the 430 cases of initial fever.\nSedimentation rate practically always increased, as a rule moderately, and decreased as the fever fell, but more slowly. X-rays examinations have been made during initial fever in 146 cases. X-rays changes were stated in all the children and in more than % of the adults. The changes stated were chifly enlarged hilar shadows, some had also infiltrations. Rather more than *4 had subjective symptoms, a number which is undoubtedly too low. The most frequent symptoms where retrosternal pain and soreness of the lower end of sternum, a stitch in the side, and pain between the shoulderblades. The mentioned symptoms must be supposed to bi' caused by tlie pathologic anatomic changes.",
    "published": "2022-11-25"
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
