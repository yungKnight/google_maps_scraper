import pytest
import asyncio
from playwright.async_api import async_playwright
import scrapy
from scrapy.http import HtmlResponse

@pytest.mark.asyncio
async def test_map():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        need = 'hospitals'
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

        while has_more_results:
            results = await page.query_selector_all('div.Nv2PK a.hfpxzc')
            new_results_loaded = False

            for result in results:
                await result.click()
                await asyncio.sleep(3)

                html_content = await page.content()
                response = HtmlResponse(url=page.url, body=html_content.encode(), encoding='utf-8')

                detail = response.css('div.m6QErb.WNBkOb.XiKgde div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
                if detail:
                    name = detail.css('h1.DUwDvf::text').get()
                    address = detail.css('div.rogA2c div.Io6YTe::text').get()

                    if name and address:
                        info = {
                            'name': name,
                            'address': address,
                            'phone': detail.css('div.RcCs1.fVHpi.w4B1d.NOE9ve.M0S7ae.AG25L:nth-child(3) button.CsEnBe div.AeaXub div.rogA2c div.Io6YTe::text').get(),
                            'website': detail.css('div.rogA2c.ITvuef div.Io6YTe::text').get()
                        }
                        provider_info.append(info)

            await page.keyboard.press('ArrowDown')
            await asyncio.sleep(3)

            new_results = await page.query_selector_all('div.Nv2PK a.hfpxzc')
            if len(new_results) > len(results):
                new_results_loaded = True
                results = new_results
                load_count += 1
                print(f'Loaded new results {load_count} times')
                print(f'Current number of results: {len(results)}')

            if not new_results_loaded:
                has_more_results = False
                print('No more new results to load')

        await browser.close()

        for info in provider_info:
            print(info)
