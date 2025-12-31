

DASHBOARD_MODULES = [
    {
        'id': 'game_feedback',
        'title': 'Game Tester Feedback',
        'enabled': True,
        'api_endpoint': '/api/feedback',
        'description': 'Detailed feedback from game testers',
        'highlight_columns': ['name', 'cat_name', 'game_completed', 'would_pay']
    },
    {
        'id': 'support_tickets',
        'title': 'Support Tickets',
        'enabled': True,
        'api_endpoint': '/api/support',
        'description': 'User-reported issues and bugs',
        'highlight_columns': ['name', 'email', 'page', 'issue_description']
    },
    {
        'id': 'tester_signups',
        'title': 'Tester Signups',
        'enabled': True,
        'api_endpoint': '/api/tester-signup',
        'description': 'Users who signed up to be game testers',
        'highlight_columns': ['name', 'email', 'signed_up_at']
    }
]

def get_enabled_modules():
    """Returns only enabled modules"""
    return [m for m in DASHBOARD_MODULES if m['enabled']]