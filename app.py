import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz
import json
import io
# === CONFIGURATION ===
BOT_TOKEN = '7613703350:AAE-W4dJ37lngM4lO2Tnuns8-a-80jYRtxk'
CHAT_ID = '-1002840229810'
REMARK = "Aayeshatech Astro Trend"
WEBHOOK_URL = "https://tradingview-webhook-0h3k.onrender.com"
# === EXAMPLE DATA (FALLBACK) ===
EXAMPLE_DATA = [
    {
        "Planet": "Su",
        "Date": "2025-08-05",
        "Time": "01:14:15",
        "Motion": "D",
        "Sign Lord": "Mo",
        "Star Lord": "Me",
        "Sub Lord": "Ke",
        "Zodiac": "Cancer",
        "Nakshatra": "Ashlesha",
        "Pada": 1,
        "Pos in Zodiac": "18°33'20\"",
        "Declination": 17.00
    },
    {
        "Planet": "Mo",
        "Date": "2025-08-05",
        "Time": "03:37:39",
        "Motion": "D",
        "Sign Lord": "Ma",
        "Star Lord": "Me",
        "Sub Lord": "Ju",
        "Zodiac": "Scorpio",
        "Nakshatra": "Jyeshtha",
        "Pada": 3,
        "Pos in Zodiac": "26°06'40\"",
        "Declination": -28.24
    },
    {
        "Planet": "Me",
        "Date": "2025-08-05",
        "Time": "06:57:46",
        "Motion": "R",
        "Sign Lord": "Mo",
        "Star Lord": "Sa",
        "Sub Lord": "Mo",
        "Zodiac": "Cancer",
        "Nakshatra": "Pushya",
        "Pada": 3,
        "Pos in Zodiac": "12°06'39\"",
        "Declination": 14.32
    },
    {
        "Planet": "Mo",
        "Date": "2025-08-05",
        "Time": "07:05:56",
        "Motion": "D",
        "Sign Lord": "Ma",
        "Star Lord": "Me",
        "Sub Lord": "Sa",
        "Zodiac": "Scorpio",
        "Nakshatra": "Jyeshtha",
        "Pada": 4,
        "Pos in Zodiac": "27°53'20\"",
        "Declination": -28.36
    },
    {
        "Planet": "Mo",
        "Date": "2025-08-05",
        "Time": "11:12:29",
        "Motion": "D",
        "Sign Lord": "Ju",
        "Star Lord": "Ke",
        "Sub Lord": "Ke",
        "Zodiac": "Saggitarius",
        "Nakshatra": "Mula",
        "Pada": 1,
        "Pos in Zodiac": "00°00'00\"",
        "Declination": -28.46
    },
    {
        "Planet": "Mo",
        "Date": "2025-08-05",
        "Time": "12:43:07",
        "Motion": "D",
        "Sign Lord": "Ju",
        "Star Lord": "Ke",
        "Sub Lord": "Ve",
        "Zodiac": "Saggitarius",
        "Nakshatra": "Mula",
        "Pada": 1,
        "Pos in Zodiac": "00°46'40\"",
        "Declination": -28.49
    },
    {
        "Planet": "Mo",
        "Date": "2025-08-05",
        "Time": "17:01:25",
        "Motion": "D",
        "Sign Lord": "Ju",
        "Star Lord": "Ke",
        "Sub Lord": "Su",
        "Zodiac": "Saggitarius",
        "Nakshatra": "Mula",
        "Pada": 1,
        "Pos in Zodiac": "03°00'00\"",
        "Declination": -28.53
    },
    {
        "Planet": "Mo",
        "Date": "2025-08-05",
        "Time": "18:18:43",
        "Motion": "D",
        "Sign Lord": "Ju",
        "Star Lord": "Ke",
        "Sub Lord": "Mo",
        "Zodiac": "Saggitarius",
        "Nakshatra": "Mula",
        "Pada": 2,
        "Pos in Zodiac": "03°40'00\"",
        "Declination": -28.53
    },
    {
        "Planet": "Mo",
        "Date": "2025-08-05",
        "Time": "20:27:22",
        "Motion": "D",
        "Sign Lord": "Ju",
        "Star Lord": "Ke",
        "Sub Lord": "Ma",
        "Zodiac": "Saggitarius",
        "Nakshatra": "Mula",
        "Pada": 2,
        "Pos in Zodiac": "04°46'40\"",
        "Declination": -28.53
    },
    {
        "Planet": "Su",
        "Date": "2025-08-05",
        "Time": "20:44:01",
        "Motion": "D",
        "Sign Lord": "Mo",
        "Star Lord": "Me",
        "Sub Lord": "Ve",
        "Zodiac": "Cancer",
        "Nakshatra": "Ashlesha",
        "Pada": 1,
        "Pos in Zodiac": "19°20'00\"",
        "Declination": 16.78
    },
    {
        "Planet": "Mo",
        "Date": "2025-08-05",
        "Time": "21:57:16",
        "Motion": "D",
        "Sign Lord": "Ju",
        "Star Lord": "Ke",
        "Sub Lord": "Ra",
        "Zodiac": "Saggitarius",
        "Nakshatra": "Mula",
        "Pada": 2,
        "Pos in Zodiac": "05°33'20\"",
        "Declination": -28.52
    },
    {
        "Planet": "Ma",
        "Date": "2025-08-05",
        "Time": "23:24:29",
        "Motion": "D",
        "Sign Lord": "Me",
        "Star Lord": "Su",
        "Sub Lord": "Me",
        "Zodiac": "Virgo",
        "Nakshatra": "Uttaraphalguni",
        "Pada": 3,
        "Pos in Zodiac": "05°06'40\"",
        "Declination": 0.82
    }
]
# === DATA FETCHING ===
@st.cache_data(ttl=3600)
def fetch_almanac_data(date):
    try:
        # Use the direct Google Apps Script URL
        base_url = "https://script.google.com/macros/s/AKfycbydjof_o_vUV1AUU7m9_14egn07wYEyE4fow-nWoHncZrug2ySkrpeCUFOxlcacCtcFhg/exec"
        url = f"{base_url}?date={date}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        # Debug information
        with st.expander("Debug Information"):
            st.write(f"**URL:** {url}")
            st.write(f"**Status Code:** {response.status_code}")
            st.write(f"**Response Headers:** {response.headers}")
            st.write(f"**Response (first 500 chars):** {response.text[:500]}")
        
        # Check if response is empty
        if not response.text.strip():
            raise ValueError("Empty response from API")
        
        # Try to parse JSON
        try:
            data = json.loads(response.text)
            return data
        except json.JSONDecodeError as e:
            st.error(f"JSON Decode Error: {str(e)}")
            with st.expander("Raw Response"):
                st.text(response.text)
            raise
            
    except Exception as e:
        st.error(f"Data fetch failed: {str(e)}")
        
        # Fallback to example data if available
        if date == "2025-08-05":
            st.warning("Using example data for 2025-08-05")
            return EXAMPLE_DATA
        return None
