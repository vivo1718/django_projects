import json
from django.shortcuts import render
from google import genai  # 👈 Official New SDK Import
from .models import CapsuleDiscovery

# 📑 Your official secure API token is safely mapped right here
GEMINI_API_KEY = ""

def fetch_ai_album_recommendation(mood_text):
    """Queries Gemini via the official google-genai Interactions SDK."""
    # Initialize the client using your specified credential block
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = (
        f"Based on the mood context: '{mood_text}', recommend exactly one music album. "
        "Your response MUST be raw JSON formatting containing exactly these keys: "
        "'album', 'artist', 'year', 'review' (a beautiful 2-sentence description of its sonic vibe). "
        "Do not wrap your answer in markdown code blocks or triple backticks. Return ONLY the raw JSON string data."
    )
    
    try:
        # ⚡ OFFICIAL INTERACTIONS API CALL blueprint
        interaction = client.interactions.create(
            model="gemini-3.8-flash",  # Matches your target architecture
            input=prompt
        )
        
        # Pull text response via output_text attribute natively
        raw_text = interaction.output_text.strip()
        
        # Robust Sanitisation Step to prevent code fence injection crashes
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()
            
        return json.loads(raw_text)
        
    except Exception as e:
        print(f"Official SDK Error Details: {e}")
        return None

def capsule_dashboard_view(request):
    """Handles mood prompts, registers discoveries, and compiles the interface."""
    mood = request.GET.get('mood', '').strip()
    current_discovery = None

    if mood:
        ai_data = fetch_ai_album_recommendation(mood)
        if ai_data:
            search_term = f"{ai_data['artist']} - {ai_data['album']} Full Album"
            
            # Save transaction safely into local SQLite tables
            current_discovery = CapsuleDiscovery.objects.create(
                mood_query=str(mood),
                album_title=str(ai_data['album']),
                artist_name=str(ai_data['artist']),
                release_year=str(ai_data['year']),
                ai_review=str(ai_data['review']),
                youtube_search_term=str(search_term)
            )

    # Fetch recent discoveries list
    recent_discoveries = CapsuleDiscovery.objects.order_by('-discovered_at')[:6]

    return render(request, 'vibe_music/dashboard.html', {
        'discovery': current_discovery,
        'recent': recent_discoveries,
        'mood': mood
    })
