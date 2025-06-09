import os
import json
import subprocess
from datetime import datetime, timedelta
from instruments.instrument import Instrument

class YouTubeManagerInstrument(Instrument):
    """
    Agent Zero Instrument for YouTube Multi-Channel Management
    """
    
    def __init__(self, agent):
        super().__init__(agent)
        self.name = "youtube_manager"
        self.description = "Manages multiple YouTube channels with scheduling and automation"
        self.tiryaki_path = "/Users/macbookpro/Desktop/tiryaki_uploader"
        self.channels = self.load_channels()
    
    def load_channels(self):
        """Load YouTube channels configuration"""
        config_path = f"{self.tiryaki_path}/channels_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def schedule_upload(self, channel_name, video_path, upload_time):
        """Schedule a video upload for specific channel"""
        task = {
            "channel": channel_name,
            "video": video_path,
            "scheduled_time": upload_time,
            "status": "pending"
        }
        
        # Agent Zero'nun scheduler'ına ekle
        self.agent.add_scheduled_task(task)
        
        return f"Video scheduled for {channel_name} at {upload_time}"
    
    def upload_video_now(self, channel_name, video_path):
        """Immediately upload video to specific channel"""
        cmd = [
            "python3",
            f"{self.tiryaki_path}/main_v4_pro_max.py",
            "--channel", channel_name,
            "--video", video_path,
            "--now"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    
    def analyze_performance(self, channel_name=None):
        """Analyze channel performance"""
        # Analytics verilerini topla
        analytics_data = self._get_analytics(channel_name)
        
        # Agent'a rapor hazırlat
        report = f"""
        📊 YouTube Performance Report
        Channel: {channel_name or 'All Channels'}
        Period: Last 7 days
        
        Total Views: {analytics_data.get('views', 0):,}
        New Subscribers: {analytics_data.get('subscribers', 0):,}
        Revenue: ${analytics_data.get('revenue', 0):,.2f}
        Best Performing Video: {analytics_data.get('top_video', 'N/A')}
        """
        
        return report
    
    def optimize_schedule(self):
        """AI-powered schedule optimization"""
        # Her kanal için en iyi yükleme saatlerini bul
        optimal_times = {}
        
        for channel in self.channels:
            # Geçmiş performans verilerini analiz et
            best_hour = self._find_best_upload_hour(channel)
            optimal_times[channel] = best_hour
        
        return optimal_times
    
    def _get_analytics(self, channel_name):
        """Get analytics data from YouTube API"""
        # YouTube Analytics API entegrasyonu
        # Şimdilik mock data
        return {
            "views": 125000,
            "subscribers": 1250,
            "revenue": 2500.50,
            "top_video": "AI Generated Art - Mind Blowing!"
        }
    
    def _find_best_upload_hour(self, channel_name):
        """Find optimal upload hour based on performance"""
        # ML algoritması ile en iyi saati bul
        # Şimdilik basit bir logic
        channel_types = {
            "toxic_motivation": "06:00",  # Sabah erken
            "gym_beast": "17:00",        # Akşam spor saati
            "para_guru": "20:00",        # Akşam prime time
            "gaming": "15:00"            # Öğleden sonra
        }
        
        for key in channel_types:
            if key in channel_name.lower():
                return channel_types[key]
        
        return "19:00"  # Default prime time