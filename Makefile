
ENV ?= ./venv

install:
	[ ! -d $(ENV)/ ] && virtualenv $(ENV)/ || :
	if [ $(OS) == "Windows_NT" ]; then\
		$(ENV)/Scripts/pip install -r requirements.txt;\
		$(ENV)/Scripts/pip install -r requirements-win.txt;\
	else\
		$(ENV)/bin/pip install -r requirements.txt;\
	fi

run-vanilla: install
	if [ $(OS) == "Windows_NT" ]; then\
		SCRAPY_SETTINGS_MODULE=scrapy.settings.default_settings $(ENV)/Scripts/scrapy.exe runspider src/spiders/charity_charities_org.py -a country=Thailand;\
	else\
		SCRAPY_SETTINGS_MODULE=scrapy.settings.default_settings $(ENV)/bin/scrapy runspider src/spiders/charity_charities_org.py -a country=Thailand;\
	fi

run-proxy: install
	if [ $(OS) == "Windows_NT" ]; then\
		$(ENV)/Scripts/scrapy.exe crawl charity-charities-spider -a country=Thailand;\
	else\
		$(ENV)/bin/scrapy crawl charity-charities-spider -a country=Thailand;\
	fi
