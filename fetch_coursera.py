import requests
import json
import sys

def get_course_rating(course_id, headers):
    """
    Courseraの評価専用API (courseRatings.v2) から公式の平均評価を取得
    """
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
    
    # 対象コースのslugリスト
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
    
    print("Fetching verified top-rated AI courses & official ratings from Coursera API...")
    
    # slugをカンマ区切りで指定して一括取得
    slugs_param = ",".join(target_slugs)
    request_url = f"{url}?q=slugs&slugs={slugs_param}&fields=name,slug,workload"
    
    courses_map = {}
    
    try:
        res = requests.get(request_url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            elements = data.get("elements", [])
            for item in elements:
                item_slug = item.get("slug")
                if item_slug in target_slugs:
                    courses_map[item_slug] = item
        else:
            print(f"API Request failed with status code: {res.status_code}")
    except Exception as e:
        print(f"Failed to fetch course list: {e}")

    courses = []
    
    # 元の target_slugs の順序を保持して処理
    for slug in target_slugs:
        item = courses_map.get(slug)
        if not item:
            print(f"  --> Warning: Could not find course data for slug: {slug}")
            continue
            
        course_id = item.get("id")
        course_name = item.get("name")
        
        # 評価を取得
        rating = get_course_rating(course_id, headers)
        
        course_data = {
            "id": course_id,
            "name": course_name,
            "url": f"https://www.coursera.org/learn/{slug}?lang=en"
        }
        
        if item.get("workload"):
            course_data["workload"] = item.get("workload")
        if rating:
            course_data["rating"] = rating
            
        courses.append(course_data)
        print(f"  --> Loaded: {course_name} (Rating: {rating})")

    print(f"Successfully retrieved {len(courses)} courses with official ratings.")

    if not courses:
        print("Error: Could not retrieve course data.")
        sys.exit(1)

    # JSONファイルへの保存
    with open("ai_top5_courses.json", "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    print("Saved to ai_top5_courses.json!")

if __name__ == "__main__":
    fetch_top_ai_courses()