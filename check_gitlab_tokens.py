# import requests
# import datetime
# import os

# # Настройки GitLab
# GITLAB_API_URL = os.environ.get("GITLAB_API_URL", "http://192.168.64.6/api/v4")
# GITLAB_ADMIN_TOKEN = os.environ.get("GITLAB_ADMIN_TOKEN")
# DAYS_BEFORE_EXPIRY = int(os.environ.get("DAYS_BEFORE_EXPIRY", "7"))

# def check_tokens():
#     headers = {"PRIVATE-TOKEN": GITLAB_ADMIN_TOKEN}
#     expiring_tokens = []
#     page = 1

#     while True:
#         url = f"{GITLAB_API_URL}/personal_access_tokens?per_page=100&page={page}"
#         resp = requests.get(url, headers=headers)

#         if resp.status_code != 200:
#             print(f"Ошибка при получении токенов: {resp.text}")
#             break

#         tokens = resp.json()
#         if not tokens:
#             break

#         for token in tokens:
#             if token["revoked"] or not token["active"]:
#                 continue

#             expires_at = token.get("expires_at")
#             if expires_at:
#                 expiry_date = datetime.datetime.strptime(expires_at, "%Y-%m-%d")
#                 days_left = (expiry_date - datetime.datetime.utcnow()).days

#                 if days_left <= DAYS_BEFORE_EXPIRY:
#                     expiring_tokens.append({
#                         "name": token["name"],
#                         "username": token["user"]["username"],
#                         "expires_at": expires_at,
#                         "days_left": days_left
#                     })

#         page += 1

#     if expiring_tokens:
#         print("⚠️  Токены, срок действия которых скоро истечет:")
#         for t in expiring_tokens:
#             print(f"- {t['username']}: {t['name']} (истекает через {t['days_left']} дней — {t['expires_at']})")
#     else:
#         print("✅ Все токены действительны.")

# if __name__ == "__main__":
#     check_tokens()
#############################
# import requests
# import datetime
# import os

# # Настройки GitLab
# GITLAB_API_URL = os.environ.get("GITLAB_API_URL", "http://192.168.64.6/api/v4")
# GITLAB_ADMIN_TOKEN = os.environ.get("GITLAB_ADMIN_TOKEN")
# DAYS_BEFORE_EXPIRY = int(os.environ.get("DAYS_BEFORE_EXPIRY", "7"))

# HEADERS = {"PRIVATE-TOKEN": GITLAB_ADMIN_TOKEN}


# def print_token_status(entity, token_name, expires_at, status_label):
#     print(f"🔐 Объект: {entity}")
#     print(f"🔑 Токен: {token_name}")
#     print(f"📅 Срок действия: {expires_at}")
#     print(f"📌 Статус: {status_label}")
#     print("-" * 60)


# def check_personal_tokens():
#     print("\n=== Personal Access Tokens ===\n")
#     page = 1
#     while True:
#         url = f"{GITLAB_API_URL}/personal_access_tokens?per_page=100&page={page}"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения: {e}")
#             break

#         if resp.status_code != 200:
#             print(f"Ошибка при получении токенов: {resp.text}")
#             break

#         tokens = resp.json()
#         if not tokens:
#             break

#         for token in tokens:
#             user = token.get("user")
#             if not user:
#                 entity = "(неизвестный пользователь)"
#             else:
#                 entity = f"{user['username']} <{user.get('email', 'без email')}>"

#             token_name = token.get("name", "(без имени)")
#             expires_at = token.get("expires_at", "∞")
#             status = "✅ Активен"

#             if token.get("revoked"):
#                 status = "❌ Отозван"
#             elif not token.get("active", True):
#                 status = "❌ Неактивен"
#             elif expires_at != "∞":
#                 expiry_date = datetime.datetime.strptime(expires_at, "%Y-%m-%d")
#                 days_left = (expiry_date - datetime.datetime.utcnow()).days
#                 if days_left < 0:
#                     status = f"❌ Истёк ({expires_at})"
#                 elif days_left <= DAYS_BEFORE_EXPIRY:
#                     status = f"⚠️ Истекает через {days_left} дней ({expires_at})"

#             print_token_status(entity, token_name, expires_at, status)

#         page += 1


# def get_all_projects():
#     projects = []
#     page = 1
#     while True:
#         url = f"{GITLAB_API_URL}/projects?per_page=100&page={page}"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения к проектам: {e}")
#             break

