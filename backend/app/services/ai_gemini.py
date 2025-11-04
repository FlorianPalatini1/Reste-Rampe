import os
import google.generativeai as genai

# Initialize Gemini AI
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Sample recipes to return if API fails
SAMPLE_RECIPES = {
    'de': [
        {
            "text": """# Gemüse-Pfanne mit Reis

## Zutaten:
- 1 Tasse gemischtes Gemüse (Brokkoli, Karotten, Zuckerschoten)
- 1 Tasse gekochter Reis
- 2 EL Sojasoße
- 1 TL Sesamöl
- 2 Knoblauchzehen, gehackt
- 1 EL Ingwer, gehackt
- Optional: Sesamsamen, Frühlingszwiebeln

## Zubereitung:
1. Sesamöl in einem Wok oder großen Topf bei hoher Hitze erhitzen
2. Knoblauch und Ingwer hinzufügen, 30 Sekunden anbraten
3. Gemüse hinzufügen und 5-7 Minuten anbraten, bis es knackig-zart ist
4. Sojasoße über das Gemüse gießen und vermischen
5. Über gekochtem Reis servieren
6. Mit Sesamsamen und Frühlingszwiebeln garnieren

**Zubereitungszeit:** 15 Minuten | **Portionen:** 2 | **Kalorien:** ~350 pro Portion""",
            "model": "fallback"
        },
        {
            "text": """# Einfache Pasta Aglio e Olio (Knoblauch-Öl-Pasta)

## Zutaten:
- 200g Spaghetti
- 6 Knoblauchzehen, in Scheiben geschnitten
- 150ml Olivenöl
- Rote Pfefferflocken nach Geschmack
- Salz und Pfeffer
- Petersilie zum Garnieren
- Parmesankäse (optional)

## Zubereitung:
1. Spaghetti nach Packungsanleitung in Salzwasser kochen
2. Während die Pasta kocht, Olivenöl in einem großen Topf bei mittlerer Hitze erhitzen
3. Knoblauch und Rote Pfefferflocken hinzufügen
4. 2-3 Minuten kochen, bis der Knoblauch golden ist (nicht anbrennen!)
5. Pasta abgießen und 1 Tasse Nudelwasser auffangen
6. Pasta zum Knoblauch-Öl hinzufügen und gut vermischen
7. Nudelwasser nach Bedarf langsam hinzufügen, bis die gewünschte Konsistenz erreicht ist
8. Mit Salz und Pfeffer würzen
9. Mit Petersilie und Parmesankäse servieren

**Zubereitungszeit:** 15 Minuten | **Portionen:** 2 | **Kalorien:** ~450 pro Portion""",
            "model": "fallback"
        }
    ],
    'en': [
        {
            "text": """# Vegetarian Stir-Fry Bowl

## Ingredients:
- 1 cup mixed vegetables (broccoli, carrots, snap peas)
- 1 cup cooked rice
- 2 tbsp soy sauce
- 1 tsp sesame oil
- 2 cloves garlic, minced
- 1 tbsp ginger, minced
- Optional: sesame seeds, green onions

## Instructions:
1. Heat sesame oil in a wok or large pan over high heat
2. Add garlic and ginger, stir-fry for 30 seconds
3. Add vegetables and stir-fry for 5-7 minutes until tender-crisp
4. Pour soy sauce over vegetables and toss
5. Serve over cooked rice
6. Garnish with sesame seeds and green onions

**Prep time:** 15 minutes | **Servings:** 2 | **Calories:** ~350 per serving""",
            "model": "fallback"
        },
        {
            "text": """# Simple Pasta Aglio e Olio (Garlic and Oil Pasta)

## Ingredients:
- 200g spaghetti
- 6 cloves garlic, sliced
- 150ml olive oil
- Red pepper flakes to taste
- Salt and pepper
- Parsley for garnish
- Parmesan cheese (optional)

## Instructions:
1. Cook pasta according to package instructions in salted boiling water
2. While pasta cooks, heat olive oil in a large pan over medium heat
3. Add sliced garlic and red pepper flakes
4. Cook for 2-3 minutes until garlic is golden (don't burn!)
5. Drain pasta, reserving 1 cup of pasta water
6. Add pasta to garlic oil, toss well
7. Add pasta water gradually until you reach desired consistency
8. Season with salt and pepper
9. Serve topped with parsley and parmesan

**Prep time:** 15 minutes | **Servings:** 2 | **Calories:** ~450 per serving""",
            "model": "fallback"
        }
    ],
    'fr': [
        {
            "text": """# Sauté de Légumes

## Ingrédients:
- 1 tasse de légumes mélangés (brocoli, carottes, pois mange-tout)
- 1 tasse de riz cuit
- 2 c. à s. de sauce soja
- 1 c. à c. d'huile de sésame
- 2 gousses d'ail, hachées
- 1 c. à s. de gingembre, haché
- Optionnel: graines de sésame, oignons verts

## Instructions:
1. Chauffer l'huile de sésame dans un wok ou une grande poêle à feu vif
2. Ajouter l'ail et le gingembre, faire sauter 30 secondes
3. Ajouter les légumes et faire sauter 5-7 minutes jusqu'à tendres-croustillants
4. Verser la sauce soja sur les légumes et mélanger
5. Servir sur le riz cuit
6. Garnir de graines de sésame et oignons verts

**Temps de préparation:** 15 minutes | **Portions:** 2 | **Calories:** ~350 par portion""",
            "model": "fallback"
        },
        {
            "text": """# Pâtes Aglio e Olio Simples (Pâtes à l'Ail et l'Huile)

## Ingrédients:
- 200g de spaghetti
- 6 gousses d'ail, tranchées
- 150ml d'huile d'olive
- Flocons de piment rouge au goût
- Sel et poivre
- Persil pour la garniture
- Fromage Parmesan (optionnel)

## Instructions:
1. Cuire les pâtes selon les instructions du paquet dans l'eau salée bouillante
2. Pendant que les pâtes cuisent, chauffer l'huile d'olive dans une grande poêle à feu moyen
3. Ajouter l'ail tranché et les flocons de piment rouge
4. Cuire 2-3 minutes jusqu'à ce que l'ail soit doré (ne pas laisser brûler!)
5. Égoutter les pâtes en gardant 1 tasse d'eau de cuisson
6. Ajouter les pâtes à l'huile d'ail, mélanger bien
7. Ajouter graduellement l'eau de cuisson jusqu'à la consistance désirée
8. Assaisonner avec sel et poivre
9. Servir garni de persil et Parmesan

**Temps de préparation:** 15 minutes | **Portions:** 2 | **Calories:** ~450 par portion""",
            "model": "fallback"
        }
    ],
    'ja': [
        {
            "text": """# 野菜炒めボウル

## 材料:
- 1カップの混合野菜（ブロッコリー、ニンジン、エンドウ豆）
- 1カップの炊いたご飯
- 大さじ2の醤油
- 小さじ1のごま油
- ニンニク2片、みじん切り
- 生姜大さじ1、みじん切り
- オプション：ゴマ、ネギ

## 作り方:
1. 強火でフライパンまたは中華鍋にごま油を熱する
2. ニンニクと生姜を加えて30秒炒める
3. 野菜を加えて5～7分、柔らかく炒める
4. 醤油を野菜にかけて混ぜる
5. 炊いたご飯の上にのせて食べる
6. ゴマとネギを添えて完成

**調理時間:** 15分 | **人数:** 2人分 | **カロリー:** 1人当たり約350kcal""",
            "model": "fallback"
        }
    ],
    'tr': [
        {
            "text": """# Sebze Kızartması

## Malzemeler:
- 1 bardak karışık sebze (brokoli, havuç, bezelye)
- 1 bardak pişmiş pirinç
- 2 yemek kaşığı soya sosu
- 1 çay kaşığı sıvı yağ
- 2 diş sarımsak, ince doğranmış
- 1 yemek kaşığı zencefil, ince doğranmış
- İsteğe bağlı: susam tohumu, yeşil soğan

## Yapılışı:
1. Wok veya büyük bir tavayı yüksek ısıda sıvı yağla ısıtın
2. Sarımsak ve zencefili ekleyip 30 saniye pişirin
3. Sebzeleri ekleyip 5-7 dakika kıvam alıncaya kadar pişirin
4. Soya sosunu sebzelerin üzerine dökün ve karıştırın
5. Pişmiş pirinç üzerine servis yapın
6. Susam tohumu ve yeşil soğan ile garnish yapın

**Hazırlama Süresi:** 15 dakika | **Porsiyon:** 2 kişi | **Kalori:** Porsiyon başına ~350""",
            "model": "fallback"
        }
    ]
}

