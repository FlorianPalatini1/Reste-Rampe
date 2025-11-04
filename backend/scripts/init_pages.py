#!/usr/bin/env python3
"""Initialize all legal pages in the database"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine, Base
from app.models import Page
from sqlalchemy import text

def init_pages():
    """Create all legal pages"""
    db = SessionLocal()
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")
        
        db.execute(text("DELETE FROM pages"))
        db.commit()
        print("✅ Existing pages cleared")
        
        # Define all pages with their content
        pages = [
            # Privacy Policy
            Page(page_key="privacy", slug="privacy", title="Datenschutzerklärung", language="de",
                 content="# Datenschutzerklärung\n\nZuletzt aktualisiert: 4. November 2025\n\n## Verantwortlicher\nReste-Rampe ist eine Plattform zur Reduktion von Lebensmittelverschwendung.\n\n## Datenschutz\nWir schützen Ihre persönlichen Daten nach allen geltenden Datenschutzgesetzen."),
            
            Page(page_key="privacy", slug="privacy", title="Privacy Policy", language="en",
                 content="# Privacy Policy\n\nLast updated: November 4, 2025\n\n## Responsible Party\nReste-Rampe is a platform to reduce food waste.\n\n## Data Protection\nWe protect your personal data according to all applicable privacy laws."),
            
            Page(page_key="privacy", slug="privacy", title="Politique de Confidentialité", language="fr",
                 content="# Politique de Confidentialité\n\nDernière mise à jour : 4 novembre 2025\n\n## Responsable\nReste-Rampe est une plateforme de réduction du gaspillage alimentaire.\n\n## Protection des Données\nNous protégeons vos données personnelles selon toutes les lois applicables."),
            
            # Imprint
            Page(page_key="imprint", slug="imprint", title="Impressum", language="de",
                 content="# Impressum\n\nZuletzt aktualisiert: 4. November 2025\n\n## Verantwortlicher\nReste-Rampe\n\n## Kontakt\ninfo@reste-rampe.de"),
            
            Page(page_key="imprint", slug="imprint", title="Imprint", language="en",
                 content="# Imprint\n\nLast updated: November 4, 2025\n\n## Responsible\nReste-Rampe\n\n## Contact\ninfo@reste-rampe.de"),
            
            Page(page_key="imprint", slug="imprint", title="Mentions Légales", language="fr",
                 content="# Mentions Légales\n\nDernière mise à jour : 4 novembre 2025\n\n## Responsable\nReste-Rampe\n\n## Contact\ninfo@reste-rampe.de"),
            
            # Terms of Service
            Page(page_key="terms", slug="terms", title="Nutzungsbedingungen", language="de",
                 content="# Nutzungsbedingungen\n\nZuletzt aktualisiert: 4. November 2025\n\n## Geltungsbereich\nDiese Bedingungen regeln die Nutzung der Reste-Rampe Plattform.\n\n## Benutzerrechte\nBenutzer müssen sich korrekt registrieren und Ihr Passwort sichern."),
            
            Page(page_key="terms", slug="terms", title="Terms of Service", language="en",
                 content="# Terms of Service\n\nLast updated: November 4, 2025\n\n## Scope\nThese terms govern the use of the Reste-Rampe platform.\n\n## User Rights\nUsers must register correctly and secure their passwords."),
            
            Page(page_key="terms", slug="terms", title="Conditions d'Utilisation", language="fr",
                 content="# Conditions d'Utilisation\n\nDernière mise à jour : 4 novembre 2025\n\n## Champ d'Application\nCes conditions régissent l'utilisation de la plateforme Reste-Rampe.\n\n## Droits des Utilisateurs\nLes utilisateurs doivent s'inscrire correctement et sécuriser leurs mots de passe."),
            
            # AGB
            Page(page_key="agb", slug="agb", title="Allgemeine Geschäftsbedingungen", language="de",
                 content="# Allgemeine Geschäftsbedingungen\n\nZuletzt aktualisiert: 4. November 2025\n\n## Anwendungsbereich\nDiese AGB gelten für alle Leistungen der Reste-Rampe.\n\n## Vertragsschluss\nDurch die Registrierung akzeptiert der Benutzer diese AGB."),
            
            Page(page_key="agb", slug="agb", title="General Terms and Conditions", language="en",
                 content="# General Terms and Conditions\n\nLast updated: November 4, 2025\n\n## Scope\nThese GTC apply to all Reste-Rampe services.\n\n## Contract Formation\nBy registering, the user accepts these GTC."),
            
            Page(page_key="agb", slug="agb", title="Conditions Générales", language="fr",
                 content="# Conditions Générales\n\nDernière mise à jour : 4 novembre 2025\n\n## Champ d'Application\nCes CG s'appliquent à tous les services de Reste-Rampe.\n\n## Formation du Contrat\nEn s'inscrivant, l'utilisateur accepte ces CG."),
        ]
        
        # Add all pages to database
        for page in pages:
            db.add(page)
        
        db.commit()
        print("✅ Pages initialized successfully!")
        
        # List created pages
        all_pages = db.query(Page).order_by(Page.page_key, Page.language).all()
        print(f"\nCreated {len(all_pages)} pages:")
        for p in all_pages:
            print(f"  - {p.page_key} ({p.language}): {p.title}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    init_pages()
