import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz

# === CONFIGURATION ===
BOT_TOKEN = '7613703350:AAE-W4dJ37lngM4lO2Tnuns8-a-80jYRtxk'
CHAT_ID = '-1002840229810'
REMARK = "Aayeshatech Astro Trend"
WEBHOOK_URL = "https://tradingview-webhook-0h3k.onrender.com"

# === DATA FETCHING ===
@st.cache_data(ttl=3600)
def fetch_almanac_data(date):
    try:
        url = f"https://data.astronomics.ai/almanac/?date={date}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Data fetch failed: {str(e)}")
        return None

# === SENTIMENT ANALYSIS ===
def analyze_sentiment(data):
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
    segments.append({
        'start': prev_time,
        'end': end,
        'sign_lord': moon_events.iloc[-1]['Sign Lord'],
        'star_lord': moon_events.iloc[-1]['Star Lord'],
        'sub_lord': moon_events.iloc[-1]['Sub Lord'],
        'zodiac': moon_events.iloc[-1]['Zodiac']
    })
    
    return segments, retrogrades

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

# === TELEGRAM NOTIFICATION ===
def send_telegram_notification(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': f"{REMARK}\n\n{message}",
            'parse_mode': 'HTML'
        }
        requests.post(url, json=payload)
    except Exception as e:
        st.error(f"Telegram notification failed: {str(e)}")

# === STREAMLIT DASHBOARD ===
st.set_page_config(page_title="Astro Market Dashboard", layout="wide")
st.title("🌌 Daily Astro Market Dashboard")

# Date selector
col1, col2 = st.columns([2, 1])
with col1:
    selected_date = st.date_input(
        "Select Date",
        datetime.now(pytz.timezone('Asia/Kolkata')).date(),
        max_value=datetime.now(pytz.timezone('Asia/Kolkata')).date() + timedelta(days=7)
    )
with col2:
    notify = st.checkbox("Send Telegram Notification")

# Fetch and process data
data = fetch_almanac_data(selected_date.strftime("%Y-%m-%d"))

if data:
    segments, retrogrades = analyze_sentiment(data)
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
    
    if strategy:
        st.markdown(" - " + "\n - ".join(strategy))
    else:
        st.info("Neutral market expected")
    
    # Telegram Notification
    if notify and st.button("Send Report to Telegram"):
        message = f"""
        <b>{REMARK}</b>
        <b>Date:</b> {selected_date.strftime('%d %b %Y')}
        
        <b>Market Sentiment:</b>
        {timeline_data[0]['Sentiment']} ({timeline_data[0]['Time Period']})
        
        <b>Top Bullish:</b> {', '.join(list(bullish_sectors.keys())[:2]) if bullish_sectors else 'None'}
        <b>Top Bearish:</b> {', '.join(list(bearish_sectors.keys())[:2]) if bearish_sectors else 'None'}
        
        <b>Key Events:</b> {f"{len(retrogrades)} retrogrades" if not retrogrades.empty else "None"}
        """
        send_telegram_notification(message)
        st.success("Report sent to Telegram!")
    
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
    st.error("Failed to load data. Please check your connection or try another date.")

# === FOOTER ===
st.markdown("---")
st.caption(f"Data source: Astronomics AI Almanac | Report generated: {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}")
