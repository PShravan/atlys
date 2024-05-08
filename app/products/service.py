from typing import List
import json
import os
import requests
import time
import uuid

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fastapi import HTTPException
from fastapi import status as http_status

from products.schema import Product, SearchQuery
from app.redis import redis_get_key, redis_set_key


# https://dentalstall.com/page/2/?s=espe&post_type=product

class ScrapeDentalStall:
    use_async = False
    retries = 3
    retry_delay = 5

    def __init__(self, query: SearchQuery) -> None:
        self.base_url = "https://dentalstall.com/"
        self.query = query

        self.query_params = {}
        self.query_param_str = ""
        if self.query.proxy:
            self.query_param_str = f"?s={self.query.proxy}&post_type=product"
            # self.query_params = {
            #     "s": self.query.proxy,
            #     "post_type": "product",
            # }
        else:
            self.base_url = self.base_url + "shop/"

    def _get_url(self, page_no):
        url = self.base_url
        if page_no > 1:
            url = url + f"page/{page_no}"
        return url + self.query_param_str

    async def get_product_html(self, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()

                if response.status == 200:
                    html = BeautifulSoup(text, "html.parser")

                    return html

        raise HTTPException(
            status_code=http_status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Scraper didn't succeed in getting data:\n"
                  f"\turl: {url}\n"
                  f"\tstatus code: {response.status}\n"
                  f"\tresponse text: {text}"
        )

    async def parse_products(html: BeautifulSoup) -> List[Product]:
        products = []
        ul_element = html.find('ul', class_='products')
        if not ul_element:
            raise Exception("no ul found")

        # Find all <li> elements with the specified class
        product_list = ul_element.find_all('li', class_='un-4-cols')

        # Loop through each product and extract the desired information
        for product in product_list:
            # Extract product name
            name = product.find('h2', class_='woo-loop-product__title').text.strip()

            # Extract product price
            price = product.find('span', class_='price').text.strip()

            # Extract product image URL
            image_url = product.find('img')['data-lazy-src']

            # TODO save image in local storage
            path_to_image = "" or image_url

            product = Product(
                product_title=name,
                product_price=price,
                path_to_image=path_to_image,
            )
            products.append(product)
        return products

    async def async_get_products(self) -> List[Product]:
        products: List[Product] = []
        for page in range(1, self.query.page + 1):
            url = self._get_url(page_no=page)
            entrypoint_page = await self.get_product_html(url)
            print("entrypoint_page: ", entrypoint_page)
            products.extend(self.parse_products(html=entrypoint_page))
        return products

    def request_url(self, url):
        for attempt in range(self.retries):
            try:
                response = requests.get(url)
                # Check if the response status code indicates a server error (5xx)
                if response.status_code >= 500:
                    print(
                        f"Server Error {response.status_code}. Retrying in {self.retry_delay}s."
                    )
                    time.sleep(self.retry_delay)
                    continue
                # request was successful
                return response
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                # retry after delay
                print(f"Retrying in {self.retry_delay}s...")
                time.sleep(self.retry_delay)
        # all retries failed
        raise Exception(f"Failed to fetch page after {self.retries} attempts.")

    def get_price(self, price):
        """
        strings obeserved:
        'Starting at: ₹3550.00'
        '₹9560.00₹10200.00'
        """
        return float(price.split('₹')[1])

    def save_image_from_url(self, url, save_dir):
        random_filename = str(uuid.uuid4())
        file_extension = url.split(".")[-1]
        filename = f"{random_filename}.{file_extension}"
        os.makedirs(save_dir, exist_ok=True)
        # Download the image from the URL
        response = requests.get(url)
        # request was successful
        if response.status_code == 200:
            # Save the image to local storage
            with open(os.path.join(save_dir, filename), "wb") as f:
                f.write(response.content)
            print(f"Image saved as {filename} in {save_dir}")
            return f"{save_dir}{filename}"
        else:
            print(f"Failed to download image from {url}")

    def update_redis(key, value):
        redis_value = redis_get_key(key)
                if redis_value and redis_value["price"] == price:
                    continue
                if redis_value and 

    def sync_get_products(self) -> List[Product]:
        products: List[Product] = []
        for page in range(1, self.query.page + 1):
            url = self._get_url(page_no=page)
            print(page, url)

            response = self.request_url(url=url)

            soup = BeautifulSoup(response.content, 'html.parser')

            ul_element = soup.find('ul', class_='products')

            if not ul_element:
                raise Exception("no ul found")
            # get all <li> elements
            product_list = ul_element.find_all('li', class_='un-4-cols')
            for product in product_list:
                # product name
                name = product.find('h2', class_='woo-loop-product__title').text.strip()

                # product price
                price = product.find('span', class_='price').text.strip()
                price = self.get_price(price)

                # check redis
                redis_value = redis_get_key(name)
                if redis_value and redis_value["price"] == price:
                    continue

                # product image URL
                image_url = product.find('img')['data-lazy-src']

                # TODO save image in local storage
                path_to_image = self.save_image_from_url(image_url, "./images/")

                prodcut_obj = Product(
                    product_title=name,
                    product_price=price,
                    path_to_image=path_to_image,
                  )
                products.append(prodcut_obj)
                # update redis
                redis_set_key(name, prodcut_obj.dict())
        return products

    def save_as_json(self, products: List[Product]):
        products_dicts = [product.dict() for product in products]
        with open("products.json", "w") as product_file:
            json.dump(products_dicts, product_file, indent=4)

    def scrape_and_save(self) -> bool:
        if self.use_async:
            products = self.async_get_products()
        else:
            products = self.sync_get_products()
        print({
            "status": "success",
            "message": f"No. of products scraped: {len(products)}"
        })
        self.save_as_json(products=products)
        return True