# === SENTIMENT ANALYSIS ===
def analyze_sentiment(data):
    if not data:
        return [], pd.DataFrame(), {}, {}
        
    df = pd.DataFrame(data)
    df['Time'] = pd.to_datetime(df['Time']).dt.time
    
    # Filter market hours (9:15 AM - 3:30 PM IST)
    start = pd.to_datetime("09:15:00").time()
    end = pd.to_datetime("15:30:00").time()
    market_data = df[df['Time'].between(start, end)]
    
    # Identify key events
    moon_events = market_data[market_data['Planet'] == 'Mo'].sort_values('Time')
    retrogrades = market_data[market_data['Motion'] == 'R']
    
    # Create sentiment segments
    segments = []
    prev_time = start
    
    for _, event in moon_events.iterrows():
        segment = {
            'start': prev_time,
            'end': event['Time'],
            'sign_lord': event['Sign Lord'],
            'star_lord': event['Star Lord'],
            'sub_lord': event['Sub Lord'],
            'zodiac': event['Zodiac']
        }
        segments.append(segment)
        prev_time = event['Time']
    
    # Add final segment
    if moon_events.empty:
        segments.append({
            'start': start,
            'end': end,
            'sign_lord': 'Unknown',
            'star_lord': 'Unknown',
            'sub_lord': 'Unknown',
            'zodiac': 'Unknown'
        })
    else:
        segments.append({
            'start': prev_time,
            'end': end,
            'sign_lord': moon_events.iloc[-1]['Sign Lord'],
            'star_lord': moon_events.iloc[-1]['Star Lord'],
            'sub_lord': moon_events.iloc[-1]['Sub Lord'],
            'zodiac': moon_events.iloc[-1]['Zodiac']
        })
    
    # Analyze assets
    assets = {
        'GOLD': 'Neutral',
        'BTC': 'Neutral',
        'DOWJONES': 'Neutral',
        'CRUDE': 'Neutral',
        'SILVER': 'Neutral'
    }
    
    # Analyze indices
    indices = {
        'NIFTY': 'Neutral',
        'BANKNIFTY': 'Neutral'
    }
    
    # Simple asset analysis based on planetary positions
    for _, row in market_data.iterrows():
        planet = row['Planet']
        zodiac = row['Zodiac']
        motion = row['Motion']
        sign_lord = row['Sign Lord']
        star_lord = row['Star Lord']
        sub_lord = row['Sub Lord']
        
        # GOLD: Bullish with Venus in Taurus or Cancer, Bearish with Saturn in Scorpio
        if planet == 'Ve' and zodiac in ['Taurus', 'Cancer']:
            assets['GOLD'] = 'Bullish'
        elif planet == 'Sa' and zodiac == 'Scorpio':
            assets['GOLD'] = 'Bearish'
        
        # BTC: Bullish with Mercury in Gemini or Aquarius, Bearish with Saturn in aspect
        if planet == 'Me' and zodiac in ['Gemini', 'Aquarius']:
            assets['BTC'] = 'Bullish'
        elif planet == 'Sa' and motion == 'R':
            assets['BTC'] = 'Bearish'
        
        # DOWJONES: Bullish with Jupiter in Pisces or Cancer, Bearish with Mars in Capricorn
        if planet == 'Ju' and zodiac in ['Pisces', 'Cancer']:
            assets['DOWJONES'] = 'Bullish'
        elif planet == 'Ma' and zodiac == 'Capricorn':
            assets['DOWJONES'] = 'Bearish'
        
        # CRUDE: Bullish with Mars in Aries or Scorpio, Bearish with Saturn in Taurus
        if planet == 'Ma' and zodiac in ['Aries', 'Scorpio']:
            assets['CRUDE'] = 'Bullish'
        elif planet == 'Sa' and zodiac == 'Taurus':
            assets['CRUDE'] = 'Bearish'
        
        # SILVER: Bullish with Moon in Cancer or Venus in Libra, Bearish with Saturn in Cancer
        if (planet == 'Mo' and zodiac == 'Cancer') or (planet == 'Ve' and zodiac == 'Libra'):
            assets['SILVER'] = 'Bullish'
        elif planet == 'Sa' and zodiac == 'Cancer':
            assets['SILVER'] = 'Bearish'
        
        # NIFTY: Bullish with Jupiter or Venus strong, Bearish with Saturn or Mars strong
        if sign_lord in ['Ju', 'Ve'] or star_lord in ['Ju', 'Ve'] or sub_lord in ['Ju', 'Ve']:
            indices['NIFTY'] = 'Bullish'
        elif sign_lord in ['Sa', 'Ma'] or star_lord in ['Sa', 'Ma'] or sub_lord in ['Sa', 'Ma']:
            indices['NIFTY'] = 'Bearish'
        
        # BANKNIFTY: Bullish with Jupiter or Venus, Bearish with Saturn or Mars
        if sign_lord in ['Ju', 'Ve'] or star_lord in ['Ju', 'Ve'] or sub_lord in ['Ju', 'Ve']:
            indices['BANKNIFTY'] = 'Bullish'
        elif sign_lord in ['Sa', 'Ma'] or star_lord in ['Sa', 'Ma'] or sub_lord in ['Sa', 'Ma']:
            indices['BANKNIFTY'] = 'Bearish'
    
    return segments, retrogrades, assets, indices
