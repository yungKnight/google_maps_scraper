import pytest
import asyncio
import os
from playwright.async_api import async_playwright
import scrapy
from scrapy.http import HtmlResponse
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "schools")

if not API_KEY:
    raise ValueError("AIRTABLE_API_KEY not found in environment variables")
if not BASE_ID:
    raise ValueError("AIRTABLE_BASE_ID not found in environment variables")

def find_existing_record(table, name, address):
    """
    Find existing record by name and address
    Returns the record if found, None otherwise
    """
    try:
        records = table.all(formula=f"{{name}} = '{name}'")
        
        for record in records:
            if record['fields'].get('address') == address:
                return record
        
        return None
    except Exception as e:
        print(f"⚠️ Error searching for existing record: {e}")
        return None

def records_are_different(existing_fields, new_info):
    """
    Compare existing record fields with new scraped info
    Returns True if there are differences, False otherwise
    """
    fields_to_compare = ['name', 'address', 'phone', 'website']
    
    for field in fields_to_compare:
        existing_value = existing_fields.get(field)
        new_value = new_info.get(field)
        
        existing_value = existing_value if existing_value else None
        new_value = new_value if new_value else None
        
        if existing_value != new_value:
            return True
    
    return False

@pytest.mark.asyncio
async def test_map():
    
    api = Api(API_KEY)
    table = api.table(BASE_ID, TABLE_NAME)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        need = input("Enter the service required: ")
        location = input("Enter the location: ")
        page = await browser.new_page()
        url = 'https://maps.google.com'
        await page.goto(url, timeout=60000)
        search_form = await page.wait_for_selector('form#XmI62e')
        await page.fill('input#searchboxinput', f'{need} in {location}')
        print('Search inputted already')
        await page.click('button.mL3xi')
        print('Search is in progress')
        await asyncio.sleep(3)
        await page.wait_for_selector('div.Nv2PK')
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
                            "name": name,
                            "address": address,
                            "phone": phone,
                            "website": website
                        }
                        provider_info.append(info)
                        
                        existing_record = find_existing_record(table, name, address)
                        
                        try:
                            if existing_record:
                                if records_are_different(existing_record['fields'], info):
                                    table.update(existing_record['id'], info)
                                    print(f"🔄 Updated existing record: {name}")
                                else:
                                    print(f"⏭️ No changes for: {name} - skipping")
                            else:
                                table.create(info)
                                print(f"✅ Created new record: {name}")
                        except Exception as e:
                            print(f"⚠️ Error processing {name}: {e}")
                            
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
        print("\n--- Scraped Results ---")
        for info in provider_info:
            print(info)