from .models import Conversation

def get_or_create_conversation(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    conv, created = Conversation.objects.get_or_create(session_key=session_key)
    return conv