# === SECTOR MAPPING ===
def map_sectors(segments):
    sector_map = {
        'Banking': ['Ju', 'Ve'],
        'IT': ['Me'],
        'Pharma': ['Ke'],
        'Energy': ['Ma', 'Sa'],
        'Auto': ['Ve'],
        'Real Estate': ['Ma', 'Sa'],
        'Consumer': ['Ve'],
        'Metals': ['Ma', 'Sa']
    }
    
    bullish_sectors = {}
    bearish_sectors = {}
    
    for seg in segments:
        for sector, planets in sector_map.items():
            if any(p in [seg['sign_lord'], seg['star_lord'], seg['sub_lord']] for p in planets):
                if seg['sub_lord'] in ['Ve', 'Ju']:
                    bullish_sectors[sector] = bullish_sectors.get(sector, 0) + 1
                elif seg['sub_lord'] in ['Sa', 'Ma', 'Ke']:
                    bearish_sectors[sector] = bearish_sectors.get(sector, 0) + 1
    
    return bullish_sectors, bearish_sectors
# === INTRADAY TIMING FUNCTIONS ===
def get_asset_intraday_timing(data, asset, start_time="05:00", end_time="23:55"):
    """Generate intraday timing for assets (5AM to 11:55PM)"""
    if not data:
        return []
    
    df = pd.DataFrame(data)
    df['Time'] = pd.to_datetime(df['Time']).dt.time
    
    # Filter for the time range
    start = pd.to_datetime(start_time).time()
    end = pd.to_datetime(end_time).time()
    asset_data = df[df['Time'].between(start, end)]
    
    # Sort by time
    asset_data = asset_data.sort_values('Time')
    
    # Create segments
    segments = []
    prev_time = start
    
    for _, row in asset_data.iterrows():
        segments.append({
            'start': prev_time.strftime('%H:%M'),
            'end': row['Time'].strftime('%H:%M'),
            'sentiment': get_asset_sentiment(row, asset),
            'trigger': f"{row['Planet']} in {row['Zodiac']}"
        })
        prev_time = row['Time']
    
    # Add final segment
    if asset_data.empty:
        segments.append({
            'start': start.strftime('%H:%M'),
            'end': end.strftime('%H:%M'),
            'sentiment': 'Neutral',
            'trigger': 'No events'
        })
    else:
        segments.append({
            'start': prev_time.strftime('%H:%M'),
            'end': end.strftime('%H:%M'),
            'sentiment': get_asset_sentiment(asset_data.iloc[-1], asset),
            'trigger': f"{asset_data.iloc[-1]['Planet']} in {asset_data.iloc[-1]['Zodiac']}"
        })
    
    return segments

