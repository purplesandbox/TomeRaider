from user_interactions.user_interactions import UserInteractions
from dotenv import load_dotenv

load_dotenv()
user = UserInteractions()
user.welcome()
