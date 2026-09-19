import os
import json

def patch_views():
    filepath = 'myapp/views.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_func = '''def ai_stylist_chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'Prompt cannot be empty'}, status=400)

        ai_reply = get_ai_stylist_recommendation(user_message, request.user)
        return JsonResponse({'reply': ai_reply})'''

    new_func = '''def ai_stylist_chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'Prompt cannot be empty'}, status=400)
            
        chat_history = request.session.get('ai_chat_history', [])

        ai_reply = get_ai_stylist_recommendation(user_message, request.user, chat_history)
        
        chat_history.append({'role': 'user', 'text': user_message})
        chat_history.append({'role': 'model', 'text': ai_reply})
        request.session['ai_chat_history'] = chat_history[-10:]
        
        return JsonResponse({'reply': ai_reply})'''

    if old_func in content:
        content = content.replace(old_func, new_func)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Successfully patched views.py!')
    elif 'chat_history' in content and 'ai_stylist_chat' in content:
        print('views.py is already patched!')
    else:
        print('Could not find the target code in views.py.')


def patch_services():
    filepath = 'myapp/ai_services.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_def = 'def get_ai_stylist_recommendation(user_prompt: str, user=None) -> dict:'
    new_def = 'def get_ai_stylist_recommendation(user_prompt: str, user=None, chat_history: list = None) -> dict:'
    
    if old_def in content:
        content = content.replace(old_def, new_def)

    old_call = '''    chat = client.chats.create(
        model='gemini-flash-lite-latest',
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[search_catalog, add_to_cart],
            temperature=0.7,
        )
    )
    
    response = chat.send_message(user_prompt)
    return response.text'''

    new_call = '''    history_contents = []
    if chat_history:
        for msg in chat_history:
            history_contents.append(
                types.Content(
                    role=msg['role'],
                    parts=[types.Part.from_text(text=msg['text'])]
                )
            )

    kwargs = {
        'model': 'gemini-flash-lite-latest',
        'config': types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[search_catalog, add_to_cart],
            temperature=0.7,
        )
    }
    
    if history_contents:
        kwargs['history'] = history_contents

    chat = client.chats.create(**kwargs)
    
    response = chat.send_message(user_prompt)
    return response.text'''

    if old_call in content:
        content = content.replace(old_call, new_call)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Successfully patched ai_services.py!')
    elif 'history_contents' in content:
        print('ai_services.py is already patched!')
    else:
        print('Could not find the target code in ai_services.py.')

if __name__ == '__main__':
    print("Applying AI Memory Patches...")
    patch_views()
    patch_services()