def get_index_intraday_timing(data, index, start_time="09:15", end_time="15:30"):
    """Generate intraday timing for indices (9:15AM to 3:30PM)"""
    if not data:
        return []
    
    df = pd.DataFrame(data)
    df['Time'] = pd.to_datetime(df['Time']).dt.time
    
    # Filter for market hours
    start = pd.to_datetime(start_time).time()
    end = pd.to_datetime(end_time).time()
    market_data = df[df['Time'].between(start, end)]
    
    # Get moon events for segmentation
    moon_events = market_data[market_data['Planet'] == 'Mo'].sort_values('Time')
    
    # Create segments
    segments = []
    prev_time = start
    
    for _, event in moon_events.iterrows():
        segments.append({
            'start': prev_time.strftime('%H:%M'),
            'end': event['Time'].strftime('%H:%M'),
            'sentiment': get_index_sentiment(event, index),
            'trigger': f"Moon in {event['Zodiac']}"
        })
        prev_time = event['Time']
    
    # Add final segment
    if moon_events.empty:
        segments.append({
            'start': start.strftime('%H:%M'),
            'end': end.strftime('%H:%M'),
            'sentiment': 'Neutral',
            'trigger': 'No Moon events'
        })
    else:
        segments.append({
            'start': prev_time.strftime('%H:%M'),
            'end': end.strftime('%H:%M'),
            'sentiment': get_index_sentiment(moon_events.iloc[-1], index),
            'trigger': f"Moon in {moon_events.iloc[-1]['Zodiac']}"
        })
    
    return segments

def get_asset_sentiment(row, asset):
    """Determine sentiment for an asset based on planetary position"""
    planet = row['Planet']
    zodiac = row['Zodiac']
    motion = row['Motion']
    sign_lord = row['Sign Lord']
    star_lord = row['Star Lord']
    sub_lord = row['Sub Lord']
    
    if asset == 'GOLD':
        if planet == 'Ve' and zodiac in ['Taurus', 'Cancer', 'Pisces']:
            return 'Bullish'
        elif planet == 'Sa' and zodiac in ['Scorpio', 'Taurus']:
            return 'Bearish'
        elif sign_lord == 'Ve' or star_lord == 'Ve' or sub_lord == 'Ve':
            return 'Bullish'
        elif sign_lord == 'Sa' or star_lord == 'Sa' or sub_lord == 'Sa':
            return 'Bearish'
    
    elif asset == 'SILVER':
        if planet == 'Ve' and zodiac in ['Taurus', 'Libra', 'Cancer']:
            return 'Bullish'
        elif planet == 'Sa' and zodiac in ['Cancer', 'Taurus']:
            return 'Bearish'
        elif sign_lord == 'Ve' or star_lord == 'Ve' or sub_lord == 'Ve':
            return 'Bullish'
        elif sign_lord == 'Sa' or star_lord == 'Sa' or sub_lord == 'Sa':
            return 'Bearish'
    
    elif asset == 'BTC':
        if planet == 'Me' and zodiac in ['Gemini', 'Aquarius', 'Virgo']:
            return 'Bullish'
        elif planet == 'Sa' and motion == 'R':
            return 'Bearish'
        elif sign_lord == 'Me' or star_lord == 'Me' or sub_lord == 'Me':
            return 'Bullish'
        elif sign_lord == 'Sa' or star_lord == 'Sa' or sub_lord == 'Sa':
            return 'Bearish'
    
    elif asset == 'DOWJONES':
        if planet == 'Ju' and zodiac in ['Pisces', 'Cancer', 'Sagittarius']:
            return 'Bullish'
        elif planet == 'Ma' and zodiac in ['Capricorn', 'Aries']:
            return 'Bearish'
        elif sign_lord == 'Ju' or star_lord == 'Ju' or sub_lord == 'Ju':
            return 'Bullish'
        elif sign_lord == 'Ma' or star_lord == 'Ma' or sub_lord == 'Ma':
            return 'Bearish'
    
    elif asset == 'CRUDE':
        if planet == 'Ma' and zodiac in ['Aries', 'Scorpio']:
            return 'Bullish'
        elif planet == 'Sa' and zodiac == 'Taurus':
            return 'Bearish'
        elif sign_lord == 'Ma' or star_lord == 'Ma' or sub_lord == 'Ma':
            return 'Bullish'
        elif sign_lord == 'Sa' or star_lord == 'Sa' or sub_lord == 'Sa':
            return 'Bearish'
    
    return 'Neutral'

