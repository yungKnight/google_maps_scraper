import pytest
import asyncio
from playwright.async_api import async_playwright
import scrapy
from scrapy.http import HtmlResponse

async def scroll_to_bottom(page):
    previous_height = await page.evaluate('document.body.scrollHeight')
    while True:
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(2)  # Wait for new content to load
        new_height = await page.evaluate('document.body.scrollHeight')
        if new_height == previous_height:
            break
        previous_height = new_height

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

        await browser.close()