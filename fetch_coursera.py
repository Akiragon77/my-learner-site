import requests
import json

def fetch_top_ai_courses():
    # Coursera公式の検索API
    url = "https://api.coursera.org/api/courses.v1"
    
    params = {
        "q": "search",
        "query": "Artificial Intelligence",
        "limit": 20
    }
    
    print("Fetching real-time data from Coursera API...")
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    elements = data.get("elements", [])
    print(f"API returned {len(elements)} courses.")

    courses = []
    for item in elements:
        name = item.get("name")
        slug = item.get("slug")
        course_id = item.get("id")
        
        if name and slug:
            # 安定してアクセスできる英語の受講URLを生成
            courses.append({
                "id": course_id,
                "name": name,
                "url": f"https://www.coursera.org/learn/{slug}?lang=en"
            })

    # 取得した結果から最新の上位5件を抽出
    top5 = courses[:5]

    # JSONファイルへの書き込み
    with open("ai_top5_courses.json", "w", encoding="utf-8") as f:
        json.dump(top5, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved {len(top5)} real-time courses to ai_top5_courses.json")

if __name__ == "__main__":
    fetch_top_ai_courses()