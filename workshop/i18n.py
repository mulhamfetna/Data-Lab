"""Lightweight bilingual (English / Arabic) strings for the platform's core UI."""

TRANSLATIONS = {
    "title":     {"en": "Data to Decisions", "ar": "من البيانات إلى القرار"},
    "subtitle":  {"en": "An interactive tour of how data becomes a decision",
                  "ar": "جولة تفاعلية حول كيف تتحوّل البيانات إلى قرار"},
    "intro":     {"en": "Each 📊 page is a slide and each 🧪 page is a live demo. The demos "
                        "follow one small business — Nour Store — from raw data to a decision.",
                  "ar": "كل صفحة 📊 شريحة وكل صفحة 🧪 عرض حيّ. تتبع العروض متجرًا صغيرًا واحدًا — "
                        "متجر نور — من البيانات الخام إلى القرار."},
    "journey":   {"en": "The journey", "ar": "الرحلة"},
    "begin":     {"en": "Pick a page from the sidebar to begin.",
                  "ar": "اختر صفحة من الشريط الجانبي للبدء."},
    "takeaway":  {"en": "Leader takeaway", "ar": "الخلاصة للقائد"},
    "language":  {"en": "Language", "ar": "اللغة"},
    "Collect":   {"en": "Collect", "ar": "جمع"},
    "Clean":     {"en": "Clean", "ar": "تنظيف"},
    "Analyze":   {"en": "Analyze", "ar": "تحليل"},
    "Decision":  {"en": "Decision", "ar": "قرار"},
}


def t(key: str, lang: str = "en") -> str:
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    return entry.get(lang, entry.get("en", key))