def get_index_sentiment(row, index):
    """Determine sentiment for an index based on planetary position"""
    sign_lord = row['Sign Lord']
    star_lord = row['Star Lord']
    sub_lord = row['Sub Lord']
    
    if index in ['NIFTY', 'BANKNIFTY']:
        if sign_lord in ['Ju', 'Ve'] or star_lord in ['Ju', 'Ve'] or sub_lord in ['Ju', 'Ve']:
            return 'Bullish'
        elif sign_lord in ['Sa', 'Ma'] or star_lord in ['Sa', 'Ma'] or sub_lord in ['Sa', 'Ma']:
            return 'Bearish'
    
    return 'Neutral'

def generate_asset_report(data, date):
    """Generate asset report in table format"""
    assets = ['GOLD', 'BTC', 'SILVER', 'CRUDE', 'DOWJONES']
    report_data = []
    
    for asset in assets:
        timing = get_asset_intraday_timing(data, asset)
        for segment in timing:
            # Determine action based on sentiment
            if segment['sentiment'] == 'Bullish':
                action = 'Go Long'
            elif segment['sentiment'] == 'Bearish':
                action = 'Go Short'
            else:
                action = 'Hold'
            
            report_data.append({
                'Date': date,
                'Segment': asset,
                'Bullish/Bearish': segment['sentiment'],
                'Time Period': f"{segment['start']} - {segment['end']}",
                'Remark': segment['trigger'],
                'Go Long/Short': action
            })
    
    return pd.DataFrame(report_data)

def generate_index_sector_report(segments, indices, bullish_sectors, bearish_sectors, retrogrades):
    """Generate index and sector report in the existing format"""
    # Get the first timeline segment for market sentiment
    if segments:
        sentiment = "🐂 Bullish" if segments[0]['sub_lord'] in ['Ve', 'Ju'] else "🐻 Bearish"
        time_period = f"{segments[0]['start'].strftime('%H:%M')} - {segments[0]['end'].strftime('%H:%M')}"
    else:
        sentiment = "➖ Neutral"
        time_period = "N/A"
    
    # Get top bullish and bearish sectors
    top_bullish = ', '.join(list(bullish_sectors.keys())[:2]) if bullish_sectors else 'None'
    top_bearish = ', '.join(list(bearish_sectors.keys())[:2]) if bearish_sectors else 'None'
    
    # Create report
    report = f"""
        <b>{REMARK}</b>
        <b>Date:</b> {date_str}
        
        <b>Market Sentiment:</b>
        {sentiment} ({time_period})
        
        <b>Top Bullish:</b> {top_bullish}
        <b>Top Bearish:</b> {top_bearish}
        
        <b>Asset Sentiment:</b>
        """
    
    for asset, sentiment in assets.items():
        emoji = "🐂" if sentiment == "Bullish" else "🐻" if sentiment == "Bearish" else "➖"
        report += f"\n<b>{asset}:</b> {emoji} {sentiment}"
    
    report += f"\n\n<b>Index Sentiment:</b>"
    for index, sentiment in indices.items():
        emoji = "🐂" if sentiment == "Bullish" else "🐻" if sentiment == "Bearish" else "➖"
        report += f"\n<b>{index}:</b> {emoji} {sentiment}"
    
    report += f"\n\n<b>Key Events:</b> {f"{len(retrogrades)} retrogrades" if not retrogrades.empty else "None"}"
    
    return report
