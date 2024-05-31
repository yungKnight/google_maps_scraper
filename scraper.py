import pytest
import asyncio
from playwright.async_api import async_playwright
import scrapy
from scrapy.http import HtmlResponse
import time

@pytest.mark.asyncio
async def test_map():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        need = 'hotels'
        location = 'Sacramento, CA'

        page = await browser.new_page()

        url = 'https://maps.google.com'
        await page.goto(url, timeout=60000)

        search_form = await page.wait_for_selector('form#XmI62e')
        
        await page.fill('input#searchboxinput', need + ' near ' + location)
        print('Search inputted already')

        await page.click('button.mL3xi')
        print('search is in progress')

        await page.wait_for_selector('div.Nv2PK.THOPZb.CpccDe')

        await asyncio.sleep(2)
        print('results first batch on screen')

        current_results = await page.query_selector_all('div.Nv2PK.THOPZb.CpccDe a.hfpxzc')
        current_results_count = len(current_results)
        print(current_results_count)

        for result in current_results:
            await result.click()
            await asyncio.sleep(5)

        print('just staying on')
        time.sleep(2)
        print('going off now')

        await browser.close()
