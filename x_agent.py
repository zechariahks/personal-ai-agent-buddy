#!/usr/bin/env python3
"""
X (formerly Twitter) Agent for posting Bible verses and managing social media content
Uses X API v2 for reliable posting without browser automation
"""

import os
import time
import json
import requests
from datetime import datetime
import random

class XAgent:
    """
    Specialized agent for X (formerly Twitter) social media management
    Posts daily Bible verses and manages X content using official API
    """
    
    def __init__(self, parent_agent=None):
        self.parent = parent_agent
        self.name = "XBot"
        self.api_base_url = "https://api.twitter.com/2"  # X still uses twitter.com API endpoints
        
        # X API credentials
        self.bearer_token = os.getenv("X_BEARER_TOKEN")
        self.api_key = os.getenv("X_API_KEY") or os.getenv("X_CONSUMER_KEY")
        self.api_secret = os.getenv("X_API_SECRET") or os.getenv("X_CONSUMER_SECRET")
        self.access_token = os.getenv("X_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        
        # OpenAI API for intelligent summaries
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Bible verse APIs
        self.bible_apis = [
            #"https://bible-api.com/john+3:16",  # Fallback verse
            "https://labs.bible.org/api/?passage=votd&type=json",  # Verse of the day
            "https://beta.ourmanna.com/api/v1/get/?format=json"  # Our Manna API
        ]
        
        # Check API credentials
        self.api_configured = self._check_api_credentials()
    
    def _check_api_credentials(self):
        """Check if X API credentials are configured"""
        required_creds = [
            self.bearer_token,
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_token_secret
        ]
        
        if all(cred for cred in required_creds):
            print("✅ X API credentials configured")
            return True
        else:
            print("⚠️  X API credentials not fully configured")
            print("💡 Set X_BEARER_TOKEN, X_API_KEY, X_API_SECRET,")
            print("   X_ACCESS_TOKEN, and X_ACCESS_TOKEN_SECRET environment variables")
            return False
    
    def _get_api_headers(self):
        """Get headers for X API requests"""
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
    
    def _get_oauth_headers(self):
        """Get OAuth headers for posting (requires OAuth 1.0a)"""
        # For posting, we need OAuth 1.0a authentication
        # This is a simplified version - in production, use a proper OAuth library
        import hmac
        import hashlib
        import base64
        import urllib.parse
        
        # This is a basic implementation - consider using tweepy or similar library
        return {
            "Authorization": f"OAuth oauth_consumer_key=\"{self.api_key}\", "
                           f"oauth_token=\"{self.access_token}\", "
                           f"oauth_signature_method=\"HMAC-SHA1\", "
                           f"oauth_timestamp=\"{int(time.time())}\", "
                           f"oauth_nonce=\"{random.randint(1000000, 9999999)}\", "
                           f"oauth_version=\"1.0\"",
            "Content-Type": "application/json"
        }
    
    def get_daily_bible_verse(self):
        """Get a daily Bible verse from various APIs"""
        try:
            # Try different Bible APIs
            for api_url in self.bible_apis:
                try:
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Parse different API formats
                        if "text" in data and "reference" in data:
                            # bible-api.com format
                            return f'"{data["text"].strip()}" — {data["reference"]}'
                        elif isinstance(data, list) and len(data) > 0:
                            # labs.bible.org format
                            verse_data = data[0]
                            text = verse_data.get("text", "").strip()
                            book = verse_data.get("bookname", "")
                            chapter = verse_data.get("chapter", "")
                            verse = verse_data.get("verse", "")
                            return f'"{text}" — {book} {chapter}:{verse}'
                        elif "verse" in data:
                            # ourmanna.com format
                            verse_info = data["verse"]
                            text = verse_info.get("details", {}).get("text", "")
                            reference = verse_info.get("details", {}).get("reference", "")
                            return f'"{text}" — {reference}'
                            
                except Exception as api_error:
                    continue
            
            # Fallback verses if APIs fail
            fallback_verses = [
                '"For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life." — John 3:16',
                '"Trust in the Lord with all your heart and lean not on your own understanding." — Proverbs 3:5',
                '"I can do all this through him who gives me strength." — Philippians 4:13',
                '"The Lord is my shepherd, I lack nothing." — Psalm 23:1',
                '"Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go." — Joshua 1:9'
            ]
            
            return random.choice(fallback_verses)
            
        except Exception as e:
            return '"Be still, and know that I am God." — Psalm 46:10'
    
    def post_to_x(self, text):
        """Post a message to X using X API v2"""
        try:
            if not self.api_configured:
                return "❌ X API not configured. Please set up API credentials."
            
            if len(text) > 280:
                text = text[:277] + "..."
            
            # Use X API v2 for posting
            url = f"{self.api_base_url}/tweets"
            
            payload = {
                "text": text
            }
            
            # For posting, we need OAuth 1.0a authentication
            # Using a simplified approach here - in production, use tweepy
            try:
                import tweepy
                
                # Use tweepy for OAuth authentication
                auth = tweepy.OAuth1UserHandler(
                    self.api_key,
                    self.api_secret,
                    self.access_token,
                    self.access_token_secret
                )
                
                api = tweepy.API(auth)
                client = tweepy.Client(
                    bearer_token=self.bearer_token,
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_token_secret
                )
                
                response = client.create_tweet(text=text)
                return f"✅ Post shared on X successfully! Post ID: {response.data['id']}"
                
            except ImportError:
                print("⚠️  tweepy not installed. Install with: pip install tweepy")
                # Fallback to manual OAuth (simplified - not production ready)
                headers = self._get_oauth_headers()
                response = requests.post(url, json=payload, headers=headers)
                
                if response.status_code == 201:
                    post_data = response.json()
                    return f"✅ Post shared on X successfully! Post ID: {post_data['data']['id']}"
                else:
                    return f"❌ Failed to post to X: {response.status_code} - {response.text}"
                    
        except Exception as e:
            return f"❌ Error posting to X: {str(e)}"
    
    def post_daily_bible_verse(self):
        """Post daily Bible verse to X"""
        try:
            print("📱 Getting daily Bible verse...")
            verse = self.get_daily_bible_verse()
            
            # Add hashtags and formatting
            post_text = f"{verse}\n\n#BibleVerse #Faith #DailyVerse #Inspiration"
            
            print(f"📱 Posting to X: {post_text[:100]}...")
            result = self.post_to_x(post_text)
            
            # Store in context memory if parent agent exists
            if self.parent and hasattr(self.parent, 'context_memory'):
                if "x_activity" not in self.parent.context_memory:
                    self.parent.context_memory["x_activity"] = []
                
                self.parent.context_memory["x_activity"].append({
                    "action": "bible_verse_posted",
                    "verse": verse,
                    "result": result,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            return result
            
        except Exception as e:
            return f"❌ Error posting daily Bible verse: {str(e)}"
    
    def post_custom_message(self, message):
        """Post a custom message to X"""
        try:
            print(f"📱 Posting custom message to X: {message[:50]}...")
            result = self.post_to_x(message)
            
            # Store in context memory if parent agent exists
            if self.parent and hasattr(self.parent, 'context_memory'):
                if "x_activity" not in self.parent.context_memory:
                    self.parent.context_memory["x_activity"] = []
                
                self.parent.context_memory["x_activity"].append({
                    "action": "custom_post_shared",
                    "message": message,
                    "result": result,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            return result
            
        except Exception as e:
            return f"❌ Error posting custom message: {str(e)}"
    
    def get_trending_topics(self, woeid=1):
        """Get trending topics from X (fallback to search if trends API unavailable)"""
        try:
            if not self.api_configured:
                return "❌ X API not configured"
            
            # Try X API v1.1 for trends first
            url = "https://api.twitter.com/1.1/trends/place.json"
            params = {"id": woeid}  # 1 = Worldwide, 23424977 = United States
            
            headers = {
                "Authorization": f"Bearer {self.bearer_token}"
            }
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    trends = data[0].get("trends", [])
                    trending_topics = []
                    
                    for trend in trends[:10]:  # Get top 10 trends
                        topic_info = {
                            "name": trend.get("name", ""),
                            "url": trend.get("url", ""),
                            "tweet_volume": trend.get("tweet_volume"),
                            "query": trend.get("query", "")
                        }
                        trending_topics.append(topic_info)
                    
                    return trending_topics
                else:
                    return "❌ No trending topics found"
            else:
                # Fallback: Use popular search terms as "trending topics"
                print("📱 Trends API unavailable, using popular search terms...")
                popular_topics = [
                    {"name": "#AI", "query": "AI artificial intelligence", "tweet_volume": None},
                    {"name": "#Technology", "query": "technology tech", "tweet_volume": None},
                    {"name": "#News", "query": "breaking news", "tweet_volume": None},
                    {"name": "#World", "query": "world news", "tweet_volume": None},
                    {"name": "#Business", "query": "business finance", "tweet_volume": None}
                ]
                return popular_topics
                
        except Exception as e:
            # Fallback to simulated trending topics
            print(f"📱 Using fallback trending topics due to: {str(e)}")
            return [
                {"name": "#AI", "query": "AI artificial intelligence", "tweet_volume": None},
                {"name": "#Technology", "query": "technology tech", "tweet_volume": None},
                {"name": "#News", "query": "breaking news", "tweet_volume": None},
                {"name": "#World", "query": "world news", "tweet_volume": None},
                {"name": "#Business", "query": "business finance", "tweet_volume": None}
            ]
    
    def search_recent_tweets(self, query, max_results=10):
        """Search for recent tweets on a topic"""
        try:
            if not self.api_configured:
                return "❌ X API not configured"
            
            # Use X API v2 for tweet search
            url = "https://api.twitter.com/2/tweets/search/recent"
            params = {
                "query": query,
                "max_results": min(max_results, 100),
                "tweet.fields": "created_at,author_id,public_metrics,context_annotations",
                "expansions": "author_id",
                "user.fields": "name,username,verified"
            }
            
            headers = {
                "Authorization": f"Bearer {self.bearer_token}"
            }
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                tweets = data.get("data", [])
                
                if not tweets:
                    print(f"📱 No tweets found for query: {query}")
                    return []  # Return empty list instead of error message
                
                users = {user["id"]: user for user in data.get("includes", {}).get("users", [])}
                
                tweet_summaries = []
                for tweet in tweets:
                    author = users.get(tweet.get("author_id"), {})
                    metrics = tweet.get("public_metrics", {})
                    
                    tweet_info = {
                        "text": tweet.get("text", ""),
                        "author": author.get("name", "Unknown"),
                        "username": author.get("username", "unknown"),
                        "verified": author.get("verified", False),
                        "created_at": tweet.get("created_at", ""),
                        "likes": metrics.get("like_count", 0),
                        "retweets": metrics.get("retweet_count", 0),
                        "replies": metrics.get("reply_count", 0)
                    }
                    tweet_summaries.append(tweet_info)
                
                return tweet_summaries
            elif response.status_code == 429:
                print("📱 Rate limit reached, using fallback data...")
                return []  # Return empty list for rate limiting
            else:
                print(f"📱 Search API error: {response.status_code}")
                return []  # Return empty list instead of error message
                
        except Exception as e:
            print(f"📱 Search error: {str(e)}")
            return []  # Return empty list instead of error message
    
    def get_news_and_trends_summary(self):
        """Get comprehensive news and trends summary from X"""
        try:
            print("📱 Getting X trending topics...")
            trends = self.get_trending_topics()
            
            news_data = {
                "trending_topics": trends,
                "topic_tweets": {}
            }
            
            if isinstance(trends, list) and trends:
                print(f"📱 Found {len(trends)} trending topics, getting sample tweets...")
                
                # Get sample tweets for top 3 trending topics
                for i, trend in enumerate(trends[:3]):
                    topic_name = trend.get("name", "")
                    topic_query = trend.get("query", topic_name)
                    
                    if topic_query:
                        print(f"📱 Getting tweets for: {topic_name}")
                        topic_tweets = self.search_recent_tweets(topic_query, max_results=5)
                        news_data["topic_tweets"][topic_name] = topic_tweets
                        
                        # Add small delay to avoid rate limiting
                        import time
                        time.sleep(1)
            else:
                # If trends is an error string, handle it
                print(f"📱 Trends result: {trends}")
                news_data["trending_topics"] = []
                news_data["error"] = str(trends)
            
            return news_data
            
        except Exception as e:
            return f"❌ Error getting news and trends: {str(e)}"
    
    def get_x_feed_summary(self, max_tweets=20):
        """Get a summary of recent tweets from X timeline"""
        try:
            if not self.api_configured:
                return "❌ X API not configured"
            
            # Search for recent popular tweets (general feed simulation)
            popular_queries = [
                "breaking news",
                "trending now", 
                "latest news",
                "technology news",
                "world news"
            ]
            
            all_tweets = []
            for query in popular_queries[:2]:  # Limit to avoid rate limits
                tweets = self.search_recent_tweets(f"{query} -is:retweet", max_results=5)
                if isinstance(tweets, list) and tweets:  # Check if it's a non-empty list
                    all_tweets.extend(tweets)
                # Add small delay to avoid rate limiting
                import time
                time.sleep(0.5)
            
            # Sort by engagement (likes + retweets)
            if all_tweets:
                all_tweets.sort(key=lambda x: x.get("likes", 0) + x.get("retweets", 0), reverse=True)
                return all_tweets[:max_tweets]
            else:
                # Try with simpler queries if no results
                print("📱 No results with complex queries, trying simpler search...")
                simple_tweets = self.search_recent_tweets("news", max_results=10)
                if isinstance(simple_tweets, list) and simple_tweets:
                    return simple_tweets[:max_tweets]
                else:
                    # Return empty list instead of error string
                    print("📱 No tweets found with any query")
                    return []
                
        except Exception as e:
            print(f"📱 Error getting X feed: {str(e)}")
            return []  # Return empty list instead of error string
    
    def _generate_ai_summary(self, data, summary_type="news"):
        """Generate AI-powered summary using OpenAI"""
        try:
            if not self.openai_api_key:
                return "❌ OpenAI API key not configured for AI summaries"
            
            # Prepare the data for summarization
            if summary_type == "trends":
                prompt = self._create_trends_prompt(data)
            elif summary_type == "news":
                prompt = self._create_news_prompt(data)
            else:
                prompt = f"Please summarize this social media data: {str(data)[:1000]}"
            
            # Call OpenAI API
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that creates concise, informative summaries of social media trends and news. Focus on the most important and interesting information."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                summary = data["choices"][0]["message"]["content"]
                return summary.strip()
            else:
                return f"❌ OpenAI API error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ Error generating AI summary: {str(e)}"
    
    def _create_trends_prompt(self, trends_data):
        """Create a prompt for trending topics summary"""
        trending_topics = trends_data.get("trending_topics", [])
        topic_tweets = trends_data.get("topic_tweets", {})
        
        prompt = "Please create a concise summary of these trending topics on X (Twitter):\n\n"
        prompt += "TRENDING TOPICS:\n"
        
        for i, trend in enumerate(trending_topics[:5], 1):
            if isinstance(trend, dict):
                name = trend.get("name", "Unknown")
                volume = trend.get("tweet_volume")
                prompt += f"{i}. {name}"
                if volume:
                    prompt += f" ({volume:,} tweets)"
                prompt += "\n"
            else:
                prompt += f"{i}. {str(trend)}\n"
        
        prompt += "\nSAMPLE TWEETS FOR TOP TOPICS:\n"
        for topic, tweets in list(topic_tweets.items())[:3]:
            prompt += f"\n{topic}:\n"
            if isinstance(tweets, list):
                for tweet in tweets[:2]:
                    if isinstance(tweet, dict):
                        prompt += f"- {tweet.get('text', '')[:100]}...\n"
                    else:
                        prompt += f"- {str(tweet)[:100]}...\n"
            else:
                prompt += f"- {str(tweets)[:100]}...\n"
        
        prompt += "\nPlease provide a summary that includes:\n"
        prompt += "1. What topics are trending and why\n"
        prompt += "2. Key themes or events driving the trends\n"
        prompt += "3. Any notable patterns or insights\n"
        prompt += "Keep it concise but informative."
        
        return prompt
    
    def _create_news_prompt(self, news_data):
        """Create a prompt for news summary"""
        if isinstance(news_data, list):
            tweets = news_data
        else:
            tweets = news_data.get("tweets", [])
        
        prompt = "Please create a news summary based on these recent tweets:\n\n"
        
        for i, tweet in enumerate(tweets[:10], 1):
            author = tweet.get("author", "Unknown")
            text = tweet.get("text", "")
            likes = tweet.get("likes", 0)
            retweets = tweet.get("retweets", 0)
            
            prompt += f"{i}. @{tweet.get('username', 'unknown')} ({author})\n"
            prompt += f"   {text[:150]}...\n"
            prompt += f"   {likes} likes, {retweets} retweets\n\n"
        
        prompt += "Please provide a news summary that includes:\n"
        prompt += "1. Main news stories and events\n"
        prompt += "2. Key developments or breaking news\n"
        prompt += "3. Important trends or themes\n"
        prompt += "4. Any significant public reactions\n"
        prompt += "Keep it organized and easy to read."
        
        return prompt
    
    def get_intelligent_trends_summary(self):
        """Get AI-powered summary of trending topics"""
        try:
            print("📱 Getting trending topics and generating AI summary...")
            
            # Get trends and sample tweets
            trends_data = self.get_news_and_trends_summary()
            
            if isinstance(trends_data, dict):
                trending_topics = trends_data.get("trending_topics", [])
                
                if isinstance(trending_topics, list) and trending_topics:
                    # Generate AI summary
                    ai_summary = self._generate_ai_summary(trends_data, "trends")
                    
                    # Combine with raw data
                    result = f"""
🔥 X Trending Topics - AI Summary

{ai_summary}

📊 Raw Data:
• {len(trending_topics)} trending topics found
• Sample tweets analyzed for top topics
• Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """.strip()
                    
                    return result
                else:
                    # Handle case where trends API is unavailable
                    error_msg = trends_data.get("error", "Unknown error")
                    return f"""
🔥 X Trending Topics - Limited Access

❌ Trending topics API unavailable: {error_msg}

💡 Your X API access level may not include trending topics.
   Using fallback popular topics for demonstration.

📊 Fallback topics analyzed:
• AI & Technology
• Breaking News  
• World Events
• Business & Finance

Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """.strip()
            else:
                return f"❌ Could not get trending topics: {trends_data}"
                
        except Exception as e:
            return f"❌ Error getting intelligent trends summary: {str(e)}"
    
    def get_intelligent_news_summary(self):
        """Get AI-powered summary of recent news from X"""
        try:
            print("📱 Getting recent news tweets and generating AI summary...")
            
            # Get recent news-related tweets
            news_tweets = self.get_x_feed_summary(max_tweets=15)
            
            if isinstance(news_tweets, list) and news_tweets:
                # Generate AI summary
                ai_summary = self._generate_ai_summary(news_tweets, "news")
                
                # Combine with raw data
                result = f"""
📰 X News Summary - AI Powered

{ai_summary}

📊 Analysis Based On:
• {len(news_tweets)} recent high-engagement tweets
• News, breaking updates, and trending discussions
• Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """.strip()
                
                return result
            else:
                # Handle case where no tweets are found or API issues
                if isinstance(news_tweets, str):
                    error_msg = news_tweets
                else:
                    error_msg = "No recent tweets found"
                
                return f"""
📰 X News Summary - Limited Access

❌ Unable to retrieve recent news tweets: {error_msg}

💡 This may be due to:
• X API access limitations
• Rate limiting
• No recent high-engagement news tweets

🔄 Try again later or check X directly for the latest news.

Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """.strip()
                
        except Exception as e:
            return f"❌ Error getting intelligent news summary: {str(e)}"
    
    def get_combined_x_summary(self):
        """Get comprehensive X summary with trends and news"""
        try:
            print("📱 Getting comprehensive X summary...")
            
            # Get both trends and news
            trends_summary = self.get_intelligent_trends_summary()
            news_summary = self.get_intelligent_news_summary()
            
            combined = f"""
📱 Complete X Summary - {datetime.now().strftime('%A, %B %d, %Y')}

{trends_summary}

---

{news_summary}

💡 This summary combines trending topics and recent news from X,
   analyzed and summarized using AI for easy consumption.
            """.strip()
            
            # Store in context memory if parent agent exists
            if self.parent and hasattr(self.parent, 'context_memory'):
                if "x_summaries" not in self.parent.context_memory:
                    self.parent.context_memory["x_summaries"] = []
                
                self.parent.context_memory["x_summaries"].append({
                    "summary": combined,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "combined"
                })
            
            return combined
            
        except Exception as e:
            return f"❌ Error getting combined X summary: {str(e)}"
    
    def get_x_status(self):
        """Get X account status and recent activity"""
        try:
            # Check recent activity from context memory
            if self.parent and hasattr(self.parent, 'context_memory'):
                recent_activity = self.parent.context_memory.get("x_activity", [])
                recent_summaries = self.parent.context_memory.get("x_summaries", [])
                
                status = f"""
📱 X Status:
• API Configuration: {'✅ Ready' if self.api_configured else '❌ Not configured'}
• OpenAI Integration: {'✅ Available' if self.openai_api_key else '❌ Not configured'}
• Recent posts: {len(recent_activity)} activities
• Recent summaries: {len(recent_summaries)} generated
                """.strip()
                
                if recent_activity:
                    latest = recent_activity[-1]
                    status += f"\n• Last activity: {latest['action']} at {latest['timestamp']}"
                
                if recent_summaries:
                    latest_summary = recent_summaries[-1]
                    status += f"\n• Last summary: {latest_summary['timestamp']}"
                
                return status
            else:
                return f"""
📱 X Status:
• API Configuration: {'✅ Ready' if self.api_configured else '❌ Not configured'}
• OpenAI Integration: {'✅ Available' if self.openai_api_key else '❌ Not configured'}
• Ready for: Posting, Trends, News Summaries
                """.strip()
                
        except Exception as e:
            return f"❌ X status error: {str(e)}"


    def cleanup(self):
        """Clean up resources (no browser to close)"""
        try:
            print("✅ X agent cleaned up")
        except Exception as e:
            print(f"⚠️ X cleanup warning: {str(e)}")

def main():
    """Test the enhanced X agent"""
    print("📱 Testing Enhanced X Agent")
    print("=" * 50)
    
    agent = XAgent()
    
    try:
        # Test Bible verse retrieval
        verse = agent.get_daily_bible_verse()
        print(f"📖 Daily Bible verse: {verse}")
        
        # Test trending topics
        if agent.api_configured:
            print("\n🔥 Testing trending topics...")
            trends = agent.get_trending_topics()
            if isinstance(trends, list):
                print(f"Found {len(trends)} trending topics")
                for i, trend in enumerate(trends[:3], 1):
                    print(f"{i}. {trend.get('name', 'Unknown')}")
            
            print("\n📰 Testing AI news summary...")
            news_summary = agent.get_intelligent_news_summary()
            print(news_summary[:200] + "..." if len(news_summary) > 200 else news_summary)
            
            print("\n🔄 Would you like to post the Bible verse to X? (y/n)")
            choice = input().lower().strip()
            
            if choice in ['y', 'yes']:
                result = agent.post_daily_bible_verse()
                print(result)
            else:
                print("📱 Skipping X post")
        else:
            print("📱 X API not configured - skipping advanced tests")
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        agent.cleanup()


if __name__ == "__main__":
    main()