# === TELEGRAM NOTIFICATION ===
def send_telegram_notification(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': f"{REMARK}\n\n{message}",
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            st.error(f"Telegram notification failed: {response.text}")
    except Exception as e:
        st.error(f"Telegram notification failed: {str(e)}")
# === STREAMLIT DASHBOARD ===
st.set_page_config(page_title="Astro Market Dashboard", layout="wide")
st.title("🌌 Daily Astro Market Dashboard")
# Date selector with validation
col1, col2 = st.columns([2, 1])
with col1:
    selected_date = st.date_input(
        "Select Date",
        datetime.now(pytz.timezone('Asia/Kolkata')).date(),
        min_value=datetime.now(pytz.timezone('Asia/Kolkata')).date() - timedelta(days=30),
        max_value=datetime.now(pytz.timezone('Asia/Kolkata')).date() + timedelta(days=30)
    )
with col2:
    notify = st.checkbox("Send Telegram Notification")
# Format date for API
date_str = selected_date.strftime("%Y-%m-%d")
# Display selected date
st.markdown(f"### Selected Date: {selected_date.strftime('%d %B %Y')}")
# Manual data upload option
with st.expander("Daily Data Upload"):
    st.write("Upload a CSV, JSON, or TXT file with planetary data:")
    
    # File upload option
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "json", "txt"])
    
    if uploaded_file is not None:
        try:
            # Process CSV file
            if uploaded_file.name.endswith('.csv'):
                # Read CSV file
                string_data = uploaded_file.read().decode("utf-8")
                
                # Show raw data for debugging
                with st.expander("Raw CSV Data"):
                    st.text(string_data[:1000])
                
                # Try reading with different parameters
                try:
                    # First try with default settings
                    df = pd.read_csv(io.StringIO(string_data))
                except:
                    try:
                        # Try with different separator
                        df = pd.read_csv(io.StringIO(string_data), sep=';')
                    except:
                        try:
                            # Try with tab separator
                            df = pd.read_csv(io.StringIO(string_data), sep='\t')
                        except Exception as e:
                            st.error(f"Error reading CSV: {str(e)}")
                            st.info("Please make sure your CSV file has the correct format.")
                            data = None
                            raise
                
                # Check if required columns exist
                required_columns = ['Planet', 'Date', 'Time', 'Motion', 'Sign Lord', 'Star Lord', 
                                  'Sub Lord', 'Zodiac', 'Nakshatra', 'Pada', 'Pos in Zodiac', 'Declination']
                
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    st.error(f"Missing required columns: {', '.join(missing_columns)}")
                    st.info("Please make sure your CSV file has all required columns.")
                    data = None
                else:
                    # Convert DataFrame to list of dictionaries
                    manual_data = df.to_dict('records')
                    st.success("CSV data uploaded successfully!")
                    data = manual_data
                    
                    # Show preview of uploaded data
                    st.subheader("Uploaded Data Preview")
                    st.dataframe(df)
            
            # Process JSON file
            elif uploaded_file.name.endswith('.json'):
                # Read JSON file
                string_data = uploaded_file.read().decode("utf-8")
                
                # Show raw data for debugging
                with st.expander("Raw JSON Data"):
                    st.text(string_data[:1000])
                
                try:
                    manual_data = json.loads(string_data)
                    st.success("JSON data uploaded successfully!")
                    data = manual_data
                    
                    # Show preview of uploaded data
                    st.subheader("Uploaded Data Preview")
                    st.dataframe(pd.DataFrame(manual_data))
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON format: {str(e)}")
                    data = None
            
            # Process TXT file (tab-separated)
            elif uploaded_file.name.endswith('.txt'):
                # Read TXT file
                string_data = uploaded_file.read().decode("utf-8")
                
                # Show raw data for debugging
                with st.expander("Raw TXT Data"):
                    st.text(string_data[:1000])
                
                try:
                    # Try reading as tab-separated data
                    df = pd.read_csv(io.StringIO(string_data), sep='\t')
                    
                    # Check if required columns exist
                    required_columns = ['Planet', 'Date', 'Time', 'Motion', 'Sign Lord', 'Star Lord', 
                                      'Sub Lord', 'Zodiac', 'Nakshatra', 'Pada', 'Pos in Zodiac', 'Declination']
                    
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    if missing_columns:
                        st.error(f"Missing required columns: {', '.join(missing_columns)}")
                        st.info("Please make sure your TXT file has all required columns in tab-separated format.")
                        data = None
                    else:
                        # Convert DataFrame to list of dictionaries
                        manual_data = df.to_dict('records')
                        st.success("TXT data uploaded successfully!")
                        data = manual_data
                        
                        # Show preview of uploaded data
                        st.subheader("Uploaded Data Preview")
                        st.dataframe(df)
                        
                except Exception as e:
                    st.error(f"Error reading TXT file: {str(e)}")
                    st.info("Please make sure your TXT file is tab-separated with the correct columns.")
                    data = None
                    
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")
            data = None
    else:
        data = None
# Fetch and process data if no manual upload
if uploaded_file is None:
    with st.spinner("Fetching astronomical data..."):
        data = fetch_almanac_data(date_str)
