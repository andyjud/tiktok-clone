from django.db.models import Count
from django.utils import timezone
from django.db.models import F
from .models import Conversation, ConvUser, Message

def get_or_create_conversation(user1, user2=None):
    if user2 is None or user1 == user2:
        conversation = Conversation.objects.annotate(num_participants=Count("participants")).filter(num_participants=1, participants=user1).first()
        if not conversation:
            conversation = Conversation.objects.create()
            ConvUser.objects.create(conversation=conversation, user=user1)
    else:
        conversation = Conversation.objects.filter(participants=user1).filter(participants=user2).first()
    return conversation


def create_message(sender, receiver, body, image):
    conversation = get_or_create_conversation(sender, receiver)
    if not conversation:
        conversation = Conversation.objects.create()
        ConvUser.objects.bulk_create([
            ConvUser(conversation=conversation, user=sender),
            ConvUser(conversation=conversation, user=receiver),
        ])
        is_new_conversation = True
    else:
        conversation.updated_at = timezone.now()
        conversation.save(update_fields=["updated_at"])
        is_new_conversation = False
        
    message = Message.objects.create(
        conversation=conversation,
        sender=sender,
        body=body,
        image=image,
    )
    
    convuser_receiver = ConvUser.objects.get(conversation=conversation, user=receiver)
    if sender != receiver and not convuser_receiver.is_live:
        ConvUser.objects.filter(
            id=convuser_receiver.id
        ).update(unread_count=F("unread_count") + 1)
        
    ConvUser.objects.filter(
        conversation=conversation,
        user=sender,
    ).update(last_seen_at=timezone.now(),unread_count=0,)
    
    return message, is_new_conversation
    