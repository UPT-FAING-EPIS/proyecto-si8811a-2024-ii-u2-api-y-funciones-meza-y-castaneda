def is_mobile(user_agent):
    mobile_keywords = ["iphone", "android", "blackberry", "windows phone", "mobile"]
    user_agent = user_agent.lower()
    return any(keyword in user_agent for keyword in mobile_keywords)
