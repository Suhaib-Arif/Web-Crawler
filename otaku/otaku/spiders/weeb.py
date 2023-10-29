import scrapy


class WeebSpider(scrapy.Spider):
    name = "weeb"
    # allowed_domains = ["myanimelist.net"]
    start_urls = [
        "https://myanimelist.net/anime/season",
        'https://myanimelist.net/anime/season/2023/spring',
        'https://myanimelist.net/anime/season/2023/winter',
        'https://myanimelist.net/anime/season/2022/fall'
    ]
    
    def start_requests(self):
        self.logger.info("scrapping")
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)
        

    def parse(self, response):
        self.logger.info("scrraping 2")
        animes = response.css('div.seasonal-anime')

        for anime in animes:
            anime_url = anime.css('div.title a.link-title::attr(href)').get()

            yield scrapy.Request(anime_url, callback=self.anime_scraper)

    def anime_scraper(self, response):
            
        yield {
            "Title": response.css('h1.title-name strong::text').get(),
            "English Title": response.css('p.title-english::text').get(),
            "URL": response.url,
            "Score": response.css('div.score-label::text').get(),
            "Genre": response.css('[href*="/anime/genre/"]::text').getall(),
            "Season": response.css('span.season a::text').get(),
            "Studio": response.css('span.studio a::text').get(),
            "Description": response.xpath('//p[@itemprop="description"]/text()').get(),        
        }
