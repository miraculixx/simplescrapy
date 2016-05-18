# simplescrapy
simple scrapy test

this tests a scripted mass crawler

## setup

1. Scrapy

```
$ pip install -r requirements.txt
$ cd simple
# should show the test spider if all is ok
$ scrapy list
test
```

2. Local nginx

setup a local nginx using this server directive:

```
    server {
      listen localhost:5151;
       location / {
          return 200 '{ "status" : "success" }';
      }
    }
```

## Test

1. Run a spider test with a direct crawl

```
$ scrapy crawl test
```

should work just fine (no errors)

2. Run a test with say 100 spiders launched 

```
$ scrapy runscript test -n 100
Started 60 crawlers
Started 70 crawlers
Started 80 crawlers
Started 90 crawlers
Started 99 crawlers
Starting actual crawl...
done.
```

3. Run a test with say 1500 spiders launched. This will start to fail, 
see errors below

```
$ scrapy runscript test -n 1500
(...)
2016-05-18 01:55:26 [scrapy] ERROR: Error downloading <GET http://localhost:5151/robots.txt>: DNS lookup failed: address 'localhost' not found: [Errno 11] Resource temporarily unavailable.
DNSLookupError: DNS lookup failed: address 'localhost' not found: [Errno 11] Resource temporarily unavailable.
```


