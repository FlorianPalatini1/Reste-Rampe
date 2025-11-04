from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.database import get_db
from app.models import Recipe, AISuggestion
from app.schemas import Recipe as RecipeSchema, RecipeCreate, AISuggestion as AISuggestionSchema, SaveAIRecipeRequest
from app.services.ai_gemini import generate_recipe, save_ai_suggestion

router = APIRouter()


@router.get("/", response_model=List[RecipeSchema])
def get_recipes(db: Session = Depends(get_db), healthy_only: bool = False, language: str = "de"):
    """Get all recipes for a specific language"""
    query = db.query(Recipe).filter(Recipe.language == language)
    if healthy_only:
        query = query.filter(Recipe.is_healthy == True)
    return query.all()


@router.get("/{recipe_id}", response_model=RecipeSchema)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Get a specific recipe"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/", response_model=RecipeSchema)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """Create a new recipe"""
    db_recipe = Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Delete a recipe"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
    return {"status": "deleted"}


@router.get("/match/ingredients")
def generate_recipe_from_ingredients(db: Session = Depends(get_db), language: str = "de"):
    """Generate a recipe using available ingredients"""
    from app.models import Ingredient
    
    # Get all available ingredients from the database
    available_ingredients = db.query(Ingredient).all()
    ingredient_names = [ing.name for ing in available_ingredients]
    
    if not ingredient_names:
        # If no ingredients available, return error
        raise HTTPException(status_code=400, detail="Keine Zutaten verfügbar")
    
    # Generate recipe using available ingredients
    result = generate_recipe(ingredients=ingredient_names, language=language)
    return result


@router.post("/seed-sample")
def seed_sample_recipes(db: Session = Depends(get_db)):
    """Seed sample recipes into the database"""
    sample_recipes = [
        # German recipes
        {
            "name": "Pasta Carbonara",
            "description": "Klassische italienische Pasta mit Eiern und Speck",
            "ingredients": json.dumps(["200g Pasta", "100g Speck", "3 Eier", "100g Parmesan"]),
            "instructions": "Pasta kochen. Speck braten. Eier und Käse vermischen. Alles kombinieren.",
            "prep_time": 20,
            "servings": 2,
            "calories": 550,
            "is_healthy": False,
            "language": "de"
        },
        {
            "name": "Gegrillter Hähnchensalat",
            "description": "Gesundes gegrilltes Hähnchen mit frischem Gemüse",
            "ingredients": json.dumps(["200g Hähnchenbrust", "100g Salat", "50g Karotten", "50g Tomate"]),
            "instructions": "Hähnchen grillen. Gemüse hacken. Mit Dressing vermischen.",
            "prep_time": 15,
            "servings": 1,
            "calories": 300,
            "is_healthy": True,
            "language": "de"
        },
        {
            "name": "Gemüse-Pfanne",
            "description": "Schnelle und farbenfrohe Gemüse-Pfanne",
            "ingredients": json.dumps(["100g Brokkoli", "100g Paprika", "100g Karotten", "2 Knoblauchzehen", "2 EL Sojasoße"]),
            "instructions": "Wok erhitzen. Gemüse anbraten. Knoblauch und Sojasoße hinzufügen. Heiß servieren.",
            "prep_time": 10,
            "servings": 2,
            "calories": 150,
            "is_healthy": True,
            "language": "de"
        },
        # English recipes
        {
            "name": "Pasta Carbonara",
            "description": "Classic Italian pasta with eggs and bacon",
            "ingredients": json.dumps(["200g pasta", "100g bacon", "3 eggs", "100g parmesan"]),
            "instructions": "Cook pasta. Fry bacon. Mix eggs and cheese. Combine everything.",
            "prep_time": 20,
            "servings": 2,
            "calories": 550,
            "is_healthy": False,
            "language": "en"
        },
        {
            "name": "Grilled Chicken Salad",
            "description": "Healthy grilled chicken with fresh vegetables",
            "ingredients": json.dumps(["200g chicken breast", "100g lettuce", "50g carrots", "50g tomato"]),
            "instructions": "Grill chicken. Chop vegetables. Toss with dressing.",
            "prep_time": 15,
            "servings": 1,
            "calories": 300,
            "is_healthy": True,
            "language": "en"
        },
        {
            "name": "Vegetable Stir Fry",
            "description": "Quick and colorful vegetable stir fry",
            "ingredients": json.dumps(["100g broccoli", "100g bell pepper", "100g carrots", "2 cloves garlic", "2 tbsp soy sauce"]),
            "instructions": "Heat wok. Stir fry vegetables. Add garlic and soy sauce. Serve hot.",
            "prep_time": 10,
            "servings": 2,
            "calories": 150,
            "is_healthy": True,
            "language": "en"
        },
        # French recipes
        {
            "name": "Pâtes Carbonara",
            "description": "Pâtes italiennes classiques aux œufs et au bacon",
            "ingredients": json.dumps(["200g pâtes", "100g bacon", "3 œufs", "100g parmesan"]),
            "instructions": "Cuire les pâtes. Frire le bacon. Mélanger les œufs et le fromage. Combiner le tout.",
            "prep_time": 20,
            "servings": 2,
            "calories": 550,
            "is_healthy": False,
            "language": "fr"
        },
        {
            "name": "Salade de Poulet Grillé",
            "description": "Poulet grillé sain avec des légumes frais",
            "ingredients": json.dumps(["200g poitrine de poulet", "100g laitue", "50g carottes", "50g tomate"]),
            "instructions": "Griller le poulet. Hacher les légumes. Mélanger avec la vinaigrette.",
            "prep_time": 15,
            "servings": 1,
            "calories": 300,
            "is_healthy": True,
            "language": "fr"
        },
        {
            "name": "Sauté de Légumes",
            "description": "Sauté de légumes rapide et coloré",
            "ingredients": json.dumps(["100g brocoli", "100g poivron", "100g carottes", "2 gousses d'ail", "2 c. à s. sauce soja"]),
            "instructions": "Chauffer le wok. Faire sauter les légumes. Ajouter l'ail et la sauce soja. Servir chaud.",
            "prep_time": 10,
            "servings": 2,
            "calories": 150,
            "is_healthy": True,
            "language": "fr"
        }
    ]
    
    for recipe_data in sample_recipes:
        # Check if recipe already exists
        existing = db.query(Recipe).filter(
            Recipe.name == recipe_data["name"],
            Recipe.language == recipe_data["language"]
        ).first()
        if not existing:
            db_recipe = Recipe(**recipe_data)
            db.add(db_recipe)
    
    db.commit()
    return {"status": "seeded", "count": len(sample_recipes)}


@router.post("/generate")
def generate_ai_recipe(dietary: str = None, language: str = "de"):
    """Generate a random recipe using AI"""
    result = generate_recipe(dietary_preferences=dietary, language=language)
    return result


@router.post("/save-from-ai")
def save_ai_recipe(request: SaveAIRecipeRequest, db: Session = Depends(get_db), language: str = "de"):
    """Save an AI-generated recipe"""
    if not request.text:
        raise HTTPException(status_code=400, detail="text is required")
    
    title = request.title or "AI Generated Recipe"
    
    recipe = Recipe(
        name=title,
        description="Generated by AI",
        ingredients=json.dumps([]),
        instructions=request.text,
        is_healthy=False,
        language=language
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.get("/ai/suggestions")
def get_ai_suggestions(limit: int = 5, db: Session = Depends(get_db)):
    """Get recent AI suggestions"""
    suggestions = db.query(AISuggestion).order_by(AISuggestion.created_at.desc()).limit(limit).all()
    return suggestions