#         if resp.status_code != 200:
#             print(f"Ошибка при получении проектов: {resp.text}")
#             break
#         data = resp.json()
#         if not data:
#             break
#         projects.extend(data)
#         page += 1
#     return projects


# def check_project_tokens():
#     print("\n=== Project Access Tokens ===\n")
#     projects = get_all_projects()
#     for project in projects:
#         project_id = project["id"]
#         project_name = project["name_with_namespace"]
#         url = f"{GITLAB_API_URL}/projects/{project_id}/access_tokens"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения к токенам проекта {project_name}: {e}")
#             continue

#         if resp.status_code != 200:
#             continue
#         tokens = resp.json()
#         for token in tokens:
#             token_name = token["name"]
#             expires_at = token.get("expires_at", "∞")
#             status = "✅ Активен"

#             if expires_at != "∞":
#                 expiry_date = datetime.datetime.strptime(expires_at, "%Y-%m-%d")
#                 days_left = (expiry_date - datetime.datetime.utcnow()).days
#                 if days_left < 0:
#                     status = f"❌ Истёк ({expires_at})"
#                 elif days_left <= DAYS_BEFORE_EXPIRY:
#                     status = f"⚠️ Истекает через {days_left} дней ({expires_at})"

#             print_token_status(f"Проект: {project_name}", token_name, expires_at, status)


# def get_all_groups():
#     groups = []
#     page = 1
#     while True:
#         url = f"{GITLAB_API_URL}/groups?per_page=100&page={page}"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения к группам: {e}")
#             break

#         if resp.status_code != 200:
#             print(f"Ошибка при получении групп: {resp.text}")
#             break
#         data = resp.json()
#         if not data:
#             break
#         groups.extend(data)
#         page += 1
#     return groups


# def check_group_tokens():
#     print("\n=== Group Access Tokens ===\n")
#     groups = get_all_groups()
#     for group in groups:
#         group_id = group["id"]
#         group_name = group["full_path"]
#         url = f"{GITLAB_API_URL}/groups/{group_id}/access_tokens"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения к токенам группы {group_name}: {e}")
#             continue

#         if resp.status_code != 200:
#             continue
#         tokens = resp.json()
#         for token in tokens:
#             token_name = token["name"]
#             expires_at = token.get("expires_at", "∞")
#             status = "✅ Активен"

#             if expires_at != "∞":
#                 expiry_date = datetime.datetime.strptime(expires_at, "%Y-%m-%d")
#                 days_left = (expiry_date - datetime.datetime.utcnow()).days
#                 if days_left < 0:
#                     status = f"❌ Истёк ({expires_at})"
#                 elif days_left <= DAYS_BEFORE_EXPIRY:
#                     status = f"⚠️ Истекает через {days_left} дней ({expires_at})"

#             print_token_status(f"Группа: {group_name}", token_name, expires_at, status)


# def main():
#     check_personal_tokens()
#     check_project_tokens()
#     check_group_tokens()


# if __name__ == "__main__":
#     main()
###############################
# import requests
# import datetime
# import os

# # Настройки GitLab
# GITLAB_API_URL = os.environ.get("GITLAB_API_URL", "http://192.168.64.6/api/v4")
# GITLAB_ADMIN_TOKEN = os.environ.get("GITLAB_ADMIN_TOKEN")
# DAYS_BEFORE_EXPIRY = int(os.environ.get("DAYS_BEFORE_EXPIRY", "7"))

# HEADERS = {"PRIVATE-TOKEN": GITLAB_ADMIN_TOKEN}


# def print_token_details(entity, token_name, expires_at, status_label, scopes, created_at, last_used_at):
#     print(f"🔐 Объект: {entity}")
#     print(f"🔑 Токен: {token_name}")
#     print(f"📜 Scopes: {', '.join(scopes) if scopes else '(не указано)'}")
#     print(f"🗓️ Создан: {created_at}")
#     print(f"🕒 Последнее использование: {last_used_at or 'Never'}")
#     print(f"📅 Срок действия: {expires_at}")
#     print(f"📌 Статус: {status_label}")
#     print("-" * 60)


# def check_personal_tokens():
#     print("\n=== Personal Access Tokens ===\n")
#     page = 1
#     while True:
#         url = f"{GITLAB_API_URL}/personal_access_tokens?per_page=100&page={page}"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения: {e}")
#             break

#         if resp.status_code != 200:
#             print(f"Ошибка при получении токенов: {resp.text}")
#             break

#         tokens = resp.json()
#         if not tokens:
#             break

