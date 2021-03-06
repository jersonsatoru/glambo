import asyncio
import aiohttp
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

discord_webhook = os.environ.get('DISCORD_WEBHOOK')
glambox_baseurl = 'https://apiclient.glambox.com.br'

glambox_username = os.environ.get('GLAMBOX_USERNAME')
glambox_password = os.environ.get('GLAMBOX_PASSWORD')

async def get_token():
    async with aiohttp.ClientSession() as session:
        credentials = {
            "username": glambox_username,
            "password": glambox_password
        }

        headers = {
            'content-type': 'application/json'
        }

        async with session.post(
            f'{glambox_baseurl}/login',
            json=credentials,
            headers=headers,
        ) as response:
            result = await response.json()
            return result


async def get_showcase():
    try:
        token = await get_token()
        bearer = token.get('result').get('Authorization')
        headers = {
            "Authorization": bearer
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            url = f'{glambox_baseurl}/glamclub/list?page=0&pageSize=250&searchKey='
            async with session.get(url) as response:
                result = await response.json()
                return result
    except Exception as err:
        print(err)


async def send_discord(text):
    async with aiohttp.ClientSession() as session:
        await session.post(discord_webhook, json={'content': text})


async def get_changes(products_id):
    try:
        showcase = await get_showcase()
        content = showcase.get('content', [])
        new_products_id = {p.get('productVariantId') for p in content}
        changes = new_products_id ^ products_id
        if changes:
            products_id = new_products_id
            products_data = [product for product in content if product.get(
                'productVariantId') in changes]
            messages = [get_message(product) for product in products_data]
            await send_discord('\n'.join(messages))
        else:
            message = f'TOTAL {len(new_products_id)} - NO CHANGES: {datetime.now()}'
            print(message)
    except Exception as err:
        print(err)
    finally:
        return products_id


def get_message(product):
    return (
        f'PRODUTO: {product.get("productVariantName")} - '
        f'VALOR: {product.get("tradePoints")} - QTD: {product.get("stockCount")}'
    )


async def main():
    # nosso db
    products_id = set()
    while True:
        products_id = await get_changes(products_id)
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
