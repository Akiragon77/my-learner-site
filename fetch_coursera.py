import requests
import json
import sys

def get_course_rating(course_id, headers):
    """
    Courseraの評価専用API (courseRatings.v2) を叩いて公式の平均評価を取得する
    """
    rating_url = f"https://api.coursera.org/api/courseRatings.v2?q=course&courseId={course_id}"
    try:
        res = requests.get(rating_url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            elements = data.get("elements", [])
            if elements:
                # APIから平均評価(averageRating)を取得して小数第1位に四捨五入 (例: 4.843 -> 4.8)
                avg_rating = elements[0].get("averageRating")
                if avg_rating:
                    return f"{avg_rating:.1f}"
    except Exception as e:
        print(f"      Failed to fetch rating for {course_id}: {e}")
    
    return None

def fetch_top_ai_courses():
    url = "https://api.coursera.org/api/courses.v1"
    
    # 世界的に高評価・大人気の定番AIコース5選のslug
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
    
    courses = []
    
    print("Fetching verified top-rated AI courses & official ratings from Coursera API...")
    for slug in target_slugs:
        try:
            # 1. コース基本情報とIDを取得
            res = requests.get(f"{url}?slug={slug}&fields=name,slug,workload", headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                elements = data.get("elements", [])
                if elements:
                    item = elements[0]
                    course_id = item.get("id")
                    
                    # 2. 取得したIDを使って評価専用APIからリアルタイム評価を取得
                    rating = get_course_rating(course_id, headers)
                    
                    course_data = {
                        "id": course_id,
                        "name": item.get("name"),
                        "url": f"https://www.coursera.org/learn/{slug}?lang=en"
                    }
                    
                    if item.get("workload"):
                        course_data["workload"] = item.get("workload")
                    if rating:
                        course_data["rating"] = rating  # 公式APIから取れた数値 (例: "4.8")
                        
                    courses.append(course_data)
                    print(f"  --> Loaded: {item.get('name')} (Rating: {rating})")
        except Exception as e:
            print(f"Failed to fetch {slug}: {e}")

    print(f"Successfully retrieved {len(courses)} courses with official ratings.")

    if not courses:
        print("Error: Could not retrieve course data.")
        sys.exit(1)

    # JSONファイルへの書き込み
    with open("ai_top5_courses.json", "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    print("Saved to ai_top5_courses.json!")

if __name__ == "__main__":
    fetch_top_ai_courses()