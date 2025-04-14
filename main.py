import json
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from datetime import datetime

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Load environment variables
load_dotenv()

class SearchAssistant:
    def __init__(self):
        self.name = "Google Search Assistant"
        self.wake_word = config['wake_word']
        self.search_history = []  # Stores tuples of (query, timestamp, count)
        self.result_clicks = {}  # Tracks clicks per result URL
        
    def get_suggestions(self, query):
        """Get search suggestions from Google Autocomplete"""
        try:
            service = build("customsearch", "v1",
                          developerKey=os.getenv("GOOGLE_API_KEY"))
            res = service.cse().suggest(
                q=query,
                cx=os.getenv("GOOGLE_CSE_ID")
            ).execute()
            return [suggestion['query'] for suggestion in res.get('items', [])]
        except Exception:
            return []

    def generate_response(self, query, filter_type=None, date_range=None, site_filter=None):
        """Track search metrics before generating response"""
        self._track_search_metrics(query)
        try:
            # Add/update search history
            now = datetime.now()
            for i, (q, t, c) in enumerate(self.search_history):
                if q == query:
                    # Update existing entry
                    self.search_history[i] = (q, now, c+1)
                    break
            else:
                # Add new entry (keep last 20)
                self.search_history = [(query, now, 1)] + self.search_history[:19]
            
            service = build("customsearch", "v1", 
                          developerKey=os.getenv("GOOGLE_API_KEY"))
            
            # Build query with filters
            search_params = {
                'q': query,
                'cx': os.getenv("GOOGLE_CSE_ID"),
                'num': 3
            }
            
            # Apply filters if specified
            if filter_type:
                if filter_type == 'images':
                    search_params['searchType'] = 'image'
                elif filter_type == 'videos':
                    search_params['searchType'] = 'video'
            
            if date_range:
                search_params['dateRestrict'] = date_range
                
            if site_filter:
                search_params['siteSearch'] = site_filter
            
            res = service.cse().list(**search_params).execute()
            
            formatted_results = []
            for item in res.get('items', []):
                if filter_type == 'images':
                    result = f"{item['title']}\nImage URL: {item['link']}\n"
                elif filter_type == 'videos':
                    result = f"{item['title']}\nVideo URL: {item['link']}\n"
                else:
                    result = f"{item['title']}\n{item['snippet']}\nLink: {item['link']}\n"
                formatted_results.append(result)
            
            return "\n".join(formatted_results)
        except Exception as e:
            return f"Error: {str(e)}"

    def _track_search_metrics(self, query):
        """Track search frequency and timing patterns"""
        now = datetime.now()
        hour = now.hour
        weekday = now.weekday()
        # We'll add more detailed tracking here later

    def get_analytics(self):
        """Return search analytics data"""
        if not self.search_history:
            return "No search data available yet"

        # Calculate basic stats
        total_searches = len(self.search_history)
        unique_queries = len({q for q,t,c in self.search_history})
        avg_searches = sum(c for q,t,c in self.search_history) / total_searches

        # Get top queries
        query_counts = {}
        for q, t, c in self.search_history:
            query_counts[q] = query_counts.get(q, 0) + c
        top_queries = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        # Format analytics report
        report = [
            f"📊 Search Analytics Report",
            f"Total searches: {total_searches}",
            f"Unique queries: {unique_queries}",
            f"Avg searches per query: {avg_searches:.1f}",
            "\nTop 5 queries:"
        ]
        for i, (query, count) in enumerate(top_queries, 1):
            report.append(f"{i}. {query} ({count}x)")

        return "\n".join(report)

    def get_history(self, search_term=None, sort_by='recent'):
        """Returns formatted search history with filtering and sorting"""
        if not self.search_history:
            return "No search history yet"
            
        # Filter history if search term provided
        filtered = self.search_history
        if search_term:
            filtered = [(q,t,c) for q,t,c in filtered if search_term.lower() in q.lower()]
            
        # Sort history
        if sort_by == 'recent':
            filtered.sort(key=lambda x: x[1], reverse=True)
        elif sort_by == 'frequent':
            filtered.sort(key=lambda x: x[2], reverse=True)
            
        # Format results
        results = []
        for i, (query, timestamp, count) in enumerate(filtered, 1):
            date_str = timestamp.strftime("%Y-%m-%d %H:%M")
            results.append(f"{i}. {query} (used {count}x, last: {date_str})")
            
        return "\n".join(results) if results else "No matching history found"
        
    def clear_history(self):
        """Clears all search history"""
        self.search_history = []
        return "History cleared successfully"
        
    def delete_history_item(self, index):
        """Deletes a specific history item by index"""
        try:
            if 0 <= index < len(self.search_history):
                deleted = self.search_history.pop(index)
                return f"Deleted: {deleted}"
            return "Invalid index"
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Please run gui.py for the graphical interface")
