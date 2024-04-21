# Integrate-with-YOU-TUBE
In this project, I'm using the YouTube Data API to retrieve statistics about a specific channel and one of its videos. I'm fetching data such as the channel name, number of subscribers, total views, and total videos for the channel, as well as metrics for a specific video including its total views, number of likes, dislikes, and comments.

After fetching the data, I'm creating two tables in a DuckDB database: channel_stats and video_metrics. These tables store the retrieved data. I use the INSERT statement to insert the fetched data into their respective tables.

Finally, print the fetched data using PrettyTable for better visualization and close the connection to the DuckDB database.

This project essentially demonstrates how to fetch data from an API, store it in a local database, and perform basic data manipulation operations.
