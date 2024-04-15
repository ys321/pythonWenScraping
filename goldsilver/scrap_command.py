import subprocess

# Delete the existing JSON file and then run the Scrapy spider
subprocess.run('del findbull.json && scrapy crawl findbull_spider -o findbull.json && python insert_findData.py', shell=True)



import subprocess

# Delete the existing JSON file and then run the Scrapy spider
subprocess.run('rm jm-new.json && scrapy crawl jmbullion-crawl -o jm-new.json && rm sd-new.json && scrapy crawl sdbullion-crawl -o sd-new.json && python insert_data.py', shell=True)