import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from typing import Dict, List

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-1.5-flash"

def analyze_tasks_with_budget(task: str, departments: List[str], currency: str = "INR") -> Dict:
    """Enhanced to include budget estimation"""
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = f"""
    You are an expert project manager with financial expertise. For this task:
    1. Break into subtasks if needed
    2. Assign to departments: {", ".join(departments)}
    3. Estimate costs in {currency}
    
    Return ONLY JSON with this improved structure:
    {{
        "main_task": "original description",
        "currency": "{currency}",
        "assignments": [
            {{
                "subtask": "description",
                "department": "dept_name",
                "instructions": "specific actions",
                "estimated_time": "hours/days",
                "estimated_budget": {{
                    "amount": 100,
                    "breakdown": {{
                        "category1": 50,
                        "category2": 50
                    }},
                    "currency": "{currency}"
                }}
            }}
        ],
        "total_budget": {{
            "amount": 500,
            "breakdown": {{
                "department1": 200,
                "department2": 300
            }}
        }}
    }}
    
    Now process: "{task}"
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,  # More precise for financial estimates
                "max_output_tokens": 2500
            }
        )
        
        # Extract and validate JSON
        json_str = response.text[response.text.find('{'):response.text.rfind('}')+1]
        result = json.loads(json_str)
        
        # Validate and calculate total if not provided
        if "total_budget" not in result:
            total = sum(a["estimated_budget"]["amount"] for a in result["assignments"])
            result["total_budget"] = {
                "amount": total,
                "breakdown": "Auto-calculated from subtasks"
            }
        
        return result
        
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}", "raw_response": response.text if 'response' in locals() else None}