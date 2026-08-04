import requests
import json
import sys

def fetch_top_ai_courses():
    # Courseraの公開API（q=search ではなく直接コース一覧を取得してフィルタリング）
    url = "https://api.coursera.org/api/courses.v1"
    
    # AIに関連する主要なコース slug の一覧
    target_slugs = [
        "ai-for-everyone",
        "machine-learning",
        "neural-networks-deep-learning",
        "generative-ai-for-everyone",
        "introduction-to-ai"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    courses = []
    
    print("Fetching specific AI course details from Coursera API...")
    for slug in target_slugs:
        try:
            # slug 指定で個別APIを叩く（非常に安定して取得可能）
            res = requests.get(f"{url}?slug={slug}&fields=name,slug", headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                elements = data.get("elements", [])
                if elements:
                    item = elements[0]
                    courses.append({
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "url": f"https://www.coursera.org/learn/{slug}?lang=en"
                    })
        except Exception as e:
            print(f"Failed to fetch {slug}: {e}")

    print(f"Successfully retrieved {len(courses)} courses.")

    if not courses:
        print("Error: Could not retrieve any course data.")
        sys.exit(1)

    # JSONファイルへの書き込み
    with open("ai_top5_courses.json", "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

    print("Saved data to ai_top5_courses.json")

if __name__ == "__main__":
    fetch_top_ai_courses()