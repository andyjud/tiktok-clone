from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from .utils import get_or_create_conversation, create_message
from .models import Conversation, Message, ConvUser

User = get_user_model()

@login_required
def messages(request):
    context = {
        'page': "Messages",
    }
    return render(request, "a_messages/messages_page.html", context)


@login_required
def conversations(request):
    get_or_create_conversation(request.user)
    conversations = Conversation.objects.filter(participants=request.user).order_by("-updated_at")
    
    conversations_extended = []
    for conversation in conversations:
        is_self = conversation.participants.count() == 1
        if is_self:
            receiver = request.user
        else:
            receiver = conversation.participants.exclude(pk=request.user.pk).first()
            
        my_convuser = ConvUser.objects.filter(conversation=conversation, user=request.user).first()
            
        conversations_extended.append({
            'conversation': conversation,
            'receiver': receiver,
            'is_self': is_self,
            'my_convuser': my_convuser,
        })
    
    context = {
        'conversations': conversations_extended,
    }
    return render(request, "a_messages/conversations.html", context)


@login_required
def chat(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if receiver and receiver != request.user:
        chat = get_or_create_conversation(request.user, receiver)
        is_self = False
    else:
        chat = get_or_create_conversation(request.user)
        is_self = True
        
    messages = reversed(Message.objects.filter(conversation=chat).order_by("-created_at")[:100])
    
    ConvUser.objects.filter(conversation=chat, user=request.user).update(unread_count=0, last_seen_at=timezone.now())
    
    context = {
        'page': "Messages",
        'receiver': receiver,
        'chat': chat,
        'messages': messages,
        'is_self': is_self,
    }
    return render(request, "a_messages/chat.html", context)


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    
    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        image = request.FILES.get("image")
        
        if not body and not image:
            return HttpResponse()
        
        message = create_message(
            sender=request.user,
            receiver=receiver,
            body=body,
            image=image,
        )
        
        context = {
            'message': message,
        }
        return render(request,"a_messages/message.html", context)
    
    return HttpResponse()


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    message.delete()
    return HttpResponse()