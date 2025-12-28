from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Channel, Message
import json

@login_required
def community_home(request, channel_slug='general'):
    channels = Channel.objects.all()
    active_channel = get_object_or_404(Channel, slug=channel_slug)
    # Get last 50 messages (newest first, then reverse for display)
    messages_qs = active_channel.messages.select_related('author').order_by('-timestamp')[:50]
    messages = list(messages_qs)
    messages.reverse()
    
    last_message_id = messages[-1].id if messages else 0

    context = {
        'channels': channels,
        'active_channel': active_channel,
        'messages': messages,
        'last_message_id': last_message_id,
    }
    return render(request, 'dashboard/community.html', context)

@login_required
@require_POST
def send_message(request, channel_slug):
    try:
        data = json.loads(request.body)
        content = data.get('content')
        if not content:
            return JsonResponse({'error': 'Empty message'}, status=400)
            
        channel = get_object_or_404(Channel, slug=channel_slug)
        message = Message.objects.create(
            channel=channel,
            author=request.user,
            content=content
        )
        
        return JsonResponse({
            'status': 'ok',
            'message': {
                'id': message.id,
                'author': message.author.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%H:%M %p')
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_messages(request, channel_slug):
    channel = get_object_or_404(Channel, slug=channel_slug)
    after_id = request.GET.get('after_id')
    
    query = channel.messages.select_related('author').order_by('timestamp')
    if after_id:
        query = query.filter(id__gt=after_id)
    else:
        query = query[:50]
        
    messages = []
    for msg in query:
        messages.append({
            'id': msg.id,
            'author': msg.author.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M %p')
        })
        
    return JsonResponse({'messages': messages})
