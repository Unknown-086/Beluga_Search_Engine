from langdetect import DetectorFactory, detect
from langdetect.lang_detect_exception import LangDetectException

# Fix seed for consistent results
# DetectorFactory.seed = 0

def detect_language_with_constraints(text, lang_subset=['ru', 'en', 'fr']):
    try:
        detected = detect(text)
        if detected in lang_subset:
            return detected
        else:
            return 'unknown'
    except LangDetectException:
        return 'unknown'

# raw_text = "Язык крестьян имеет пестрое разнообразие, унаследованное от феодализма. На пути к пролетариату крестьянство приносит на фабрику и завод свои местные крестьянские говоры с их фонетикой, грамматикой и лексикой, а самый процесс набора рабочих из крестьян и мобильность рабочего населения порождают другой процесс: ликвидацию. крестьянского наследства путем нивелирования особенностей местных диалектов"
raw_text = "т"

language = detect_language_with_constraints(raw_text, lang_subset=['ru', 'en', 'fr'])
print(language)  # Should output 'ru' for Russian
