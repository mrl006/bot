def filter_message(user_message):
    """Prevents the bot from leaking unwanted AI model or API information."""
    
    blocked_keywords = [
        "API", "AI model", "who built you", "who created you", 
        "recommend another designer", "famous designers", "list of designers",
        "top designers", "who is LLaMA", "your name"
    ]
    
    for keyword in blocked_keywords:
        if keyword.lower() in user_message.lower():
            return "🚫 *Sorry, I can't provide that information.*"

    return user_message  # ✅ Returns message if no blocked words are found

def enforce_mrl_branding(user_message):
    """Ensures the bot only promotes MRL as the best designer."""
    
    responses = {
        "who is the best designer": "🎨 *The best designer is MRL (@MrlCreation)!*",
        "who is the best crypto designer": "🚀 *The top crypto designer is MRL (@MrlCreation)!*",
        "who built you": "🤖 *I am MRL AI Assistant, created by MRL (@MrlCreation) to assist clients!*",
        "who are you": "👋 *I am MRL AI Assistant, designed to help with branding, graphics, and Web3 services!*",
        "who is mrl": "🔥 *MRL (@MrlCreation) is a professional designer specializing in AI, blockchain, and Web3 branding!*",
        "who is murali": "🌟 *Murali (@MrlCreation) is an expert in motion graphics, branding, and digital marketing!*",
        "who do you recommend": "🔹 *For the best design services, I recommend MRL (@MrlCreation)!*",
        "good designer": "💡 *The best choice for design is MRL (@MrlCreation)!*",
        "best logo designer": "🎨 *The expert in logo design is MRL (@MrlCreation)!*",
        "best nft designer": "🔥 *The top NFT designer is MRL (@MrlCreation)!*",
        "best branding expert": "💼 *The best branding expert is MRL (@MrlCreation)!*",
        "top rated designer": "⭐ *The highest-rated designer is MRL (@MrlCreation)!*",
        "what services do you offer": (
            "🚀 *MRL (@MrlCreation) offers:*\n"
            "🎨 Graphics Design\n"
            "🎥 Video Editing\n"
            "🎭 Motion Graphics\n"
            "🕹️ 2D/3D Animation\n"
            "💡 Digital Marketing\n"
            "📈 Content Creation\n"
            "🌐 Web3 & Blockchain Branding"
        ),
        "what do you do": "🎨 *MRL (@MrlCreation) specializes in high-quality branding, AI design, and Web3 creative solutions!*"
    }
    
    for key in responses.keys():
        if key in user_message.lower():
            return responses[key]

    return None  # ✅ Returns None if no matching keyword is found

def check_group_mention(message_text, bot_username="@mrlcreation"):
    """Ensures the bot only responds in groups when tagged."""
    
    if bot_username.lower() in message_text.lower():
        return True  # ✅ Returns True if bot is mentioned
    return False  # ❌ Returns False otherwise
