### Run Spider for Thailand Only

run from root

```
scrapy crawl charity-charities-spider -o charities-thailand.csv -a country=Thailand
```

### Run for all Asia Countries

```
scrapy crawl charity-charities-spider -o charities-singapore.csv -a country=Singapore
scrapy crawl charity-charities-spider -o charities-vietnam.csv -a country=Vietnam
scrapy crawl charity-charities-spider -o charities-malaysia.csv -a country=Malayasia
scrapy crawl charity-charities-spider -o charities-indonesia.csv -a country=Indonesia
scrapy crawl charity-charities-spider -o charities-laos.csv -a country=Laos
scrapy crawl charity-charities-spider -o charities-cambodia.csv -a country=Cambodia
scrapy crawl charity-charities-spider -o charities-myanmar.csv -a country=Myanmar
scrapy crawl charity-charities-spider -o charities-thailand.csv -a country=Thailand

```