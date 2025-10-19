from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def generate_script(prompt: str, video_length: str = "short") -> dict:
    """Generate video script using OpenAI GPT-4"""
    try:
        word_count = {
            "short": "100-150",
            "medium": "200-300",
            "long": "400-500"
        }.get(video_length, "100-150")
        
        system_prompt = f"""You are a professional video script writer. Create engaging video scripts that are optimized for AI video generation.
        
        Guidelines:
        - Write in a conversational, engaging tone
        - Break content into clear scenes
        - Include visual descriptions for each scene
        - Keep scenes short and punchy
        - Word count: {word_count} words
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a video script about: {prompt}"}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        script_text = response.choices[0].message.content
        
        # Parse script into scenes
        scenes = parse_script_into_scenes(script_text)
        
        return {
            'success': True,
            'script': script_text,
            'scenes': scenes,
            'word_count': len(script_text.split())
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def parse_script_into_scenes(script_text: str) -> list:
    """Parse script text into individual scenes"""
    # Simple parsing - split by paragraphs or newlines
    lines = [line.strip() for line in script_text.split('\n') if line.strip()]
    
    scenes = []
    current_scene = ""
    
    for line in lines:
        if line.startswith("Scene") or line.startswith("#"):
            if current_scene:
                scenes.append({'text': current_scene, 'duration': 5})
            current_scene = line
        else:
            current_scene += " " + line if current_scene else line
    
    if current_scene:
        scenes.append({'text': current_scene, 'duration': 5})
    
    # If no scenes found, create scenes from sentences
    if not scenes:
        sentences = script_text.split('. ')
        scenes = [{'text': sent.strip() + '.', 'duration': 5} for sent in sentences if sent.strip()]
    
    return scenes[:10]  # Limit to 10 scenes

async def search_stock_footage(query: str, count: int = 5) -> list:
    """Search for stock videos/images from Pexels"""
    pexels_api_key = os.getenv('PEXELS_API_KEY')
    
    if not pexels_api_key or pexels_api_key == 'your_pexels_api_key_here':
        # Return placeholder images if no API key
        return [
            {
                'type': 'image',
                'url': 'https://images.unsplash.com/photo-1559860199-52dc7841bf5c',
                'thumbnail': 'https://images.unsplash.com/photo-1559860199-52dc7841bf5c?w=400',
                'source': 'unsplash'
            }
            for _ in range(count)
        ]
    
    try:
        # Search for videos
        headers = {'Authorization': pexels_api_key}
        response = requests.get(
            f'https://api.pexels.com/videos/search',
            headers=headers,
            params={'query': query, 'per_page': count}
        )
        
        if response.status_code == 200:
            data = response.json()
            videos = []
            
            for video in data.get('videos', [])[:count]:
                video_files = video.get('video_files', [])
                if video_files:
                    videos.append({
                        'type': 'video',
                        'url': video_files[0]['link'],
                        'thumbnail': video.get('image'),
                        'source': 'pexels'
                    })
            
            return videos
        
    except Exception as e:
        print(f"Error fetching stock footage: {e}")
    
    # Fallback to placeholder
    return [{
        'type': 'image',
        'url': 'https://images.unsplash.com/photo-1559860199-52dc7841bf5c',
        'thumbnail': 'https://images.unsplash.com/photo-1559860199-52dc7841bf5c?w=400',
        'source': 'unsplash'
    }]

async def generate_voiceover(text: str, voice: str = "alloy") -> dict:
    \"\"\"Generate AI voiceover using OpenAI TTS\"\"\"
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,  # alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        
        # Save audio file
        audio_filename = f"voiceover_{hash(text)}.mp3"
        audio_path = f"/tmp/{audio_filename}"
        
        response.stream_to_file(audio_path)
        
        return {
            'success': True,
            'audio_path': audio_path,
            'filename': audio_filename
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
