import requests
import json
import sys

def fetch_top_ai_courses():
    url = "https://api.coursera.org/api/courses.v1"
    
    # APIから取得可能なフィールド（名前、slug、想定学習時間）を要求
    params = {
        "limit": 100,
        "fields": "name,slug,workload"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Fetching courses from Coursera API...")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data from Coursera API: {e}")
        sys.exit(1)
        
    elements = data.get("elements", [])
    print(f"Retrieved {len(elements)} raw courses.")

    ai_keywords = ["ai", "artificial intelligence", "machine learning", "deep learning", "generative ai"]
    seen_ids = set()
    courses = []

    for item in elements:
        course_id = item.get("id")
        name = item.get("name", "")
        slug = item.get("slug", "")
        # APIメタデータから workload (想定学習時間) を取得
        workload = item.get("workload")
        
        if course_id and course_id not in seen_ids and name and slug:
            name_lower = name.lower()
            if any(kw in name_lower for kw in ai_keywords):
                seen_ids.add(course_id)
                
                # APIメタデータに存在する値のみを保持
                course_data = {
                    "id": course_id,
                    "name": name,
                    "url": f"https://www.coursera.org/learn/{slug}?lang=en"
                }
                if workload:
                    course_data["workload"] = workload

                courses.append(course_data)
                
                if len(courses) == 5:
                    break

    print(f"Extracted {len(courses)} AI courses.")

    if not courses:
        print("Error: No matching AI courses found.")
        sys.exit(1)

    with open("ai_top5_courses.json", "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    print("Successfully updated ai_top5_courses.json!")

if __name__ == "__main__":
    fetch_top_ai_courses()