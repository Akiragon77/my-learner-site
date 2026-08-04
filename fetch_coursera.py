import requests
import json
import sys

def fetch_top_ai_courses():
    url = "https://api.coursera.org/api/courses.v1"
    
    params = {
        "q": "search",
        "query": "Artificial Intelligence",
        "limit": 20
    }
    
    # APIブロックを回避するため、一般的なブラウザのUser-Agentを設定
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Fetching real-time data from Coursera API...")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data from Coursera API: {e}")
        # API取得失敗時に空のファイルで上書きして事故るのを防ぐ
        sys.exit(1)
    
    elements = data.get("elements", [])
    print(f"API returned {len(elements)} raw elements.")

    courses = []
    for item in elements:
        name = item.get("name")
        slug = item.get("slug")
        course_id = item.get("id")
        
        if name and slug:
            courses.append({
                "id": course_id,
                "name": name,
                "url": f"https://www.coursera.org/learn/{slug}?lang=en"
            })

    top5 = courses[:5]
    print(f"Extracted Top 5 courses: {top5}")

    # 万が一抽出結果が0件だった場合はエラー終了にして空ファイルの保存を防ぐ
    if not top5:
        print("Error: No valid courses were extracted from the response.")
        sys.exit(1)

    # JSONファイルへの書き込み
    with open("ai_top5_courses.json", "w", encoding="utf-8") as f:
        json.dump(top5, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved {len(top5)} real-time courses to ai_top5_courses.json")

if __name__ == "__main__":
    fetch_top_ai_courses()