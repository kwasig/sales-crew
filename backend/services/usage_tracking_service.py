"""
Usage Tracking Service for Sales Crew Application
Tracks user activity, search metrics, and system usage for dashboard analytics
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import json
import uuid

class UsageTrackingService:
    def __init__(self):
        self.usage_data = {
            'sessions': {},
            'searches': [],
            'metrics': {
                'total_searches': 0,
                'successful_searches': 0,
                'average_response_time': 0,
                'popular_companies': {},
                'hourly_usage': defaultdict(int),
                'daily_usage': defaultdict(int)
            }
        }
        
    def start_session(self, user_id: str = "anonymous") -> str:
        """Start a new user session"""
        session_id = str(uuid.uuid4())
        self.usage_data['sessions'][session_id] = {
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'search_count': 0,
            'last_activity': datetime.now().isoformat()
        }
        return session_id
    
    def track_search(self, session_id: str, company_name: str, search_params: Dict, success: bool = True):
        """Track a search operation"""
        if session_id not in self.usage_data['sessions']:
            return
            
        search_record = {
            'session_id': session_id,
            'company_name': company_name,
            'search_params': search_params,
            'timestamp': datetime.now().isoformat(),
            'success': success
        }
        
        self.usage_data['searches'].append(search_record)
        self.usage_data['sessions'][session_id]['search_count'] += 1
        self.usage_data['sessions'][session_id]['last_activity'] = datetime.now().isoformat()
        
        # Update metrics
        self.usage_data['metrics']['total_searches'] += 1
        if success:
            self.usage_data['metrics']['successful_searches'] += 1
        
        # Track popular companies
        self.usage_data['metrics']['popular_companies'][company_name] = \
            self.usage_data['metrics']['popular_companies'].get(company_name, 0) + 1
        
        # Track hourly usage
        hour = datetime.now().strftime('%H:00')
        self.usage_data['metrics']['hourly_usage'][hour] += 1
        
        # Track daily usage
        day = datetime.now().strftime('%Y-%m-%d')
        self.usage_data['metrics']['daily_usage'][day] += 1
    
    def get_dashboard_metrics(self) -> Dict:
        """Get comprehensive dashboard metrics"""
        total_sessions = len(self.usage_data['sessions'])
        active_sessions = sum(1 for session in self.usage_data['sessions'].values() 
                            if (datetime.now() - datetime.fromisoformat(session['last_activity'])).seconds < 3600)
        
        # Calculate success rate
        success_rate = 0
        if self.usage_data['metrics']['total_searches'] > 0:
            success_rate = (self.usage_data['metrics']['successful_searches'] / self.usage_data['metrics']['total_searches']) * 100
        
        # Get top companies
        top_companies = sorted(
            self.usage_data['metrics']['popular_companies'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            'overview': {
                'total_sessions': total_sessions,
                'active_sessions': active_sessions,
                'total_searches': self.usage_data['metrics']['total_searches'],
                'success_rate': round(success_rate, 1),
                'average_searches_per_session': round(self.usage_data['metrics']['total_searches'] / max(1, total_sessions), 1)
            },
            'activity': {
                'hourly_usage': dict(self.usage_data['metrics']['hourly_usage']),
                'daily_usage': dict(self.usage_data['metrics']['daily_usage'])
            },
            'top_companies': [{'name': company, 'searches': count} for company, count in top_companies],
            'recent_searches': self.usage_data['searches'][-10:]
        }
    
    def get_usage_analytics(self, days: int = 7) -> Dict:
        """Get detailed usage analytics for the specified number of days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_searches = [
            search for search in self.usage_data['searches']
            if datetime.fromisoformat(search['timestamp']) >= cutoff_date
        ]
        
        return {
            'period': f"Last {days} days",
            'total_searches': len(recent_searches),
            'successful_searches': sum(1 for s in recent_searches if s['success']),
            'unique_companies': len(set(s['company_name'] for s in recent_searches)),
            'searches_by_day': self._get_searches_by_day(recent_searches)
        }
    
    def _get_searches_by_day(self, searches: List) -> Dict:
        """Group searches by day"""
        searches_by_day = defaultdict(int)
        for search in searches:
            day = datetime.fromisoformat(search['timestamp']).strftime('%Y-%m-%d')
            searches_by_day[day] += 1
        return dict(searches_by_day)

# Global instance
usage_tracker = UsageTrackingService()