#!/bin/bash

# Укажите ваш Jenkins URL, логин и API токен
JENKINS_URL="http://localhost:8080"
USERNAME="admin"
API_TOKEN="11e37d5430884c7d6b5f849196a454c656"

#all=$(curl -k -X GET -u admin:11e37d5430884c7d6b5f849196a454c656 "http://localhost:8080/pluginManager/api/json?depth=1" | jq -r '.plugins[] | "- \(.shortName):\(.version)"')
# Получаем список всех установленных плагинов
all_plugins=$(curl -k -s -X GET -u $USERNAME:$API_TOKEN "$JENKINS_URL/pluginManager/api/json?depth=1" | jq -r '.plugins[] | "- \(.shortName):\(.version)"')

# Получаем список плагинов, у которых есть обновления
updated_plugins=$(curl -k -s -X GET -u $USERNAME:$API_TOKEN "$JENKINS_URL/pluginManager/api/json?depth=1" | jq -r '.plugins[] | select(.hasUpdate) | "- \(.shortName):\(.version) → \(.availableVersion)"')

# Формируем список плагинов без обновлений
not_updated_plugins=$(echo "$all_plugins" | grep -v -F "$(echo "$updated_plugins" | cut -d' ' -f2)")

# Объединяем все списки
final_plugins_list=$(echo -e "$not_updated_plugins\n$updated_plugins")

# Вывод результатов
echo -e "\n✅ 📌 Все установленные плагины:\n"
echo "$all_plugins"

echo -e "\n✅ 📌 Плагины без обновлений:\n"
echo "$not_updated_plugins"

echo -e "\n🔹 📌 Плагины, которые можно обновить:\n"
echo "$updated_plugins"

echo -e "\n📌 🔥 Финальный список (неизмененные + обновленные):\n"
echo "$final_plugins_list"

# Сохраняем списки в файлы
echo "$all_plugins" > all_plugins.txt
echo "$not_updated_plugins" > not_updated_plugins.txt
echo "$updated_plugins" > updated_plugins.txt
echo "$final_plugins_list" > final_plugins_list.txt

echo -e "\n✅ Все списки сохранены в файлы!"