#         for token in tokens:
#             user = token.get("user")
#             entity = f"{user['username']} <{user.get('email', 'без email')}>" if user else "(неизвестный пользователь)"
#             token_name = token.get("name", "(без имени)")
#             expires_at = token.get("expires_at", "∞")
#             created_at = token.get("created_at", "—")
#             last_used_at = token.get("last_used_at", None)
#             scopes = token.get("scopes", [])
#             status = "✅ Активен"

#             if token.get("revoked"):
#                 status = "❌ Отозван"
#             elif not token.get("active", True):
#                 status = "❌ Неактивен"
#             elif expires_at != "∞":
#                 expiry_date = datetime.datetime.strptime(expires_at, "%Y-%m-%d")
#                 days_left = (expiry_date - datetime.datetime.utcnow()).days
#                 if days_left < 0:
#                     status = f"❌ Истёк ({expires_at})"
#                 elif days_left <= DAYS_BEFORE_EXPIRY:
#                     status = f"⚠️ Истекает через {days_left} дней ({expires_at})"

#             print_token_details(entity, token_name, expires_at, status, scopes, created_at, last_used_at)

#         page += 1


# def get_all_projects():
#     projects = []
#     page = 1
#     while True:
#         url = f"{GITLAB_API_URL}/projects?per_page=100&page={page}"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения к проектам: {e}")
#             break

#         if resp.status_code != 200:
#             print(f"Ошибка при получении проектов: {resp.text}")
#             break
#         data = resp.json()
#         if not data:
#             break
#         projects.extend(data)
#         page += 1
#     return projects


# def check_project_tokens():
#     print("\n=== Project Access Tokens ===\n")
#     projects = get_all_projects()
#     for project in projects:
#         project_id = project["id"]
#         project_name = project["name_with_namespace"]
#         url = f"{GITLAB_API_URL}/projects/{project_id}/access_tokens"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения к токенам проекта {project_name}: {e}")
#             continue

#         if resp.status_code != 200:
#             continue
#         tokens = resp.json()
#         for token in tokens:
#             token_name = token["name"]
#             expires_at = token.get("expires_at", "∞")
#             created_at = token.get("created_at", "—")
#             last_used_at = token.get("last_used_at", None)
#             scopes = token.get("scopes", [])

#             status = "✅ Активен"
#             if expires_at != "∞":
#                 expiry_date = datetime.datetime.strptime(expires_at, "%Y-%m-%d")
#                 days_left = (expiry_date - datetime.datetime.utcnow()).days
#                 if days_left < 0:
#                     status = f"❌ Истёк ({expires_at})"
#                 elif days_left <= DAYS_BEFORE_EXPIRY:
#                     status = f"⚠️ Истекает через {days_left} дней ({expires_at})"

#             print_token_details(f"Проект: {project_name}", token_name, expires_at, status, scopes, created_at, last_used_at)


# def get_all_groups():
#     groups = []
#     page = 1
#     while True:
#         url = f"{GITLAB_API_URL}/groups?per_page=100&page={page}"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения к группам: {e}")
#             break

#         if resp.status_code != 200:
#             print(f"Ошибка при получении групп: {resp.text}")
#             break
#         data = resp.json()
#         if not data:
#             break
#         groups.extend(data)
#         page += 1
#     return groups


# def check_group_tokens():
#     print("\n=== Group Access Tokens ===\n")
#     groups = get_all_groups()
#     for group in groups:
#         group_id = group["id"]
#         group_name = group["full_path"]
#         url = f"{GITLAB_API_URL}/groups/{group_id}/access_tokens"
#         try:
#             resp = requests.get(url, headers=HEADERS, timeout=5)
#         except Exception as e:
#             print(f"Ошибка подключения к токенам группы {group_name}: {e}")
#             continue

#         if resp.status_code != 200:
#             continue
#         tokens = resp.json()
#         for token in tokens:
#             token_name = token["name"]
#             expires_at = token.get("expires_at", "∞")
#             created_at = token.get("created_at", "—")
#             last_used_at = token.get("last_used_at", None)
#             scopes = token.get("scopes", [])

#             status = "✅ Активен"
#             if expires_at != "∞":
#                 expiry_date = datetime.datetime.strptime(expires_at, "%Y-%m-%d")
#                 days_left = (expiry_date - datetime.datetime.utcnow()).days
#                 if days_left < 0:
#                     status = f"❌ Истёк ({expires_at})"
#                 elif days_left <= DAYS_BEFORE_EXPIRY:
#                     status = f"⚠️ Истекает через {days_left} дней ({expires_at})"

