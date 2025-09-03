# Google Maps Scraper(with Airtable Integration)

A sophisticated web scraper that extracts business information from Google Maps search results and automatically saves or updates records in Airtable. Built with Playwright for reliable web automation and designed to prevent duplicate entries while keeping data fresh.

## 🚀 Features

- **Smart Duplicate Prevention**: Automatically detects existing records and prevents duplicates
- **Intelligent Updates**: Only updates records when actual changes are detected
- **Secure Credential Management**: Uses environment variables for API keys and sensitive data
- **Real-time Progress Tracking**: Clear console output showing scraping progress and database operations
- **Robust Error Handling**: Graceful handling of network issues and API errors
- **Infinite Scroll Support**: Automatically loads more results from Google Maps
- **Comprehensive Data Extraction**: Captures business name, address, phone, and website

## 📋 Prerequisites

- Python 3.7+
- Airtable account with API access

## 🛠️ Installation

### 1. Clone or Download the Project

```bash
# Create a new directory for your project
mkdir maps-scraper
cd maps-scraper

# Save the scraper code as scraper.py
```

### 2. Install Required Dependencies

```bash
pip install pytest playwright scrapy pyairtable python-dotenv
```

### 3. Install Playwright Browsers

```bash
playwright install chromium
```

## ⚙️ Configuration

### 1. Create Environment File

Create a `.env` file in your project root directory:

```bash
# Airtable Configuration
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=your_base_id_here
AIRTABLE_TABLE_NAME=schools
```

### 2. Get Your Airtable Credentials

#### API Key:
1. Go to [Airtable Account Settings](https://airtable.com/account)
2. Navigate to "Developer" section
3. Generate a personal access token
4. Copy the token (starts with `pat...`)

#### Base ID:
1. Open your Airtable base
2. Go to "Help" → "API documentation"
3. Find your Base ID (starts with `app...`)

#### Table Name:
- Use the exact name of your table in Airtable (case-sensitive)

### 3. Set Up Your Airtable Table

Ensure your Airtable table has these columns:
- `name` (Single line text)
- `address` (Long text)
- `phone` (Phone number or Single line text)
- `website` (URL or Single line text)

## 🚦 Usage

### Basic Usage

Run the scraper:

```bash
pytest -s scraper.py
```

### Interactive Prompts

The scraper will prompt you for:

1. **Service Required**: What type of business you're looking for
   - Example: `schools`, `restaurants`, `hospitals`, `gyms`

2. **Location**: Where to search
   - Example: `New York`, `Lagos Nigeria`, `London UK`

### Example Search Queries

```
Service: private schools
Location: Ibadan Nigeria

Service: restaurants
Location: Manhattan New York

Service: dental clinics  
Location: Toronto Canada
```

## 📊 Output and Logging

The scraper provides real-time feedback:

```
✅ Created new record: ABC International School
🔄 Updated existing record: XYZ Academy (phone number changed)
⏭️ No changes for: DEF School - skipping
⚠️ Error processing Some Business: [error details]
```

### Status Messages:
- ✅ **Created new record**: New business added to Airtable
- 🔄 **Updated existing record**: Existing business updated with new information
- ⏭️ **No changes**: Record exists and is up-to-date (skipped)
- ⚠️ **Error**: Something went wrong (with error details)

## 🔧 Advanced Configuration

### Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AIRTABLE_API_KEY` | Your Airtable personal access token | Yes | None |
| `AIRTABLE_BASE_ID` | Your Airtable base ID | Yes | None |
| `AIRTABLE_TABLE_NAME` | Name of your Airtable table | No | "schools" |

### Customizing Browser Behavior

To run in headless mode (no visible browser), modify the scraper:

```python
browser = await p.chromium.launch(headless=True)
```

### Adjusting Delays

Modify sleep times for different connection speeds:

```python
await asyncio.sleep(3)
```

## 🔍 How It Works

### 1. Duplicate Detection Algorithm

```python
def find_existing_record(table, name, address):
    # Searches Airtable for records with matching name
    # Then verifies address matches to ensure same location
    # Returns the record if found, None otherwise
```

### 2. Change Detection

```python
def records_are_different(existing_fields, new_info):
    # Compares all fields (name, address, phone, website)
    # Handles None values and empty strings
    # Returns True if any field has changed
```

### 3. Processing Flow

1. **Search Google Maps** with user query
2. **Extract business details** from each result
3. **Check Airtable** for existing records
4. **Decide action**: Create, Update, or Skip
5. **Execute action** and log result
6. **Continue** to next business

## 🐛 Troubleshooting

### Common Issues

#### 1. "ValueError: AIRTABLE_API_KEY not found"
**Solution**: Check your `.env` file exists and contains the correct variable names.

#### 2. Airtable API errors
**Solution**: 
- Verify your API key is correct
- Check your base ID and table name
- Ensure table columns match expected names

#### 3. No results found
**Solution**: 
- Try different search terms
- Check your internet connection
- Verify Google Maps is accessible

## 📝 Limitations

- **Rate Limiting**: Airtable API has rate limits (5 requests per second)
- **Google Maps Changes**: Scraper may need updates if Google changes their HTML structure
- **Network Dependent**: Requires stable internet connection
- **Browser Required**: Needs Chrome/Chromium installed


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please respect Google's Terms of Service and rate limits when using this scraper.

## ⚠️ Disclaimer

This scraper is for educational and personal use only. Users are responsible for:
- Complying with Google's Terms of Service
- Respecting rate limits and not overloading servers
- Ensuring they have permission to scrape and store business data
- Following applicable data protection laws (GDPR, etc.)

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Verify your configuration matches the examples
3. Test with a simple search query first
4. Check that all dependencies are installed correctly