from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import News
from app.schemas_news import NewsCreate, NewsUpdate, NewsResponse
from datetime import datetime
from typing import List

router = APIRouter(tags=["news"])


# Food-related news articles (sample data that can be extended)
FOOD_NEWS_SAMPLES = {
    "de": [
        {
            "title": "Neue Superfood-Trends 2024: Was Sie wissen sollten",
            "excerpt": "Entdecken Sie die Top-Superfoods des Jahres und wie Sie diese in Ihre tägliche Ernährung integrieren können.",
            "content": "# Neue Superfood-Trends 2024\n\nDie Welt der Ernährung entwickelt sich ständig weiter. In diesem Jahr sehen wir spannende neue Superfoods, die die Ernährungswissenschaft revolutionieren.\n\n## Top Superfoods 2024\n\n1. **Fermentierte Lebensmittel** - Kimchi, Tempeh und andere fermentierte Produkte unterstützen die Darmgesundheit\n2. **Pilze** - Reich an Vitaminen und natürlichen Immunverstärkern\n3. **Algen** - Eine ausgezeichnete Quelle für Jod und Mineralstoffe\n4. **Pseudocerealien** - Quinoa, Amaranth und Buchweizen sind glutenfrei und nährstoffreich\n\n## Wie Sie davon profitieren\n\nAchten Sie darauf, diese Lebensmittel schrittweise in Ihre Ernährung einzuführen und experimentieren Sie mit neuen Rezepten.",
            "category": "Ernährung",
            "source": "Resta Rampe Newsdesk"
        },
        {
            "title": "Nachhaltige Landwirtschaft: Vom Feld auf Ihren Teller",
            "excerpt": "Wie nachhaltige Anbaumethoden nicht nur der Umwelt helfen, sondern auch bessere Lebensmittel produzieren.",
            "content": "# Nachhaltige Landwirtschaft\n\nDie Art und Weise, wie wir Lebensmittel anbauen, hat großen Einfluss auf die Umwelt und die Qualität unserer Nahrung.\n\n## Die Vorteile nachhaltiger Landwirtschaft\n\n- Bessere Bodenqualität\n- Höherer Nährstoffgehalt in Lebensmitteln\n- Weniger Pestizide\n- Unterstützung lokaler Bauern\n\nWählen Sie lokale und saisonale Produkte, um die nachhaltige Landwirtschaft zu unterstützen.",
            "category": "Nachhaltigkeit",
            "source": "Resta Rampe Newsdesk"
        },
        {
            "title": "Fermentation: Das alte Handwerk erlebt eine Renaissance",
            "excerpt": "Die Fermentation von Lebensmitteln ist ein jahrtausendealtes Handwerk, das wieder großes Interesse weckt.",
            "content": "# Fermentation: Altes Handwerk, moderne Küche\n\nDie Fermentation ist eines der ältesten Konservierungsverfahren der Menschheit und erlebt gerade eine Renaissance.\n\n## Warum fermentieren?\n\n1. **Langzeitkonservierung** - Fermentierte Lebensmittel haltbar für Monate oder Jahre\n2. **Probiotika** - Unterstützung der Darmgesundheit\n3. **Verbesserte Nährstoffverfügbarkeit** - Der Körper kann Nährstoffe besser aufnehmen\n4. **Geschmack** - Komplexe und tiefe Geschmacksprofile\n\n## Einfache Fermentationen zum Selbermachen\n\n- Sauerkraut\n- Kimchi\n- Kombucha\n- Joghurt",
            "category": "Kochen",
            "source": "Resta Rampe Newsdesk"
        }
    ],
    "en": [
        {
            "title": "Top Food Trends of 2024: What You Need to Know",
            "excerpt": "Discover the hottest food trends this year and how to incorporate them into your kitchen.",
            "content": "# Top Food Trends of 2024\n\nThe culinary world is constantly evolving. This year brings exciting innovations and rediscoveries.\n\n## Trending Topics\n\n1. **Plant-Based Everything** - From meat alternatives to dairy-free products\n2. **Local and Seasonal** - Supporting local farmers and sustainable practices\n3. **Fermented Foods** - Kombucha, kimchi, and other fermented delights\n4. **Ancient Grains** - Rediscovering nutritious grains from history\n\n## How to Get Started\n\nExperiment with one new trend each week and find what works best for your lifestyle.",
            "category": "Food Trends",
            "source": "Resta Rampe Newsdesk"
        },
        {
            "title": "The Rise of Plant-Based Cooking",
            "excerpt": "Plant-based diets are not just a trend, they're a sustainable lifestyle choice.",
            "content": "# Plant-Based Cooking Revolution\n\nMore people are choosing plant-based diets for health, environmental, and ethical reasons.\n\n## Benefits of Plant-Based Eating\n\n- Lower carbon footprint\n- Reduced risk of chronic diseases\n- Greater variety of foods\n- Support for sustainable agriculture\n\n## Getting Started with Plant-Based Cooking\n\nBegin by incorporating meatless Mondays into your week and gradually expand from there.",
            "category": "Nutrition",
            "source": "Resta Rampe Newsdesk"
        },
        {
            "title": "How to Build the Perfect Home Spice Cabinet",
            "excerpt": "A well-stocked spice cabinet is the foundation of flavorful cooking.",
            "content": "# Your Essential Home Spice Cabinet\n\nWith the right spices, you can transform simple ingredients into extraordinary dishes.\n\n## Essential Spices\n\n1. **Cumin** - Warmth and earthiness\n2. **Paprika** - Sweetness and depth\n3. **Cinnamon** - Warmth in both sweet and savory dishes\n4. **Coriander** - Brightness and citrus notes\n5. **Black Pepper** - The fundamental spice\n\n## Storage Tips\n\nKeep spices in airtight containers away from light and heat for maximum freshness.",
            "category": "Cooking",
            "source": "Resta Rampe Newsdesk"
        }
    ],
    "fr": [
        {
            "title": "Les Tendances Culinaires de 2024",
            "excerpt": "Découvrez les tendances culinaires les plus en vogue cette année.",
            "content": "# Les Tendances Culinaires de 2024\n\nLa gastronomie évolue constamment avec de nouvelles influences et réinterprétations.\n\n## Tendances Principales\n\n1. **Cuisine végétale** - Des alternatives innovantes à la viande\n2. **Fermentation** - L'art ancien revient en force\n3. **Produits locaux** - Soutenir les producteurs régionaux\n4. **Cuisines du monde** - Fusion et expérimentation\n\n## Comment Exploiter Ces Tendances\n\nCommencez par un petit changement dans votre cuisine et développez progressivement.",
            "category": "Tendances",
            "source": "Resta Rampe Newsdesk"
        },
        {
            "title": "L'Art de la Fermentation Traditionnelle",
            "excerpt": "La fermentation est un processus millénaire qui connaît une véritable renaissance.",
            "content": "# Fermentation: Un Art Culinaire Ancien\n\nLa fermentation transforme les aliments simples en délices savoureux et sains.\n\n## Bénéfices de la Fermentation\n\n- Meilleure digestibilité\n- Probiotiques naturels\n- Conservation naturelle\n- Saveurs complexes\n\n## Aliments Faciles à Fermenter\n\n- Chou (choucroute, kimchi)\n- Légumes (cornichons fermentés)\n- Boissons (kombucha, gingembre fermenté)",
            "category": "Cuisine",
            "source": "Resta Rampe Newsdesk"
        },
        {
            "title": "Cuisiner Avec Les Saisons: Un Guide Pratique",
            "excerpt": "Apprenez à cuisiner en harmonie avec les saisons pour des résultats optimaux.",
            "content": "# Cuisiner Avec Les Saisons\n\nLa cuisine saisonnière garantit des ingrédients frais, savoureux et durables.\n\n## Avantages de la Cuisine Saisonnière\n\n1. **Goût supérieur** - Les produits à leur apogée\n2. **Économies** - Prix réduits pour produits de saison\n3. **Durabilité** - Moins de transport et d'emballage\n4. **Support local** - Aide aux agriculteurs régionaux\n\n## Aliments de Saison\n\nConsultez les calendriers saisonniers locaux pour découvrir les meilleurs produits.",
            "category": "Saisonnalité",
            "source": "Resta Rampe Newsdesk"
        }
    ]
}


