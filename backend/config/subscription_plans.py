"""
Subscription Plan Configuration
Defines limits and features for each subscription tier
"""

SUBSCRIPTION_PLANS = {
    'starter': {
        'name': 'Starter',
        'video_limit': 5,  # videos per month
        'max_duration': 60,  # seconds (1 minute)
        'features': {
            'text_to_video': True,
            'ai_voiceover': True,
            'voiceover_languages': 5,
            'export_quality': '1080p',
            'stock_library': True,
            'branding': 'basic',
            'watermark': True,
            'team_members': 1,
            'api_access': False,
        }
    },
    'professional': {
        'name': 'Professional',
        'video_limit': 15,  # videos per month
        'max_duration': 300,  # seconds (5 minutes)
        'features': {
            'text_to_video': True,
            'ai_voiceover': True,
            'voiceover_languages': 29,
            'export_quality': '4k',
            'stock_library': True,
            'branding': 'advanced',
            'watermark': False,
            'team_members': 3,
            'api_access': False,
            'priority_support': True,
        }
    },
    'enterprise': {
        'name': 'Enterprise',
        'video_limit': 20,  # videos per month
        'max_duration': 1800,  # seconds (30 minutes)
        'features': {
            'text_to_video': True,
            'ai_voiceover': True,
            'voiceover_languages': 'unlimited',
            'export_quality': '4k',
            'stock_library': True,
            'branding': 'custom',
            'watermark': False,
            'team_members': 'unlimited',
            'api_access': True,
            'priority_support': True,
            'dedicated_manager': True,
            'custom_integrations': True,
            'sso': True,
        }
    },
    'free': {
        'name': 'Free',
        'video_limit': 2,  # videos per month
        'max_duration': 30,  # seconds (30 seconds)
        'features': {
            'text_to_video': True,
            'ai_voiceover': False,
            'voiceover_languages': 0,
            'export_quality': '720p',
            'stock_library': False,
            'branding': None,
            'watermark': True,
            'team_members': 1,
            'api_access': False,
        }
    }
}

def get_plan_limits(plan_name):
    """
    Get the limits for a specific plan
    
    Args:
        plan_name (str): Name of the plan ('starter', 'professional', 'enterprise', 'free')
    
    Returns:
        dict: Plan configuration or None if plan doesn't exist
    """
    plan_name = plan_name.lower()
    return SUBSCRIPTION_PLANS.get(plan_name)

def check_video_limit(plan_name, current_videos_count):
    """
    Check if user has reached their video limit
    
    Args:
        plan_name (str): User's subscription plan
        current_videos_count (int): Number of videos created this month
    
    Returns:
        tuple: (bool: can_create, int: remaining_videos)
    """
    plan = get_plan_limits(plan_name)
    if not plan:
        return False, 0
    
    video_limit = plan['video_limit']
    remaining = max(0, video_limit - current_videos_count)
    can_create = current_videos_count < video_limit
    
    return can_create, remaining

def check_duration_limit(plan_name, duration_seconds):
    """
    Check if video duration is within plan limits
    
    Args:
        plan_name (str): User's subscription plan
        duration_seconds (int): Desired video duration in seconds
    
    Returns:
        tuple: (bool: is_valid, int: max_duration)
    """
    plan = get_plan_limits(plan_name)
    if not plan:
        return False, 0
    
    max_duration = plan['max_duration']
    is_valid = duration_seconds <= max_duration
    
    return is_valid, max_duration

def get_plan_features(plan_name):
    """
    Get features for a specific plan
    
    Args:
        plan_name (str): Name of the plan
    
    Returns:
        dict: Plan features or empty dict
    """
    plan = get_plan_limits(plan_name)
    if not plan:
        return {}
    
    return plan.get('features', {})
