import requests
import pandas as pd
import matplotlib.pyplot as plt

# used random users api
API_URL = "https://randomuser.me/api/?results=10"

try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit()

# formatting data in required shape
users = data.get("results", [])
students = []
for idx, user in enumerate(users):
    students.append({
        "name": f"{user['name']['first']} {user['name']['last']}",
        "score": 60 + (idx * 3) % 40
    })

# pandas dataframe 
df = pd.DataFrame(students)

# getavg score
average_score = df["score"].mean()
print(f"Average Score: {average_score:.2f}")
print(f"Total students processed: {len(df)}")

# visualizational thing matplot
plt.figure(figsize=(12, 6))
plt.bar(df["name"], df["score"], color="steelblue")
plt.xlabel("Student Name")
plt.ylabel("Score")
plt.title("Student Scores")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
