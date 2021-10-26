import requests
import bs4
import logging
import collections
import csv
logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger('wb')

ParseResult=collections.namedtuple(
    'ParseResult',
    (
        'brand_name',
        'goods_name',
        'url',
    ),

)
Headrs=('Бренд',
        'Товар',
        'Ссылка')

class Client:
    def __init__(self):
        self.session=requests.Session()
        self.session.headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.73 (Edition Yx GX)'
        }


        self.result=[]

    def load_page(self):
        url='https://www.wildberries.ru/catalog/muzhchinam/odezhda/dzhinsy'
        res=self.session.get(url=url)
        res.raise_for_status()
        return res.text


    def parse_page(self,text: str):
        soup = bs4.BeautifulSoup(text,'lxml')
        container = soup.select('div.product-card-list')
        for block in container:
            self.parse_block(block=block)


    def parse_block(self,block):

        url_block=block.select_one('a.product-card__main.j-open-full-product-card')
        if not url_block:
            logger.error('no url_block')
            return

        url=url_block.get('href')
        url='https://www.wildberries.ru'+url
        if not url:
            logger.error('no href')
            return

        name_block=block.select_one('div.product-card__brand-name')
        if not name_block:
            logger.error(f'no name_block on {url}')
            return

        brand_name=name_block.select_one('strong.brand-name')
        if not brand_name:
            logger.error(f'no brand name on {url}')
            return

        brand_name=brand_name.text
        brand_name=brand_name.replace('/', '').strip()

        goods_name = name_block.select_one('span.goods-name')
        if not goods_name:
         logger.error(f'no goods name on {url}')
         return

        goods_name = goods_name.text
        goods_name = goods_name.replace('/', '').strip()





        logger.debug('%s %s' '%s', url, brand_name, goods_name)

        self.result.append(ParseResult(
            url=url,
            brand_name=brand_name,
            goods_name=goods_name

        ))
        logger.debug('-'*100)


    def save_resulds(self):
        path='C:\PycharmProjects\parsers\.venv\Scripts/test.csv'
        with open(path,'w') as f:
            writer =csv.writer(f,quoting=csv.QUOTE_MINIMAL)
            writer.writerow(Headrs)
            for item in self.result:
             writer.writerow(item)



    def run(self):
        text=self.load_page()
        self.parse_page(text=text)
        logger.info(f'получили {len(self.result)} элементов ')
        self.save_resulds()




if __name__=='__main__':
    parser=Client()
    parser.run()








