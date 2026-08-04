import requests
import json
import sys

def get_course_rating(course_id, headers):
    """Courseraの評価専用API (courseRatings.v2) から公式の平均評価(数値)を取得"""
    rating_url = f"https://api.coursera.org/api/courseRatings.v2?q=course&courseId={course_id}"
    try:
        res = requests.get(rating_url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            elements = data.get("elements", [])
            if elements:
                avg_rating = elements[0].get("averageRating")
                if avg_rating is not None:
                    return float(avg_rating)
    except Exception:
        pass
    return None

def fetch_top_ai_courses():
    url = "https://api.coursera.org/api/courses.v1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("Fetching AI courses list from Coursera API...")
    
    # AIに関連する検索クエリでAPIを呼び出す
    try:
        res = requests.get(f"{url}?q=search&query=Artificial%20Intelligence&limit=50&fields=name,slug", headers=headers, timeout=15)
        if res.status_code != 200:
            # searchクエリが使えない場合のフォールバック（一覧取得）
            res = requests.get(f"{url}?limit=100&fields=name,slug", headers=headers, timeout=15)
        
        res.raise_for_status()
        all_courses = res.json().get("elements", [])
    except Exception as e:
        print(f"Failed to fetch courses: {e}")
        sys.exit(1)

    print(f"Retrieved {len(all_courses)} candidate courses. Evaluating ratings...")

    ai_keywords = ["ai", "artificial intelligence", "machine learning", "deep learning", "generative ai"]
    evaluated_courses = []
    seen_names = set()

    # 取得したコースを1件ずつ検証
    for course in all_courses:
        course_id = course.get("id")
        name = course.get("name", "")
        slug = course.get("slug", "")
        name_lower = name.lower()

        # 重複チェック ＆ AIキーワードが含まれているか判定
        if name_lower in seen_names:
            continue
        if not any(kw in name_lower for kw in ai_keywords):
            continue

        # 評価（Rating）を取得
        rating = get_course_rating(course_id, headers)
        
        # 評価が取得でき、かつ高評価（4.0以上）のものだけエントリー
        if rating and rating >= 4.0:
            seen_names.add(name_lower)
            evaluated_courses.append({
                "id": course_id,
                "name": name,
                "rating_val": rating,
                "rating": f"{rating:.1f}",
                "url": f"https://www.coursera.org/learn/{slug}?lang=en"
            })
            print(f"  [Match] {name} (Rating: {rating:.1f})")

    # 評価（rating_val）が高い順にソート（並び替え）
    evaluated_courses.sort(key=lambda x: x["rating_val"], reverse=0 == 0) # 降順ソート
    evaluated_courses.sort(key=lambda x: x["rating_val"], reverse=True)

    # 上位5件を抽出
    top5_courses = evaluated_courses[:5]

    # 不要なソート用キーを削除
    for item in top5_courses:
        del item["rating_val"]

    print(f"\nSuccessfully selected TOP {len(top5_courses)} rated AI courses.")

    if not top5_courses:
        print("Warning: No matching rated courses found.")
        sys.exit(1)

    # JSONへ書き出し
    with open("ai_top5_courses.json", "w", encoding="utf-8") as f:
        json.dump(top5_courses, f, ensure_ascii=False, indent=2)

    print("Saved automatically generated top courses to ai_top5_courses.json!")

if __name__ == "__main__":
    fetch_top_ai_courses()