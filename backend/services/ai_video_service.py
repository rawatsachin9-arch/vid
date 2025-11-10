import os
import json
import base64
import httpx
import uuid
from typing import List, Dict
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Try to set litellm drop_params if available
try:
    import litellm
    litellm.drop_params = True
except:
    pass

load_dotenv()

class AIVideoService:
    def __init__(self):
        # Use Emergent LLM Key for both text and image generation
        self.api_key = os.getenv("EMERGENT_LLM_KEY", "")
        # Emergent proxy URL for image generation
        self.emergent_image_url = "https://integrations.emergentagent.com/llm/images/generations"
    
    async def generate_script_scenes(self, input_text: str, num_scenes: int = 5) -> List[Dict]:
        """
        Generate video scenes from input text using GPT-4o via Emergent LLM Key
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
        
        # Initialize chat with system message
        chat = LlmChat(
            api_key=self.api_key,
            session_id="video_script_generation",
            system_message="You are an expert video script writer and scene designer. You break down text into engaging visual scenes perfect for video creation."
        ).with_model("openai", "gpt-4o")
        
        # Send message
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        response_text = response.text if hasattr(response, 'text') else str(response)
        
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
        Generate an image for a scene using gpt-image-1 via Emergent LLM Key
        Returns image URL directly (not base64 to avoid MongoDB 16MB document limit)
        
        Calls Emergent API directly and returns the hosted image URL
        """
        try:
            # Call the Emergent image generation API directly
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.emergent_image_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-image-1",
                        "prompt": image_prompt,
                        "n": 1,
                        "quality": "low"
                        # Note: response_format not supported by Emergent API for gpt-image-1
                    }
                )
                
                if response.status_code != 200:
                    print(f"Image generation API error: {response.status_code} - {response.text}")
                    return "https://via.placeholder.com/1024x1024/cccccc/666666?text=Image+Generation+Failed"
                
                result = response.json()
                
                # The API returns: {"data": [{"url": "..."}, ...]}
                if "data" in result and len(result["data"]) > 0:
                    image_data = result["data"][0]
                    
                    # Check if we have a URL - USE IT DIRECTLY (don't convert to base64 to avoid MongoDB 16MB limit)
                    if "url" in image_data and image_data["url"]:
                        image_url = image_data["url"]
                        print(f"✅ Image generated successfully: {image_url[:100]}...")
                        return image_url  # Return URL directly instead of converting to base64
                    
                    # Handle b64_json format - save to file and return URL to avoid MongoDB 16MB limit
                    elif "b64_json" in image_data and image_data["b64_json"]:
                        b64_data = image_data["b64_json"]
                        print(f"✅ Image generated successfully (base64 format - {len(b64_data)} chars)")
                        
                        try:
                            # Save base64 image to a file and return URL
                            image_url = await self._save_base64_image_to_file(b64_data)
                            print(f"✅ Image saved to file: {image_url}")
                            return image_url
                        except Exception as e:
                            print(f"❌ Failed to save image to file: {e}")
                            return "https://via.placeholder.com/1024x1024/cccccc/666666?text=File+Save+Failed"
                    else:
                        print(f"Unexpected response format: {list(image_data.keys())}")
                        return "https://via.placeholder.com/1024x1024/cccccc/666666?text=Unexpected+Format"
                else:
                    print(f"No image data in response: {result}")
                    return "https://via.placeholder.com/1024x1024/cccccc/666666?text=No+Image+Data"
                    
        except httpx.TimeoutException:
            print(f"Timeout generating image for prompt: {image_prompt[:100]}")
            return "https://via.placeholder.com/1024x1024/cccccc/666666?text=Timeout"
        except Exception as e:
            print(f"Error generating image: {e}")
            import traceback
            traceback.print_exc()
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

    async def _save_base64_image_to_file(self, b64_data: str) -> str:
        """
        Save base64 image data to a file and return the URL
        This avoids storing large base64 data in MongoDB (16MB limit)
        """
        try:
            # Create images directory if it doesn't exist
            images_dir = "/app/backend/static/images"
            os.makedirs(images_dir, exist_ok=True)
            
            # Generate unique filename
            image_id = str(uuid.uuid4())
            filename = f"{image_id}.png"
            filepath = os.path.join(images_dir, filename)
            
            # Decode base64 and save to file
            image_bytes = base64.b64decode(b64_data)
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            
            # Return URL to the saved image
            # Use the backend URL to serve the static file
            backend_url = os.getenv("BACKEND_URL", "https://c-project-4.preview.emergentagent.com")
            image_url = f"{backend_url}/static/images/{filename}"
            
            return image_url
            
        except Exception as e:
            print(f"Error saving base64 image to file: {e}")
            raise