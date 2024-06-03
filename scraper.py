import pytest
import asyncio
from playwright.async_api import async_playwright
import scrapy
from scrapy.http import HtmlResponse

@pytest.mark.asyncio
async def test_map():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        need = 'tax advisor'
        location = 'Sacramento, CA'

        page = await browser.new_page()

        url = 'https://maps.google.com'
        await page.goto(url, timeout=60000)

        search_form = await page.wait_for_selector('form#XmI62e')

        await page.fill('input#searchboxinput', f'{need} in {location}')
        print('Search inputted already')

        await page.click('button.mL3xi')
        print('Search is in progress')

        await page.wait_for_selector('div.Nv2PK')
        await asyncio.sleep(2)
        print('Results first batch on screen')

        provider_info = []
        has_more_results = True
        load_count = 0
        processed_results = set()

        while has_more_results:
            results = await page.query_selector_all('div.Nv2PK a.hfpxzc')
            new_results_loaded = False

            for i in range(len(results)):
                result = results[i]
                result_id = await result.get_attribute('href')

                if result_id in processed_results:
                    continue
                
                processed_results.add(result_id)

                await result.click()
                await asyncio.sleep(3)

                html_content = await page.content()
                response = HtmlResponse(url=page.url, body=html_content.encode(), encoding='utf-8')

                detail = response.css('div.m6QErb.WNBkOb.XiKgde div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
                if detail:
                    name = detail.css('h1.DUwDvf::text').get()

                    address = detail.css('div.rogA2c div.Io6YTe::text').get()

                    phone_button = detail.css('button.CsEnBe[data-item-id^="phone:"]')
                    phone = None
                    if phone_button:
                        phone_attr = phone_button.attrib['data-item-id']
                        phone = phone_attr.split(':')[-1]
                        
                    website = detail.css('div.rogA2c.ITvuef div.Io6YTe::text').get()

                    if name and address:
                        info = {
                            'name': name,
                            'address': address,
                            'phone': phone,
                            'website': website
                        }
                        provider_info.append(info)

            await page.keyboard.press('ArrowDown')
            await asyncio.sleep(3)

            new_results = await page.query_selector_all('div.Nv2PK a.hfpxzc')
            if len(new_results) > len(results):
                new_results_loaded = True
                load_count += 1
                print(f'Loaded new results {load_count} times')
                print(f'Current number of results: {len(new_results)}')
            else:
                has_more_results = False
                print('No more new results to load')

        await browser.close()

        for info in provider_info:
            print(info)