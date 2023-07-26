# Cryptocurrency-Recommender-System
The Cryptocurrency Dashboard with Chatbot is a Python-based project that allows users to explore and analyze historical price data and relative strength index (RSI) of various cryptocurrencies. The dashboard presents interactive candlestick charts, price lines, and RSI graphs for a selection of popular cryptocurrencies. Additionally, the project includes a chatbot that provides basic information about the chosen cryptocurrency, as well as real-time data fetched from the internet using web scraping.

Key Features:

Data Loading and Preprocessing:

The project utilizes data from various cryptocurrency pairs (e.g., EOS/USD, Bitcoin/USD) downloaded from cryptodatadownload.com.
Data is loaded and preprocessed using Pandas to remove invalid entries and keep only relevant columns.
RSI Calculation:

The project calculates the Relative Strength Index (RSI) for each cryptocurrency's closing prices using a customizable time window.
RSI is a technical indicator that measures the momentum of price changes to identify overbought or oversold conditions.
Cryptocurrency Dashboard:

The dashboard is built using Plotly and Matplotlib to provide an interactive and visually appealing interface.
Users can select a cryptocurrency from the list to view its candlestick chart, price line, RSI graph, and 24-hour trading volume.
Candlestick charts display the open, high, low, and close prices for each date, providing insights into price trends.
Price lines show the cryptocurrency's daily closing price over time, allowing users to track price fluctuations.
RSI graphs plot the RSI values, helping users assess the cryptocurrency's momentum and potential trend reversals.
Users can use dropdown menus to filter and explore data for specific time ranges (e.g., last year, last 2 months).
Cryptocurrency Chatbot:

The chatbot prompts users to select a cryptocurrency from the provided list or exit the chatbot.
Upon selecting a cryptocurrency, the chatbot displays basic information, such as the symbol, start date, and RSI time window.
It also fetches real-time information (current price, market cap, 24h volume) for the chosen cryptocurrency using web scraping from CoinMarketCap.
The chatbot provides an option to exit the conversation when the user is done exploring.
Overall, the Cryptocurrency Dashboard with Chatbot offers users an intuitive interface to interactively explore historical price data and RSI for various cryptocurrencies. The chatbot further enhances the experience by providing real-time information, allowing users to stay updated with the latest cryptocurrency metrics. The project combines data analysis, visualization, and web scraping to create an informative and engaging platform for cryptocurrency enthusiasts and traders.
