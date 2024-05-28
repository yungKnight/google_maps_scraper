import pytest
import asyncio
from playwright.async_api import async_playwright
import scrapy
from scrapy.http import HtmlResponse


@pytest.mark.asyncio
async def test_map():
	async with async_playwright() as p:
		browser = await p.chromium.launch(headless = False)

		need = 'hotels'
		location = 'Sacramento, CA'

		page = await browser.new_page()

		url = 'https://maps.google.com'
		await page.goto(url, timeout = 60000)

		search_form = await page.wait_for_selector('form#XmI62e')
		if search_form:
			print('search_form is present')
			return True

		await page.fill('input.fontBodyMedium.searchboxinput.xiQny', 'hotels near Denver, Colorado')