@router.get("/", response_model=List[NewsResponse])
def get_news(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(6, ge=1, le=50),
    language: str = Query("de")
):
    """Get news articles with pagination"""
    # First try to get from database
    articles = db.query(News).offset(skip).limit(limit).all()
    
    # If no articles in database, return sample data
    if not articles:
        sample_articles = FOOD_NEWS_SAMPLES.get(language, FOOD_NEWS_SAMPLES.get("de", []))
        return [
            {
                "id": idx + 1,
                "title": article["title"],
                "excerpt": article["excerpt"],
                "content": article["content"],
                "category": article["category"],
                "source": article["source"],
                "published_at": datetime.utcnow().isoformat(),
                "image_url": None,
                "language": language
            }
            for idx, article in enumerate(sample_articles)
        ]
    
    return articles


@router.get("/{article_id}", response_model=NewsResponse)
def get_news_article(article_id: int, db: Session = Depends(get_db)):
    """Get a single news article"""
    article = db.query(News).filter(News.id == article_id).first()
    if not article:
        # Return sample article if not found in database
        sample_articles = FOOD_NEWS_SAMPLES.get("de", [])
        if article_id - 1 < len(sample_articles):
            sample = sample_articles[article_id - 1]
            return {
                "id": article_id,
                "title": sample["title"],
                "excerpt": sample["excerpt"],
                "content": sample["content"],
                "category": sample["category"],
                "source": sample["source"],
                "published_at": datetime.utcnow().isoformat(),
                "image_url": None,
                "language": "de"
            }
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/", response_model=NewsResponse)
def create_news(article: NewsCreate, db: Session = Depends(get_db)):
    """Create a new news article (admin only)"""
    db_article = News(
        title=article.title,
        excerpt=article.excerpt,
        content=article.content,
        category=article.category,
        source=article.source,
        image_url=article.image_url,
        language=article.language,
        published_at=datetime.utcnow()
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.put("/{article_id}", response_model=NewsResponse)
def update_news(article_id: int, article: NewsUpdate, db: Session = Depends(get_db)):
    """Update a news article"""
    db_article = db.query(News).filter(News.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if article.title:
        db_article.title = article.title
    if article.excerpt:
        db_article.excerpt = article.excerpt
    if article.content:
        db_article.content = article.content
    if article.category:
        db_article.category = article.category
    if article.source:
        db_article.source = article.source
    if article.image_url:
        db_article.image_url = article.image_url
    
    db.commit()
    db.refresh(db_article)
    return db_article


@router.delete("/{article_id}")
def delete_news(article_id: int, db: Session = Depends(get_db)):
    """Delete a news article"""
    db_article = db.query(News).filter(News.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(db_article)
    db.commit()
    return {"status": "deleted"}
