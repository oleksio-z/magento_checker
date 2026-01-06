## 🚀 **English README**

# Magento Checker

**Magento Checker** is a simple Python script that analyzes a list of domains and outputs a filtered list of sites that use the **Magento CMS**. 
It's useful for quickly identifying Magento-powered websites from a bulk domain list.

### ⚙️ Features

* Parses a given domain list
* Detects sites running **Magento CMS**
* Outputs results to a new file
* Uses asynchronous requests for faster scanning

### 🧰 Requirements

Make sure Python is installed along with the following packages:

```bash
pip install aiohttp aiofiles termcolor
```

### 📌 Usage

```bash
python3 magento_check.py -i input_domains.txt -o magento_sites.txt
```

**Flags:**

* `-i` — Path to input file with domains
* `-o` — Output file for detected Magento sites

### 📄 License

This project is released under the **GPL-2.0 License**.

---

## 🇺🇦 **Український README**

# Magento Checker

**Magento Checker** — це простий Python-скрипт, який аналізує список доменів та створює новий список сайтів, що працюють на **CMS Magento**. 
Ідеально підходить для швидкого визначення Magento-сайтів у великому переліку доменів.

### ⚙️ Можливості

* Обробка заданого списку доменів
* Виявлення сайтів, що використовують Magento
* Виведення результатів у файл
* Асинхронні запити для пришвидшеної обробки

### 🧰 Вимоги

Переконайся, що у тебе встановлений Python та такі пакети:

```bash
pip install aiohttp aiofiles termcolor
```

### 📌 Як використовувати

```bash
python3 magento_check.py -i input_domains.txt -o magento_sites.txt
```

**Параметри:**

* `-i` — шлях до вхідного файлу з доменами
* `-o` — вихідний файл для сайтів на Magento

### 📄 Ліцензія

Цей проєкт поширюється під ліцензією **GPL-2.0**.

---
