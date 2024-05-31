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
        
        await page.fill('input#searchboxinput', need + ' in ' + location)
        print('Search inputted already')

        await page.click('button.mL3xi')
        print('search is in progress')

        await page.wait_for_selector('div.Nv2PK') #not adding the additional classes as they are dynamic depending on need
        await asyncio.sleep(2)
        print('results first batch on screen')

        results = await page.query_selector_all('div.Nv2PK a.hfpxzc')
        current_results_count = len(results)
        print(current_results_count)

        total_results = []

        for result in results:
            await result.click()
            await asyncio.sleep(3)
            total_results.append(result)

        await browser.close()