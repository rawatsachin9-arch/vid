import os
import json
import base64
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class AIVideoService:
    def __init__(self):
        self.emergent_key = os.getenv("EMERGENT_LLM_KEY", "")
        self.client = OpenAI(api_key=self.emergent_key)
    
    async def generate_script_scenes(self, input_text: str, num_scenes: int = 5) -> List[Dict]:
        """
        Generate video scenes from input text using GPT-4o
        """
        prompt = f"""
        Convert the following text into {num_scenes} engaging video scenes. For each scene, provide:
        1. scene_number (1 to {num_scenes})
        2. description (brief visual description, 1-2 sentences)
        3. narration (what will be spoken, engaging and natural)
        4. image_prompt (detailed prompt for AI image generation, focus on visual elements, style, composition)
        5. duration (recommended duration in seconds, typically 5-8 seconds)
        
        Input text:
        {input_text}
        
        Return ONLY a valid JSON array with this exact structure:
        [
            {{
                "scene_number": 1,
                "description": "...",
                "narration": "...",
                "image_prompt": "...",
                "duration": 5
            }}
        ]
        
        Make the scenes flow naturally and tell a cohesive story. Each scene should be visually distinct.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert video script writer and scene designer. You break down text into engaging visual scenes perfect for video creation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        response_text = response.choices[0].message.content
        
        # Parse the JSON response
        try:
            # Extract JSON from the response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            scenes = json.loads(response_text)
            return scenes
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {response_text}")
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
    
    async def generate_image_for_scene(self, image_prompt: str) -> str:
        """
        Generate an image for a scene using gpt-image-1
        Returns base64-encoded image data URL
        """
        try:
            response = self.client.images.generate(
                model="gpt-image-1",
                prompt=image_prompt,
                size="1024x1024",
                n=1,
                response_format="b64_json"
            )
            
            # Get base64 image data
            b64_json = response.data[0].b64_json
            # Convert to data URL format
            image_data_url = f"data:image/png;base64,{b64_json}"
            return image_data_url
        except Exception as e:
            print(f"Error generating image: {e}")
            # Return a placeholder image if generation fails
            return "https://via.placeholder.com/1024x1024/cccccc/666666?text=Image+Generation+Failed"
    
    async def generate_all_scene_images(self, scenes: List[Dict]) -> List[Dict]:
        """
        Generate images for all scenes
        """
        for scene in scenes:
            try:
                print(f"Generating image for scene {scene['scene_number']}...")
                image_url = await self.generate_image_for_scene(scene['image_prompt'])
                scene['image_url'] = image_url
            except Exception as e:
                print(f"Failed to generate image for scene {scene['scene_number']}: {e}")
                scene['image_url'] = None
        
        return scenes
