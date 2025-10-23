import os
import json
import base64
from typing import List, Dict
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
from emergentintegrations.llm.openai.image_generation import OpenAIImageGeneration

load_dotenv()

class AIVideoService:
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY", "")
        self.llm_chat = LlmChat(
            api_key=self.api_key,
            session_id="video_generation",
            system_message="You are an expert video script writer and scene designer. You break down text into engaging visual scenes perfect for video creation."
        ).with_model("openai", "gpt-4o")
        
        self.image_gen = OpenAIImageGeneration(api_key=self.api_key)
    
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
        
        user_message = UserMessage(text=prompt)
        response = await self.llm_chat.send_message(user_message)
        
        # Parse the JSON response
        try:
            # Extract JSON from the response (handle markdown code blocks)
            response_text = response.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            scenes = json.loads(response_text)
            return scenes
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {response}")
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
    
    async def generate_image_for_scene(self, image_prompt: str) -> str:
        """
        Generate an image for a scene using gpt-image-1
        Returns base64 encoded image
        """
        try:
            images = await self.image_gen.generate_images(
                prompt=image_prompt,
                model="gpt-image-1",
                number_of_images=1
            )
            
            if images and len(images) > 0:
                # Convert to base64
                image_base64 = base64.b64encode(images[0]).decode('utf-8')
                return f"data:image/png;base64,{image_base64}"
            else:
                raise Exception("No image was generated")
        except Exception as e:
            print(f"Error generating image: {e}")
            raise
    
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