#             print_token_details(f"Группа: {group_name}", token_name, expires_at, status, scopes, created_at, last_used_at)


# def main():
#     check_personal_tokens()
#     check_project_tokens()
#     check_group_tokens()


# if __name__ == "__main__":
#     main()

import requests
import datetime
import os
from zoneinfo import ZoneInfo

# Настройки
GITLAB_BASE_URL = "http://192.168.64.6"
GITLAB_API_URL = f"{GITLAB_BASE_URL}/api/v4"
GITLAB_ADMIN_TOKEN = os.environ.get("GITLAB_ADMIN_TOKEN")
HEADERS = {"PRIVATE-TOKEN": GITLAB_ADMIN_TOKEN}
EXPIRY_THRESHOLD_DAYS = 34

seen_tokens = set()

def format_expiry_datetime(date_str):
    try:
        dt_utc = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, tzinfo=datetime.timezone.utc)
        return dt_utc.strftime("⏳ Истекает: %B %d, %Y at %I:%M %p (UTC)")
    except:
        return f"⏳ Истекает: {date_str}"

def print_token(token, label=None, link=None):
    token_key = (token.get("name"), token.get("created_at"), token.get("expires_at"))
    if token_key in seen_tokens:
        return
    seen_tokens.add(token_key)

    if link and label:
        print(f"🔗 {label}: {link}")
    print(f"🔑 Токен: {token.get('name')}")
    print(f"📜 Scopes: {', '.join(token.get('scopes', [])) or '(не указано)'}")
    print(f"🗓️ Создан: {token.get('created_at', '—')}")
    print(f"🕒 Последнее использование: {token.get('last_used_at') or 'Never'}")
    print(f"📅 Срок действия: {token.get('expires_at')}")
    print(f"{format_expiry_datetime(token.get('expires_at'))}")
    print("-" * 60)

def check_expiration(expires_at):
    if not expires_at or expires_at == "∞":
        return False
    expiry_date = datetime.datetime.strptime(expires_at, "%Y-%m-%d")
    days_left = (expiry_date - datetime.datetime.utcnow()).days
    return days_left <= EXPIRY_THRESHOLD_DAYS

def check_personal_tokens():
    for page in range(1, 1000):
        url = f"{GITLAB_API_URL}/personal_access_tokens?per_page=100&page={page}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code != 200:
                break
            tokens = resp.json()
            if not tokens:
                break
            for token in tokens:
                if token.get("revoked") or not token.get("active", True):
                    continue
                if not check_expiration(token.get("expires_at")):
                    continue
                user = token.get("user")
                if user:
                    label = f"{user['username']} <{user.get('email', 'без email')}>"
                    print_token(token, label=label)
        except:
            break

def get_all_projects():
    projects = []
    for page in range(1, 1000):
        try:
            url = f"{GITLAB_API_URL}/projects?per_page=100&page={page}"
            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code != 200:
                break
            data = resp.json()
            if not data:
                break
            projects.extend(data)
        except:
            break
    return projects

def check_project_tokens():
    for project in get_all_projects():
        try:
            url = f"{GITLAB_API_URL}/projects/{project['id']}/access_tokens"
            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code != 200:
                continue
            for token in resp.json():
                if token.get("revoked") or not token.get("active", True):
                    continue
                if not check_expiration(token.get("expires_at")):
                    continue
                path = project['path_with_namespace']
                link = f"{GITLAB_BASE_URL}/{path}"
                print_token(token, label="Проект", link=link)
        except:
            continue

def get_all_groups():
    groups = []
    for page in range(1, 1000):
        try:
            url = f"{GITLAB_API_URL}/groups?per_page=100&page={page}"
            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code != 200:
                break
            data = resp.json()
            if not data:
                break
            groups.extend(data)
        except:
            break
    return groups

def check_group_tokens():
    for group in get_all_groups():
        try:
            url = f"{GITLAB_API_URL}/groups/{group['id']}/access_tokens"
            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code != 200:
                continue
            for token in resp.json():
                if token.get("revoked") or not token.get("active", True):
                    continue
                if not check_expiration(token.get("expires_at")):
                    continue
                link = f"{GITLAB_BASE_URL}/groups/{group['full_path']}"
                print_token(token, label="Группа", link=link)
        except:
            continue

def main():
    print("\n=== Токены, истекающие через 30 дней или раньше (UTC) ===\n")
    check_personal_tokens()
    check_project_tokens()
    check_group_tokens()

if __name__ == "__main__":
    main()