if data:
    segments, retrogrades, assets, indices = analyze_sentiment(data)
    bullish_sectors, bearish_sectors = map_sectors(segments)
    
    # Market Sentiment Timeline
    st.subheader("📊 Market Sentiment Timeline")
    timeline_data = []
    for seg in segments:
        sentiment = "🐂 Bullish" if seg['sub_lord'] in ['Ve', 'Ju'] else "🐻 Bearish"
        timeline_data.append({
            "Time Period": f"{seg['start'].strftime('%H:%M')} - {seg['end'].strftime('%H:%M')}",
            "Sentiment": sentiment,
            "Sign Lord": seg['sign_lord'],
            "Star Lord": seg['star_lord'],
            "Sub Lord": seg['sub_lord'],
            "Zodiac": seg['zodiac']
        })
    
    st.dataframe(pd.DataFrame(timeline_data), use_container_width=True)
    
    # Asset Intraday Timing (5AM to 11:55PM)
    st.subheader("🌐 Asset Intraday Timing (5AM - 11:55PM)")
    
    # Create tabs for each asset
    asset_tabs = st.tabs(["GOLD", "SILVER", "BTC", "DOWJONES", "CRUDE"])
    
    assets_list = ["GOLD", "SILVER", "BTC", "DOWJONES", "CRUDE"]
    
    for i, asset in enumerate(assets_list):
        with asset_tabs[i]:
            asset_timing = get_asset_intraday_timing(data, asset)
            
            if asset_timing:
                # Create a DataFrame for better display
                timing_df = pd.DataFrame(asset_timing)
                
                # Add sentiment emoji
                timing_df['Sentiment'] = timing_df['sentiment'].apply(
                    lambda x: "🐂 Bullish" if x == "Bullish" else "🐻 Bearish" if x == "Bearish" else "➖ Neutral"
                )
                
                # Display the timing table
                st.dataframe(timing_df[['start', 'end', 'Sentiment', 'trigger']], 
                            use_container_width=True,
                            column_config={
                                "start": "Start Time",
                                "end": "End Time",
                                "Sentiment": "Sentiment",
                                "trigger": "Planetary Trigger"
                            })
            else:
                st.info(f"No timing data available for {asset}")
    
    # Index Intraday Timing (9:15AM to 3:30PM)
    st.subheader("📈 Index Intraday Timing (9:15AM - 3:30PM)")
    
    # Create tabs for each index
    index_tabs = st.tabs(["NIFTY", "BANKNIFTY"])
    
    indices_list = ["NIFTY", "BANKNIFTY"]
    
    for i, index in enumerate(indices_list):
        with index_tabs[i]:
            index_timing = get_index_intraday_timing(data, index)
            
            if index_timing:
                # Create a DataFrame for better display
                timing_df = pd.DataFrame(index_timing)
                
                # Add sentiment emoji
                timing_df['Sentiment'] = timing_df['sentiment'].apply(
                    lambda x: "🐂 Bullish" if x == "Bullish" else "🐻 Bearish" if x == "Bearish" else "➖ Neutral"
                )
                
                # Display the timing table
                st.dataframe(timing_df[['start', 'end', 'Sentiment', 'trigger']], 
                            use_container_width=True,
                            column_config={
                                "start": "Start Time",
                                "end": "End Time",
                                "Sentiment": "Sentiment",
                                "trigger": "Planetary Trigger"
                            })
            else:
                st.info(f"No timing data available for {index}")
    
    # Sectoral Outlook
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 Bullish Sectors")
        if bullish_sectors:
            st.dataframe(pd.DataFrame({
                "Sector": list(bullish_sectors.keys()),
                "Strength": ["✅" * min(v, 3) for v in bullish_sectors.values()]
            }), use_container_width=True)
        else:
            st.info("No bullish sectors identified")
    
    with col2:
        st.subheader("🔴 Bearish Sectors")
        if bearish_sectors:
            st.dataframe(pd.DataFrame({
                "Sector": list(bearish_sectors.keys()),
                "Strength": ["⚠️" * min(v, 3) for v in bearish_sectors.values()]
            }), use_container_width=True)
        else:
            st.info("No bearish sectors identified")
    
    # Key Planetary Triggers
    st.subheader("🌟 Key Planetary Triggers")
    if not retrogrades.empty:
        st.dataframe(
            retrogrades[['Planet', 'Time', 'Zodiac', 'Nakshatra', 'Motion']].rename(columns={
                'Planet': 'Planet',
                'Time': 'Time (IST)',
                'Zodiac': 'Zodiac',
                'Nakshatra': 'Nakshatra',
                'Motion': 'Motion'
            }),
            use_container_width=True
        )
    else:
        st.info("No retrogrades during market hours")
    
    # Trading Strategy
    st.subheader("📈 Trading Strategy")
    strategy = []
    if bearish_sectors:
        strategy.append(f"🔴 Short: {', '.join(list(bearish_sectors.keys())[:2])}")
    if bullish_sectors:
        strategy.append(f"🟢 Long: {', '.join(list(bullish_sectors.keys())[:2])}")
    
    # Add asset recommendations
    bullish_assets = [asset for asset, sentiment in assets.items() if sentiment == 'Bullish']
    bearish_assets = [asset for asset, sentiment in assets.items() if sentiment == 'Bearish']
    
    if bullish_assets:
        strategy.append(f"🟢 Buy: {', '.join(bullish_assets)}")
    if bearish_assets:
        strategy.append(f"🔴 Sell: {', '.join(bearish_assets)}")
    
    if strategy:
        st.markdown(" - " + "\n - ".join(strategy))
    else:
        st.info("Neutral market expected")
    
    # Telegram Notification
    if notify and st.button("Send Report to Telegram"):
        # Generate asset report
        asset_report_df = generate_asset_report(data, selected_date.strftime('%Y-%m-%d'))
        
        # Convert asset report to string for Telegram
        asset_report_str = "<b>ASSET REPORT</b>\n"
        asset_report_str += "<pre>"
        asset_report_str += asset_report_df.to_string(index=False)
        asset_report_str += "</pre>"
        
        # Generate index and sector report
        index_sector_report = generate_index_sector_report(segments, indices, bullish_sectors, bearish_sectors, retrogrades)
        
        # Combine both reports
        combined_message = asset_report_str + "\n\n" + index_sector_report
        
        # Send to Telegram
        send_telegram_notification(combined_message)
        st.success("Reports sent to Telegram!")
    
    # Tomorrow's Preview
    st.subheader("🔮 Tomorrow's Preview")
    tomorrow = selected_date + timedelta(days=1)
    tomorrow_data = fetch_almanac_data(tomorrow.strftime("%Y-%m-%d"))
    
    if tomorrow_data:
        tomorrow_df = pd.DataFrame(tomorrow_data)
        moon_tomorrow = tomorrow_df[tomorrow_df['Planet'] == 'Mo']
        
        if not moon_tomorrow.empty:
            first_event = moon_tomorrow.iloc[0]
            st.markdown(f"""
            - **Date:** {tomorrow.strftime('%d %b %Y')}
            - **First Moon Event:** {first_event['Time']} ({first_event['Zodiac']})
            - **Key Influence:** {first_event['Sign Lord']} + {first_event['Sub Lord']}
            """)
        else:
            st.info("No Moon events tomorrow")
    else:
        st.warning("Tomorrow's data unavailable")