# Language mappings for prompts
LANGUAGE_NAMES = {
    'de': 'German',
    'en': 'English',
    'fr': 'French',
    'ja': 'Japanese',
    'tr': 'Turkish',
    'fa': 'Farsi',
    'nds': 'Low German'
}

def generate_recipe(ingredients: list = None, dietary_preferences: str = None, language: str = "de") -> dict:
    """Generate a recipe using Gemini AI from available ingredients"""
    try:
        if not api_key:
            # Return a fallback recipe if no API key
            import random
            recipes_for_lang = SAMPLE_RECIPES.get(language, SAMPLE_RECIPES.get('en', SAMPLE_RECIPES['de']))
            recipe = random.choice(recipes_for_lang)
            return recipe
        
        # Build the prompt
        lang_name = LANGUAGE_NAMES.get(language, 'English')
        
        if ingredients:
            # Create a prompt using the available ingredients
            ingredients_str = ', '.join(ingredients)
            prompt = f"""Please create a delicious recipe in {lang_name} using these available ingredients: {ingredients_str}.

Important guidelines:
- Use ONLY the ingredients provided above
- The recipe should be practical and easy to prepare
- Include: ingredients list, detailed cooking instructions, prep time, and servings
- Make it appealing and well-formatted with markdown headers
- Include estimated calories if possible"""
        else:
            # Generic recipe prompt if no ingredients specified
            prompt = f"Please create a delicious recipe in {lang_name}. Include: ingredients list, cooking instructions, prep time, and servings. Format it nicely with markdown headers."
        
        if dietary_preferences:
            prompt += f"\nThe recipe should be suitable for a {dietary_preferences} diet."
        
        # Get available models dynamically
        try:
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name.replace('models/', ''))
            print(f"Available Gemini models: {available_models}")
        except Exception as e:
            print(f"Could not list models: {str(e)}")
            available_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        
        # Try to use Gemini API with available models
        models_to_try = available_models if available_models else ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        response = None
        model_used = None
        
        for model_name in models_to_try:
            try:
                print(f"Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                model_used = model_name
                print(f"Successfully used model: {model_name}")
                break
            except Exception as e:
                print(f"Model {model_name} failed: {str(e)}")
                continue
        
        if response:
            return {
                "text": response.text,
                "model": model_used
            }
        else:
            # Use fallback recipes if API fails
            import random
            recipes_for_lang = SAMPLE_RECIPES.get(language, SAMPLE_RECIPES.get('en', SAMPLE_RECIPES['de']))
            recipe = random.choice(recipes_for_lang)
            return recipe
            
    except Exception as e:
        # Return fallback recipe on any error
        import random
        recipes_for_lang = SAMPLE_RECIPES.get(language, SAMPLE_RECIPES.get('en', SAMPLE_RECIPES['de']))
        recipe = random.choice(recipes_for_lang)
        return recipe

def save_ai_suggestion(text: str, dietary: str = None) -> dict:
    """Save an AI suggestion to the database (placeholder for future DB integration)"""
    return {
        "id": None,
        "text": text,
        "dietary": dietary,
        "created_at": None
    }

