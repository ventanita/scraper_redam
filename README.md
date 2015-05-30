# Install
```shell
git clone https://github.com/ventanita/scraper_redam.git
cd scraper_redam
pip install -r requirements.txt
```

## Ubuntu instructions
Install dependencies for `cryptography` package:

```shell
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
```
After this just run the above mentioned install.

# Run this way
```shell
cd scraper_redam
scrapy crawl redam -a start_id=1 -a end_id=3000
```
          
