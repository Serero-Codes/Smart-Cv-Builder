import os
import json
from groq import Groq

def process_form_data(data):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    company = data.get('target_company', 'Tech Industry')

    prompt = f"""
    You are an elite Executive Resume Writer. The user has provided raw, brief CV data. 
    Your job is to EXPAND this data into a highly professional, page-filling, ATS-optimized CV tailored for {company}.
    
    Rules for Expansion:
    1. Summary: Make it a powerful 3-4 sentence paragraph highlighting senior-level impact.
    2. Experience & Projects: Transform brief descriptions into 3-4 highly detailed bullet points per role. 
       Use the Harvard format: Action Verb + Task + Result/Metric (invent realistic metrics if none provided, e.g., "improved efficiency by 30%").
    
    Raw Data:
    {json.dumps(data, indent=2)}
    
    Output ONLY a valid JSON object matching this EXACT schema:
    {{
      "name": "string",
      "email": "string",
      "phone": "string",
      "links": "string",
      "summary": "string",
      "skills": "string (grouped like 'Languages: X | Frameworks: Y')",
      "experience": [
        {{ "role": "string", "company": "string", "duration": "string", "bullets": ["string", "string", "string"] }}
      ],
      "projects": [
        {{ "name": "string", "tech": "string", "bullets": ["string", "string"] }}
      ],
      "education": [
        {{ "degree": "string", "school": "string", "year": "string" }}
      ]
    }}
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.4,
        response_format={"type": "json_object"}
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print("JSON Parse Error:", e)
        return data