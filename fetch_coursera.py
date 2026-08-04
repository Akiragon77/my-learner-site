import requests
import json

def fetch_top_ai_courses():
    url = "https://api.coursera.org/api/courses.v1"
    params = {
        "q": "search",
        "query": "AI",
        "fields": "name,ratings,slug",
        "limit": 50
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    courses = []
    for item in data.get("elements", []):
        ratings = item.get("ratings", {})
        avg_rating = ratings.get("averageFiveStarRating", 0)
        rating_count = ratings.get("ratingCount", 0)
        slug = item.get("slug")
        
        if avg_rating and slug:
            courses.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "rating": round(avg_rating, 2),
                "review_count": rating_count,
                # Force English locale in the URL
                "url": f"https://www.coursera.org/learn/{slug}?lang=en"
            })
    
    # Sort by rating (highest first) and take top 5
    top5 = sorted(courses, key=lambda x: x["rating"], reverse=True)[:5]
    
    # Save to JSON
    with open("ai_top5_courses.json", "w", encoding="utf-8") as f:
        json.dump(top5, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_top_ai_courses()
