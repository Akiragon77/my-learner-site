import requests
import json
import sys

def get_course_rating(course_id, headers):
    """Courseraの評価専用API (courseRatings.v2) から公式の平均評価を取得"""
    rating_url = f"https://api.coursera.org/api/courseRatings.v2?q=course&courseId={course_id}"
    try:
        res = requests.get(rating_url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            elements = data.get("elements", [])
            if elements:
                avg_rating = elements[0].get("averageRating")
                if avg_rating:
                    return f"{avg_rating:.1f}"
    except Exception as e:
        print(f"      Failed to fetch rating for {course_id}: {e}")
    return None

def fetch_top_ai_courses():
    url = "https://api.coursera.org/api/courses.v1"
    
    # 定番・超高評価のAIコース5選のslug
    target_slugs = [
        "ai-for-everyone",
        "machine-learning",
        "neural-networks-deep-learning",
        "generative-ai-for-everyone",
        "introduction-to-ai"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # 確実に異なるデータを集めるため、APIから一覧を取得してマッピングする
    print("Fetching courses list from Coursera API...")
    try:
        res = requests.get(f"{url}?limit=100&fields=name,slug", headers=headers, timeout=15)
        res.raise_for_status()
        all_elements = res.json().get("elements", [])
    except Exception as e:
        print(f"Error fetching base course list: {e}")
        sys.exit(1)

    # slug をキーにした辞書を作成
    slug_map = {item.get("slug"): item for item in all_elements if item.get("slug")}

    courses = []
    print("Extracting target courses and ratings...")

    for slug in target_slugs:
        item = slug_map.get(slug)
        if item:
            course_id = item.get("id")
            course_name = item.get("name")
            
            # 公式評価の取得
            rating = get_course_rating(course_id, headers)
            
            course_data = {
                "id": course_id,
                "name": course_name,
                "url": f"https://www.coursera.org/learn/{slug}?lang=en"
            }
            if rating:
                course_data["rating"] = rating
                
            courses.append(course_data)
            print(f"  --> Loaded: {course_name} (Rating: {rating})")
        else:
            print(f"  --> Warning: Slug '{slug}' not found in API response.")

    print(f"Successfully retrieved {len(courses)} courses.")

    if not courses:
        print("Error: Could not retrieve course data.")
        sys.exit(1)

    with open("ai_top5_courses.json", "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    print("Saved to ai_top5_courses.json!")

if __name__ == "__main__":
    fetch_top_ai_courses()