else:
    st.error("Failed to load data. Please try another date or upload data manually.")
    
    # Show example data if available
    if date_str == "2025-08-05":
        st.info("Showing example data for 2025-08-05")
        st.dataframe(pd.DataFrame(EXAMPLE_DATA), use_container_width=True)
    
    # Provide example data download
    st.subheader("Download Example Data")
    
    # CSV format
    example_df = pd.DataFrame(EXAMPLE_DATA)
    csv = example_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Example CSV",
        data=csv,
        file_name="example_astro_data.csv",
        mime="text/csv"
    )
    
    # JSON format
    example_json = json.dumps(EXAMPLE_DATA, indent=2)
    st.download_button(
        label="Download Example JSON",
        data=example_json,
        file_name="example_astro_data.json",
        mime="application/json"
    )
    
    # TXT format (tab-separated)
    txt_data = example_df.to_csv(sep='\t', index=False).encode('utf-8')
    st.download_button(
        label="Download Example TXT",
        data=txt_data,
        file_name="example_astro_data.txt",
        mime="text/plain"
    )
    
    # Instructions for TXT format
    st.subheader("TXT Format Instructions")
    st.markdown("""
    Your TXT file should be tab-separated with these columns in this exact order:
    
    1. Planet (Su, Mo, Me, Ma, Ju, Ve, Sa, Ra, Ke)
    2. Date (YYYY-MM-DD)
    3. Time (HH:MM:SS)
    4. Motion (D for Direct, R for Retrograde)
    5. Sign Lord (Mo, Ma, Me, Ju, Ve, Sa)
    6. Star Lord (Mo, Ma, Me, Ju, Ve, Sa)
    7. Sub Lord (Mo, Ma, Me, Ju, Ve, Sa)
    8. Zodiac (Aries, Taurus, etc.)
    9. Nakshatra (Ashwini, Bharani, etc.)
    10. Pada (1, 2, 3, or 4)
    11. Pos in Zodiac (degrees°minutes'seconds")
    12. Declination (decimal number)
    
    Example:
    ```
    Planet	Date	Time	Motion	Sign Lord	Star Lord	Sub Lord	Zodiac	Nakshatra	Pada	Pos in Zodiac	Declination
    Mo	2025-08-06	01:47:55	D	Ju	Ke	Ju	Saggitarius	Mula	3	07°33'20"	-28.48
    Ke	2025-08-06	02:31:18	D	Su	Ve	Me	Leo	Purvaphalguni	4	25°53'19"	3.96
    ```
    
    Make sure there are no extra spaces or special characters in the column names.
    """)
# === FOOTER ===
st.markdown("---")
st.caption(f"Data source: Astronomics AI Almanac | Report generated: {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}")
