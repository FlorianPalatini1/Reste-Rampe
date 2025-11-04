from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Page, User
from app.schemas import PageResponse, PageCreate, PageUpdate
from app.auth import get_current_user_from_token
from datetime import datetime

router = APIRouter()

# Sample GDPR-compliant privacy policies in multiple languages
PRIVACY_PAGES = {
    "de": {
        "slug": "privacy",
        "title": "Datenschutzerklärung",
        "content": """# Datenschutzerklärung

**Zuletzt aktualisiert: 29. Oktober 2025**

## 1. Verantwortlicher

Resta Rampe
E-Mail: privacy@resta-rampe.de

## 2. Allgemeine Informationen zur Datenverarbeitung

### 2.1 Umfang der Verarbeitung persönlicher Daten

Wir verarbeiten personenbezogene Daten der Nutzer nur in dem Umfang, wie dies zur Bereitstellung einer funktionsfähigen Website sowie unserer Inhalte und Leistungen erforderlich ist.

### 2.2 Rechtsgrundlagen

Die Verarbeitung personenbezogener Daten erfolgt auf Grundlage von:
- Art. 6 Abs. 1 a) DSGVO (Einwilligung)
- Art. 6 Abs. 1 b) DSGVO (Vertragserfüllung)
- Art. 6 Abs. 1 c) DSGVO (Rechtsverbindlichkeit)
- Art. 6 Abs. 1 f) DSGVO (berechtigte Interessen)

## 3. Datenerfassung und -verarbeitung

### 3.1 Registrierung und Benutzerkonto

Wenn Sie sich auf unserer Website registrieren, erfassen wir folgende Daten:
- Benutzername
- E-Mail-Adresse
- Passwort (verschlüsselt)
- Registrationsdatum

Diese Daten werden verarbeitet, um:
- Ihnen ein Benutzerkonto zu erstellen
- Sie zu authentifizieren
- Unsere Dienstleistungen bereitzustellen

### 3.2 Rezepte und Shopping-Listen

Wenn Sie Rezepte erstellen oder Einkaufslisten verwalten, speichern wir:
- Rezeptinformationen und Zutaten
- Einkaufslisten und deren Inhalte
- Zeitstempel der Erstellung und Änderung

Diese Daten werden nur zum Zweck der Bereitstellung dieser Funktionen verwendet.

### 3.3 Künstliche Intelligenz und Generierung

Wenn Sie KI-gestützte Funktionen (z.B. Rezeptvorschläge) nutzen, werden Ihre Anfragen und Zutaten an den KI-Dienst Google Gemini übermittelt. Bitte beachten Sie die Datenschutzrichtlinie von Google.

### 3.4 Automatische Datenerfassung

#### Cookies und Speichertechnologien

Unsere Website verwendet Cookies zur Speicherung von:
- Authentifizierungsinformationen (Session-Tokens)
- Spracheinstellungen
- Benutzereinstellungen

Sie können Cookies in Ihren Browsereinstellungen deaktivieren.

#### Log-Daten

Unser Server erfasst automatisch:
- IP-Adresse
- Browser-Typ und Version
- Betriebssystem
- Besuchte Seiten
- Zugriffszeitpunkte

Diese Daten werden verwendet für:
- Server-Sicherheit und Fehlerdiagnose
- Analyse der Website-Nutzung
- Verbesserung unserer Dienste

## 4. Weitergabe von Daten

Ihre personenbezogenen Daten werden nicht an Dritte weitergegeben, außer:

- **Rechtsverbindlichkeit**: Wenn wir gesetzlich dazu verpflichtet sind
- **Service-Provider**: Hosting-Anbieter und Datenbankdienste
- **KI-Dienste**: Google Gemini API für Rezeptgenerierung
- **Mit Ihrer Zustimmung**: Zu anderen Zwecken nur mit Ihrer ausdrücklichen Genehmigung

## 5. Datensicherheit

Wir implementieren technische und organisatorische Maßnahmen zum Schutz Ihrer Daten:
- SSL/TLS-Verschlüsselung für Datenübertragung
- Gehashte Passwörter in der Datenbank
- Regelmäßige Sicherheitsprüfungen
- Zugriffskontrolle und Berechtigungsverwaltung

## 6. Dauer der Datenspeicherung

- **Benutzerkonto**: Solange Ihr Konto aktiv ist, danach 30 Tage
- **Rezepte und Listen**: Solange Sie diese speichern möchten
- **Log-Daten**: 30 Tage
- **Cookies**: Je nach Art zwischen Session-Ende und 1 Jahr

## 7. Ihre Rechte

Sie haben folgende Rechte gemäß DSGVO:

### 7.1 Auskunftsrecht (Art. 15 DSGVO)
Sie können Auskunft darüber verlangen, welche personenbezogenen Daten wir über Sie verarbeiten.

### 7.2 Berichtigungsrecht (Art. 16 DSGVO)
Sie können die Berichtigung ungenauer personenbezogener Daten verlangen.

### 7.3 Löschungsrecht (Art. 17 DSGVO)
Sie können unter bestimmten Voraussetzungen die Löschung Ihrer personenbezogenen Daten verlangen.

### 7.4 Einschränkung der Verarbeitung (Art. 18 DSGVO)
Sie können die Einschränkung der Verarbeitung Ihrer Daten verlangen.

### 7.5 Datenportabilität (Art. 20 DSGVO)
Sie können Ihre Daten in einem strukturierten, gängigen Format erhalten.

### 7.6 Widerspruchsrecht (Art. 21 DSGVO)
Sie können der Verarbeitung Ihrer Daten widersprechen.

### 7.7 Widerrufsrecht
Sie können Ihre Einwilligung zur Datenverarbeitung jederzeit widerrufen.

## 8. Datenschutzbeauftragter

Bei Fragen zum Datenschutz kontaktieren Sie uns unter:
- E-Mail: privacy@resta-rampe.de
- Adresse: Resta Rampe, [Ihre Adresse]

## 9. Beschwerderecht

Sie haben das Recht, sich bei einer Datenschutzbehörde zu beschweren:
- Bundesbeauftragte für den Datenschutz und die Informationsfreiheit (BfDI)
- E-Mail: poststelle@bfdi.bund.de

## 10. Änderungen dieser Datenschutzerklärung

Wir behalten uns das Recht vor, diese Datenschutzerklärung jederzeit anzupassen. Wir werden Sie über wesentliche Änderungen benachrichtigen.

## 11. Kontakt

Bei Fragen, Bedenken oder Anfragen zu dieser Datenschutzerklärung können Sie uns kontaktieren unter:
- E-Mail: privacy@resta-rampe.de
- Website: resta-rampe.de
"""
    },
    "en": {
        "slug": "privacy",
        "title": "Privacy Policy",
        "content": """# Privacy Policy

**Last Updated: October 29, 2025**

## 1. Responsible Party

Resta Rampe
Email: privacy@resta-rampe.de

## 2. General Information on Data Processing

### 2.1 Scope of Personal Data Processing

We process personal data of users only to the extent necessary to provide a functional website and our content and services.

### 2.2 Legal Basis

The processing of personal data is based on:
- Art. 6 Abs. 1 a) GDPR (Consent)
- Art. 6 Abs. 1 b) GDPR (Contract fulfillment)
- Art. 6 Abs. 1 c) GDPR (Legal obligation)
- Art. 6 Abs. 1 f) GDPR (Legitimate interests)

## 3. Data Collection and Processing

### 3.1 Registration and User Account

When you register on our website, we collect:
- Username
- Email address
- Password (encrypted)
- Registration date

This data is processed to:
- Create your user account
- Authenticate you
- Provide our services

### 3.2 Recipes and Shopping Lists

When you create recipes or manage shopping lists, we store:
- Recipe information and ingredients
- Shopping lists and their contents
- Creation and modification timestamps

This data is used only for providing these features.

### 3.3 Artificial Intelligence and Generation

When you use AI features (e.g., recipe suggestions), your requests and ingredients are submitted to Google Gemini. Please review Google's privacy policy.

### 3.4 Automatic Data Collection

#### Cookies and Storage Technologies

Our website uses cookies to store:
- Authentication information (session tokens)
- Language settings
- User preferences

You can disable cookies in your browser settings.

#### Log Data

Our server automatically collects:
- IP address
- Browser type and version
- Operating system
- Visited pages
- Access times

This data is used for:
- Server security and error diagnostics
- Website usage analysis
- Service improvement

## 4. Data Sharing

Your personal data is not shared with third parties, except:

- **Legal obligation**: If required by law
- **Service providers**: Hosting and database services
- **AI services**: Google Gemini API for recipe generation
- **With your consent**: For other purposes only with explicit permission

## 5. Data Security

We implement technical and organizational measures to protect your data:
- SSL/TLS encryption for data transmission
- Hashed passwords in the database
- Regular security checks
- Access control and permission management

## 6. Data Retention

- **User account**: As long as your account is active, then 30 days
- **Recipes and lists**: As long as you wish to store them
- **Log data**: 30 days
- **Cookies**: Depending on type, between session end and 1 year

## 7. Your Rights

You have the following rights under GDPR:

### 7.1 Right of Access (Art. 15 GDPR)
You can request information about what personal data we process about you.

### 7.2 Right to Rectification (Art. 16 GDPR)
You can request correction of inaccurate personal data.

### 7.3 Right to Erasure (Art. 17 GDPR)
Under certain circumstances, you can request deletion of your personal data.

### 7.4 Right to Restrict Processing (Art. 18 GDPR)
You can request restriction of processing of your data.

### 7.5 Data Portability (Art. 20 GDPR)
You can obtain your data in a structured, commonly used format.

### 7.6 Right to Object (Art. 21 GDPR)
You can object to processing of your data.

### 7.7 Right to Withdraw Consent
You can withdraw your consent to data processing at any time.

## 8. Data Protection Officer

For questions about data protection, contact us at:
- Email: privacy@resta-rampe.de
- Address: Resta Rampe, [Your Address]

## 9. Right to Lodge a Complaint

You have the right to lodge a complaint with a data protection authority:
- German Federal Data Protection Commissioner
- Email: poststelle@bfdi.bund.de

## 10. Changes to Privacy Policy

We reserve the right to update this privacy policy at any time. We will notify you of material changes.

## 11. Contact

For questions, concerns, or requests regarding this privacy policy, you can contact us at:
- Email: privacy@resta-rampe.de
- Website: resta-rampe.de
"""
    },
    "fr": {
        "slug": "privacy",
        "title": "Politique de Confidentialité",
        "content": """# Politique de Confidentialité

**Dernière mise à jour : 29 octobre 2025**

## 1. Responsable du Traitement

Resta Rampe
Email: privacy@resta-rampe.de

## 2. Informations Générales sur le Traitement des Données

### 2.1 Portée du Traitement des Données Personnelles

Nous traitons les données personnelles des utilisateurs uniquement dans la mesure nécessaire pour fournir un site Web fonctionnel et nos contenus et services.

### 2.2 Base Juridique

Le traitement des données personnelles est fondé sur:
- Art. 6 Abs. 1 a) RGPD (Consentement)
- Art. 6 Abs. 1 b) RGPD (Exécution du contrat)
- Art. 6 Abs. 1 c) RGPD (Obligation légale)
- Art. 6 Abs. 1 f) RGPD (Intérêts légitimes)

## 3. Collecte et Traitement des Données

### 3.1 Inscription et Compte Utilisateur

Lorsque vous vous inscrivez sur notre site Web, nous collectons:
- Nom d'utilisateur
- Adresse email
- Mot de passe (chiffré)
- Date d'inscription

Ces données sont traitées pour:
- Créer votre compte utilisateur
- Vous authentifier
- Fournir nos services

### 3.2 Recettes et Listes de Courses

Lorsque vous créez des recettes ou gérez des listes de courses, nous stockons:
- Informations sur les recettes et ingrédients
- Listes de courses et leurs contenus
- Horodatages de création et modification

Ces données sont utilisées uniquement pour la fourniture de ces fonctionnalités.

### 3.3 Intelligence Artificielle et Génération

Lorsque vous utilisez des fonctionnalités IA (par exemple, suggestions de recettes), vos demandes et ingrédients sont soumis à Google Gemini. Veuillez consulter la politique de confidentialité de Google.

### 3.4 Collecte Automatique de Données

#### Cookies et Technologies de Stockage

Notre site Web utilise des cookies pour stocker:
- Informations d'authentification (jetons de session)
- Paramètres de langue
- Préférences utilisateur

Vous pouvez désactiver les cookies dans les paramètres de votre navigateur.

#### Données de Journal

Notre serveur collecte automatiquement:
- Adresse IP
- Type et version du navigateur
- Système d'exploitation
- Pages visitées
- Heures d'accès

Ces données sont utilisées pour:
- Sécurité du serveur et diagnostic des erreurs
- Analyse de l'utilisation du site
- Amélioration des services

## 4. Partage des Données

Vos données personnelles ne sont pas partagées avec des tiers, sauf:

- **Obligation légale**: Si exigé par la loi
- **Fournisseurs de services**: Services d'hébergement et bases de données
- **Services IA**: API Google Gemini pour la génération de recettes
- **Avec votre consentement**: À d'autres fins uniquement avec permission explicite

## 5. Sécurité des Données

Nous mettons en œuvre des mesures techniques et organisationnelles pour protéger vos données:
- Chiffrement SSL/TLS pour la transmission de données
- Mots de passe hachés dans la base de données
- Vérifications de sécurité régulières
- Contrôle d'accès et gestion des permissions

## 6. Conservation des Données

- **Compte utilisateur**: Tant que votre compte est actif, puis 30 jours
- **Recettes et listes**: Tant que vous souhaitez les conserver
- **Données de journal**: 30 jours
- **Cookies**: Selon le type, entre fin de session et 1 an

## 7. Vos Droits

Vous disposez des droits suivants en vertu du RGPD:

### 7.1 Droit d'Accès (Art. 15 RGPD)
Vous pouvez demander des informations sur les données personnelles que nous traitons vous concernant.

### 7.2 Droit de Rectification (Art. 16 RGPD)
Vous pouvez demander la correction de données personnelles inexactes.

### 7.3 Droit à l'Effacement (Art. 17 RGPD)
Sous certaines conditions, vous pouvez demander la suppression de vos données personnelles.

### 7.4 Droit à la Limitation du Traitement (Art. 18 RGPD)
Vous pouvez demander la limitation du traitement de vos données.

### 7.5 Droit à la Portabilité (Art. 20 RGPD)
Vous pouvez obtenir vos données dans un format structuré et courant.

### 7.6 Droit d'Opposition (Art. 21 RGPD)
Vous pouvez vous opposer au traitement de vos données.

### 7.7 Droit de Retrait du Consentement
Vous pouvez retirer votre consentement au traitement des données à tout moment.

## 8. Délégué à la Protection des Données

Pour des questions sur la protection des données, contactez-nous à:
- Email: privacy@resta-rampe.de
- Adresse: Resta Rampe, [Votre adresse]

## 9. Droit de Plainte

Vous avez le droit de déposer une plainte auprès d'une autorité de protection des données.

## 10. Modifications de la Politique de Confidentialité

Nous nous réservons le droit de mettre à jour cette politique de confidentialité à tout moment. Nous vous notifierons des modifications importantes.

## 11. Contact

Pour des questions, préoccupations ou demandes concernant cette politique de confidentialité, vous pouvez nous contacter à:
- Email: privacy@resta-rampe.de
- Site Web: resta-rampe.de
"""
    },
    "ja": {
        "slug": "privacy",
        "title": "プライバシーポリシー",
        "content": """# プライバシーポリシー

**最終更新: 2025年10月29日**

## 1. 責任者

Resta Rampe
メール: privacy@resta-rampe.de

## 2. データ処理に関する一般情報

### 2.1 個人データ処理の範囲

当社は、機能的なウェブサイトおよび当社のコンテンツとサービスを提供するために必要な範囲でのみ、ユーザーの個人データを処理します。

### 2.2 法的根拠

個人データの処理は以下に基づいています:
- GDPR第6条第1項a (同意)
- GDPR第6条第1項b (契約の履行)
- GDPR第6条第1項c (法的義務)
- GDPR第6条第1項f (正当な利益)

## 3. データの収集と処理

### 3.1 登録とユーザーアカウント

当社のウェブサイトに登録する場合、当社は以下を収集します:
- ユーザー名
- メールアドレス
- パスワード (暗号化)
- 登録日

このデータは以下の目的で処理されます:
- ユーザーアカウントの作成
- 認証
- サービスの提供

### 3.2 レシピとショッピングリスト

レシピを作成またはショッピングリストを管理する場合、当社は以下を保存します:
- レシピ情報と材料
- ショッピングリストとその内容
- 作成・変更日時

このデータはこれらの機能を提供する目的でのみ使用されます。

### 3.3 人工知能と生成

AI機能(例:レシピ提案)を使用する場合、お客様のリクエストと材料はGoogle Geminiに送信されます。Googleのプライバシーポリシーをご確認ください。

### 3.4 自動データ収集

#### クッキーとストレージ技術

当社のウェブサイトはクッキーを使用して以下を保存します:
- 認証情報 (セッショントークン)
- 言語設定
- ユーザー設定

ブラウザの設定でクッキーを無効にできます。

#### ログデータ

当社のサーバーは自動的に以下を収集します:
- IPアドレス
- ブラウザタイプとバージョン
- オペレーティングシステム
- 訪問ページ
- アクセス時刻

このデータは以下に使用されます:
- サーバーセキュリティとエラー診断
- ウェブサイト利用分析
- サービス改善

## 4. データの共有

個人データは以下の場合を除き、第三者と共有されません:

- **法的義務**: 法律で要求される場合
- **サービスプロバイダ**: ホスティングとデータベースサービス
- **AIサービス**: レシピ生成用Google Gemini API
- **同意を得て**: その他の目的での明示的な許可がある場合

## 5. データセキュリティ

当社はデータを保護するための技術的および組織的措置を実装しています:
- データ送信用SSL/TLS暗号化
- データベースでのハッシュ化されたパスワード
- 定期的なセキュリティチェック
- アクセス制御と権限管理

## 6. データ保持

- **ユーザーアカウント**: アカウントがアクティブな限り、その後30日間
- **レシピとリスト**: 保存を希望する限り
- **ログデータ**: 30日間
- **クッキー**: タイプによりセッション終了から1年

## 7. お客様の権利

GDPRに基づく以下の権利があります:

### 7.1 アクセス権
お客様について当社が処理する個人データについて情報をリクエストできます。

### 7.2 修正権
不正確な個人データの修正をリクエストできます。

### 7.3 削除権
特定の条件下で個人データの削除をリクエストできます。

### 7.4 処理制限権
データ処理の制限をリクエストできます。

### 7.5 データポータビリティ権
データを構造化された一般的な形式で取得できます。

### 7.6 異議申し立て権
データ処理に異議を唱えることができます。

### 7.7 同意撤回権
データ処理への同意をいつでも撤回できます。

## 8. データ保護役員

データ保護についての質問は以下までお問い合わせください:
- メール: privacy@resta-rampe.de
- 住所: Resta Rampe, [お客様の住所]

## 9. 苦情申し立て権

データ保護当局に苦情申し立てを行う権利があります。

## 10. プライバシーポリシーの変更

このプライバシーポリシーはいつでも更新する権利を留保します。重要な変更についてはお知らせします。

## 11. お問い合わせ

このプライバシーポリシーに関するご質問、ご不明な点、またはご要望については、以下までお問い合わせください:
- メール: privacy@resta-rampe.de
- ウェブサイト: resta-rampe.de
"""
    },
    "tr": {
        "slug": "privacy",
        "title": "Gizlilik Politikası",
        "content": """# Gizlilik Politikası

**Son Güncelleme: 29 Ekim 2025**

## 1. Sorumlu Kişi

Resta Rampe
E-posta: privacy@resta-rampe.de

## 2. Veri İşlemeyle İlgili Genel Bilgiler

### 2.1 Kişisel Veri İşlemesinin Kapsamı

Kullanıcıların kişisel verilerini yalnızca işlevsel bir web sitesi ve hizmetlerimiz sağlamak için gerekli ölçüde işleriz.

### 2.2 Yasal Dayanak

Kişisel verilerin işlenmesi aşağıdakılara dayanmaktadır:
- GDPR Madde 6 Paragraf 1 a (Rıza)
- GDPR Madde 6 Paragraf 1 b (Sözleşmenin Yerine Getirilmesi)
- GDPR Madde 6 Paragraf 1 c (Yasal Yükümlülük)
- GDPR Madde 6 Paragraf 1 f (Meşru İlişkiler)

## 3. Veri Toplama ve İşleme

### 3.1 Kayıt ve Kullanıcı Hesabı

Web sitemize kaydolduğunuzda, aşağıdakileri toplarız:
- Kullanıcı adı
- E-posta adresi
- Şifre (şifrelenmiş)
- Kayıt tarihi

Bu veriler aşağıdaki amaçlarla işlenir:
- Kullanıcı hesabı oluşturmak
- Sizi kimlik doğrulamak
- Hizmetlerimizi sağlamak

### 3.2 Tarifler ve Alışveriş Listeleri

Tarifler oluşturduğunuzda veya alışveriş listelerini yönettiğinizde, aşağıdakileri depolayız:
- Tarif bilgileri ve malzemeler
- Alışveriş listeleri ve içerikleri
- Oluşturma ve değiştirme zaman damgaları

Bu veriler yalnızca bu özellikler sağlamak amacıyla kullanılır.

### 3.3 Yapay Zeka ve Üretim

Yapay zeka özelliklerini (örn. tarif önerileri) kullandığınızda, istekleriniz ve malzemeleriniz Google Gemini'ye gönderilir. Lütfen Google'ın gizlilik politikasını inceleyin.

### 3.4 Otomatik Veri Toplama

#### Çerezler ve Depolama Teknolojileri

Web sitemiz aşağıdakileri depolamak için çerezleri kullanır:
- Kimlik doğrulama bilgileri (oturum belirteçleri)
- Dil ayarları
- Kullanıcı tercihleri

Tarayıcı ayarlarınızda çerezleri devre dışı bırakabilirsiniz.

#### Günlük Verileri

Sunucumuz otomatik olarak aşağıdakileri toplar:
- IP adresi
- Tarayıcı türü ve sürümü
- İşletim sistemi
- Ziyaret edilen sayfalar
- Erişim saatleri

Bu veriler aşağıdakiler için kullanılır:
- Sunucu güvenliği ve hata tanılaması
- Web sitesi kullanım analizi
- Hizmet iyileştirmesi

## 4. Veri Paylaşımı

Kişisel verileriniz aşağıdakiler hariç üçüncü taraflarla paylaşılmaz:

- **Yasal Yükümlülük**: Kanun tarafından istenirse
- **Hizmet Sağlayıcıları**: Barındırma ve veritabanı hizmetleri
- **Yapay Zeka Hizmetleri**: Tarif üretimi için Google Gemini API
- **Rızanızla**: Diğer amaçlar için yalnızca açık izin ile

## 5. Veri Güvenliği

Verilerinizi korumak için teknik ve örgütsel önlemler uygularız:
- Veri aktarımı için SSL/TLS şifrelemesi
- Veritabanında karma hale getirilmiş şifreler
- Düzenli güvenlik kontrolleri
- Erişim kontrolü ve izin yönetimi

## 6. Veri Saklama

- **Kullanıcı hesabı**: Hesabınız aktif olduğu sürece, sonra 30 gün
- **Tarifler ve listeler**: Depolamak istediğiniz sürece
- **Günlük verileri**: 30 gün
- **Çerezler**: Türüne bağlı olarak oturum sonu ile 1 yıl arası

## 7. Haklarınız

GDPR uyarınca aşağıdaki haklara sahipsiniz:

### 7.1 Erişim Hakkı
Hakkınızda işlediğimiz kişisel veriler hakkında bilgi isteyebilirsiniz.

### 7.2 Düzeltme Hakkı
Yanlış kişisel verilerin düzeltilmesini isteyebilirsiniz.

### 7.3 Silme Hakkı
Belirli koşullar altında kişisel verilerinizin silinmesini isteyebilirsiniz.

### 7.4 İşleme Kısıtlama Hakkı
Verilerinizin işlenmesinin kısıtlanmasını isteyebilirsiniz.

### 7.5 Veri Taşınabilirliği Hakkı
Verilerinizi yapılandırılmış bir yaygın biçimde alabilirsiniz.

### 7.6 İtiraz Hakkı
Verilerinizin işlenmesine itiraz edebilirsiniz.

### 7.7 Rıza Geri Çekme Hakkı
Veri işlemesine verilen rızanızı istediğiniz zaman geri çekebilirsiniz.

## 8. Veri Koruma Sorumlusu

Veri koruması hakkında sorular için aşağıdadır iletişim kurun:
- E-posta: privacy@resta-rampe.de
- Adres: Resta Rampe, [Adresiniz]

## 9. Şikayet Hakkı

Bir veri koruma otoritesine şikayet açma hakkınız vardır.

## 10. Gizlilik Politikasında Değişiklikler

Bu gizlilik politikasını istediğimiz zaman güncelleme hakkını saklı tutarız. Önemli değişiklikler hakkında sizi bilgilendireceğiz.

## 11. İletişim

Bu gizlilik politikası hakkında sorularınız, endişeleriniz veya taleplerle ilgili olarak bizimle iletişim kurun:
- E-posta: privacy@resta-rampe.de
- Web sitesi: resta-rampe.de
"""
    },
    "fa": {
        "slug": "privacy",
        "title": "سياسة الخصوصية",
        "content": """# سياسة الخصوصية

**آخر تحديث: 29 أكتوبر 2025**

## 1. المسؤول

Resta Rampe
البريد الإلكتروني: privacy@resta-rampe.de

## 2. معلومات عامة عن معالجة البيانات

### 2.1 نطاق معالجة البيانات الشخصية

نحن نعالج بيانات المستخدمين الشخصية فقط بالقدر الضروري لتوفير موقع ويب وخدماتنا.

### 2.2 الأساس القانوني

تعتمد معالجة البيانات الشخصية على:
- المادة 6 الفقرة 1 أ من اللائحة العامة لحماية البيانات (الموافقة)
- المادة 6 الفقرة 1 ب من اللائحة العامة لحماية البيانات (تنفيذ العقد)
- المادة 6 الفقرة 1 ج من اللائحة العامة لحماية البيانات (الالتزام القانوني)
- المادة 6 الفقرة 1 و من اللائحة العامة لحماية البيانات (المصالح المشروعة)

## 3. جمع ومعالجة البيانات

### 3.1 التسجيل وحساب المستخدم

عند التسجيل على موقعنا، نجمع:
- اسم المستخدم
- عنوان البريد الإلكتروني
- كلمة المرور (مشفرة)
- تاريخ التسجيل

يتم معالجة هذه البيانات لـ:
- إنشاء حسابك
- المصادقة عليك
- توفير خدماتنا

### 3.2 الوصفات وقوائم التسوق

عند إنشاء وصفات أو إدارة قوائم التسوق، نقوم بتخزين:
- معلومات الوصفات والمكونات
- قوائم التسوق ومحتوياتها
- طوابع الإنشاء والتعديل الزمنية

يتم استخدام هذه البيانات فقط لتوفير هذه الميزات.

### 3.3 الذكاء الاصطناعي والإنشاء

عند استخدام ميزات الذكاء الاصطناعي (مثل اقتراحات الوصفات)، يتم إرسال طلباتك ومكوناتك إلى Google Gemini. يرجى مراجعة سياسة الخصوصية من Google.

### 3.4 جمع البيانات التلقائي

#### ملفات تعريف الارتباط وتقنيات التخزين

يستخدم موقعنا ملفات تعريف الارتباط لتخزين:
- معلومات المصادقة (رموز الجلسة)
- إعدادات اللغة
- تفضيلات المستخدم

يمكنك تعطيل ملفات تعريف الارتباط في إعدادات المتصفح.

#### بيانات السجل

يجمع الخادم الخاص بنا تلقائياً:
- عنوان IP
- نوع المتصفح والإصدار
- نظام التشغيل
- الصفحات المزارة
- أوقات الوصول

يتم استخدام هذه البيانات لـ:
- أمان الخادم وتشخيص الأخطاء
- تحليل استخدام الموقع
- تحسين الخدمات

## 4. مشاركة البيانات

لا يتم مشاركة بيانات المستخدم الشخصية مع أطراف ثالثة، باستثناء:

- **الالتزام القانوني**: إذا تطلبت القانون
- **مقدمو الخدمات**: خدمات الاستضافة وقواعد البيانات
- **خدمات الذكاء الاصطناعي**: واجهة Google Gemini API لإنشاء الوصفات
- **بموافقتك**: لأغراض أخرى فقط بإذن صريح

## 5. أمان البيانات

ننفذ تدابير تقنية وتنظيمية لحماية بيانات:
- تشفير SSL/TLS لنقل البيانات
- كلمات المرور المشفرة في قاعدة البيانات
- فحوصات أمان دورية
- التحكم بالوصول وإدارة الأذونات

## 6. احتفاظ البيانات

- **حساب المستخدم**: طالما كان حسابك نشطاً، ثم 30 يوماً
- **الوصفات والقوائم**: طالما تريد تخزينها
- **بيانات السجل**: 30 يوم
- **ملفات تعريف الارتباط**: حسب النوع، بين نهاية الجلسة و 1 سنة

## 7. حقوقك

لديك الحقوق التالية بموجب اللائحة العامة لحماية البيانات:

### 7.1 حق الوصول
يمكنك طلب معلومات حول البيانات الشخصية التي نعالجها عنك.

### 7.2 حق التصحيح
يمكنك طلب تصحيح البيانات الشخصية غير الدقيقة.

### 7.3 حق الحذف
في ظل ظروف معينة، يمكنك طلب حذف بيانات المستخدم الشخصية.

### 7.4 حق تقيد المعالجة
يمكنك طلب تقيد معالجة بيانات المستخدم.

### 7.5 حق نقل البيانات
يمكنك الحصول على بيانات المستخدم بصيغة منظمة وشائعة الاستخدام.

### 7.6 حق الاعتراض
يمكنك الاعتراض على معالجة بيانات المستخدم.

### 7.7 حق سحب الموافقة
يمكنك سحب موافقتك على معالجة البيانات في أي وقت.

## 8. مسؤول حماية البيانات

لأسئلة حول حماية البيانات، اتصل بنا على:
- البريد الإلكتروني: privacy@resta-rampe.de
- العنوان: Resta Rampe، [عنوانك]

## 9. حق تقديم شكوى

لديك الحق في تقديم شكوى إلى سلطة حماية البيانات.

## 10. التغييرات على سياسة الخصوصية

نحتفظ بالحق في تحديث سياسة الخصوصية هذه في أي وقت. سيتم إخطارك بالتغييرات المهمة.

## 11. اتصل بنا

لأي أسئلة أو مخاوف أو طلبات تتعلق بسياسة الخصوصية هذه، يمكنك الاتصال بنا على:
- البريد الإلكتروني: privacy@resta-rampe.de
- الموقع الإلكتروني: resta-rampe.de
"""
    },
    "nds": {
        "slug": "privacy",
        "title": "Datenschutzerkläring",
        "content": """# Datenschutzerkläring

**Toletzt aktualisiert: 29. Oktober 2025**

## 1. Verantwortlick

Resta Rampe
E-Mail: privacy@resta-rampe.de

## 2. Allgemeen Informatschonen zur Datenverarweitung

### 2.1 Umfang vun Datenverarweitung

Wi verarbeiten personlige Daten vun Nutzer blot in de Umfang, as dat nödig is för en funktschionaale Webseite un unse Inhalt un Leistungen.

### 2.2 Rechtliche Grundlage

De Verarbeitung vun personligen Daten geschüüt op Grundlag vun:
- Art. 6 Abs. 1 a) DSGVO (Inwilligung)
- Art. 6 Abs. 1 b) DSGVO (Vertragserfüllung)
- Art. 6 Abs. 1 c) DSGVO (Rechtsverpflichtung)
- Art. 6 Abs. 1 f) DSGVO (berechtigte Interessen)

## 3. Datenaufnahm un -verarbeitung

### 3.1 Registrering un Nutzerkontu

Wenn du de up unse Webseite registreerst, sammeln wi:
- Nutzernaam
- E-Mail-Adreschse
- Passwort (verschlüsselt)
- Registreringsdatum

Disse Daten ward verarbeitet föör:
- Din Nutzerkontu to schaffen
- Dik to authenticieren
- Unse Servichsen to stellen

### 3.2 Rezepte un Shoppinlisten

Wenn du Rezepte schaffst oder Shoppin-Listen verwaltst, speicheren wi:
- Rezeptinformatschonen un Zutaten
- Shoppin-Listen un deren Inhalt
- Tietstemel vun Schaffen un Ännerung

Disse Daten ward blot for de Stellen vun desse Funktschionen bruukt.

### 3.3 Künstliche Intelligenz un Generateschon

Wenn du KI-Funktschionen (z.B. Rezeptvorschläge) bruukst, werden dien Anfragen un Zutaten to Google Gemini stoken. Plees Google de Datenschutzrichtlinie angeken.

### 3.4 Automatische Datenaufnahm

#### Cookies un Speicherteknologien

Unse Webseite bruukt Cookies för de Speicherung vun:
- Authentificierungsinformatschonen (Session-Tokens)
- Spraakinstellen
- Nutzerinstellen

Du kannst Cookies in dien Browserinstellen utmaken.

#### Log-Daten

Unse Server sammelt automatisch:
- IP-Adreschse
- Browsertyp un -version
- Bedienungssystem
- Besökte Siden
- Tottidpunkte

Disse Daten ward bruukt föör:
- Serversekerheit un Fehlerfeststellung
- Analyse vun Webseitenbenutzung
- Verbesserung vun unsen Servichsen

## 4. Wietergaav vun Daten

Dien personlige Daten ward an Dritte neet weitergeven, außer:

- **Rechtsverpflichtung**: Wenn dat Gesetz dat vorschreibt
- **Servichsanbieder**: Hosting- un Datenbankenservichsen
- **KI-Servichsen**: Google Gemini API föör Rezeptgenerierung
- **Mit dien Inwilligung**: För andere Zwecke blot mit dien ausdrücklike Erlaupnis

## 5. Datensekerheit

Wi stellen technische un organisatorische Maßnahmen to Schutz vun dien Daten em:
- SSL/TLS-Verschlüsselung föör Datentransfer
- Verschlüsselde Passwörter in de Datenbank
- Regelmaßige Sekeheitsüberpröfungen
- Togangskontrall un Berchtigungsverwaltung

## 6. Speicherdauer

- **Nutzerkontu**: So lang as dien Kontu aktiv is, danach 30 Daag
- **Rezepte un Listen**: So lang as du desse speichern wullst
- **Log-Daten**: 30 Daag
- **Cookies**: Je no Sorte twüschen Sessionende un 1 Jaar

## 7. Dien Rechte

Du hast disse Rechte no DSGVO:

### 7.1 Auskunftsrecht
Du kannst Auskunft darum bidden, welke personlige Daten wi över de verarbeiten.

### 7.2 Berichtigungsrecht
Du kannst de Berichtiging vun onjüstigen personligen Daten bidden.

### 7.3 Löschungsrecht
Under besünnere Bedingungen kannst du de Löschung vun dien personligen Daten bidden.

### 7.4 Recht auf Einschränkung de Verarbeitung
Du kannst de Einschränkung vun Verarbeitung vun dien Daten bidden.

### 7.5 Recht op Datentransferbarkeit
Du kannst dien Daten in en struktureerd, gebru

iklik Format kriegen.

### 7.6 Widerspruchsrecht
Du kannst de Verarbeitung vun dien Daten widerspräken.

### 7.7 Recht op Wiederroop de Inwilligung
Du kannst dien Inwilligung to Datenverarbeitung jedertiid toruchtrekken.

## 8. Datenschutzverantwortlicker

Föör Fraajen to Datenschutz kontakteert us unner:
- E-Mail: privacy@resta-rampe.de
- Adreschse: Resta Rampe, [Dien Adreschse]

## 9. Recht op Beschwärt

Du hast dat Recht, bi en Datenschutzbehoerde en Beschwärt intobauen.

## 10. Ännerungen disse Datenschutzerkläring

Wi behalten us dat Recht, disse Datenschutzerkläring jedertiid to ännern. Wi will de över wichtige Ännerungen unterrichten.

## 11. Kontakt

Föör Fraagen, Bedenken oder Anfragen to disse Datenschutzerkläring kannst du us unterkuntakt:
- E-Mail: privacy@resta-rampe.de
- Webseite: resta-rampe.de
"""
    }
}

# Get or create pages
@router.get("/pages/public/{slug}")
def get_public_page(slug: str, language: str = Query("de"), db: Session = Depends(get_db)):
    """Get a public page by slug and language"""
    print(f"🔍 get_public_page called: slug={slug}, language={language}")
    # Get from database first - prioritize real data
    page = db.query(Page).filter(Page.slug == slug, Page.language == language).first()
    
    if page:
        print(f"✅ Found page: {page.language} - {page.title}")
        return PageResponse(
            id=page.id,
            slug=page.slug,
            title=page.title,
            content=page.content,
            language=page.language,
            page_key=page.page_key,
            updated_at=page.updated_at
        )
    
    print(f"❌ Page not found for slug={slug}, language={language}")
    # If not found, return 404 (don't fallback to hardcoded)
    raise HTTPException(status_code=404, detail="Page not found")


@router.get("/pages")
def get_all_pages(current_user: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Get all pages (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    pages = db.query(Page).all()
    return [
        PageResponse(
            id=page.id,
            slug=page.slug,
            title=page.title,
            content=page.content,
            language=page.language,
            page_key=page.page_key,
            updated_at=page.updated_at
        )
        for page in pages
    ]


@router.get("/pages/{page_id}")
def get_page(page_id: int, current_user: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Get a specific page by ID (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    return PageResponse(
        id=page.id,
        slug=page.slug,
        title=page.title,
        content=page.content,
        language=page.language,
        page_key=page.page_key,
        updated_at=page.updated_at
    )


@router.post("/pages")
def create_page(page: PageCreate, current_user: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Create a new page (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    new_page = Page(
        slug=page.slug,
        title=page.title,
        content=page.content,
        language=page.language,
        page_key=page.page_key
    )
    db.add(new_page)
    db.commit()
    db.refresh(new_page)
    return PageResponse(
        id=new_page.id,
        slug=new_page.slug,
        title=new_page.title,
        content=new_page.content,
        language=new_page.language,
        page_key=new_page.page_key,
        updated_at=new_page.updated_at
    )


@router.put("/pages/{page_id}")
def update_page(page_id: int, page: PageUpdate, current_user: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Update a page (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    if page.slug:
        db_page.slug = page.slug
    if page.title:
        db_page.title = page.title
    if page.content:
        db_page.content = page.content
    if page.language:
        db_page.language = page.language
    
    db.commit()
    db.refresh(db_page)
    return PageResponse(
        id=db_page.id,
        slug=db_page.slug,
        title=db_page.title,
        content=db_page.content,
        language=db_page.language,
        page_key=db_page.page_key,
        updated_at=db_page.updated_at
    )


@router.delete("/pages/{page_id}")
def delete_page(page_id: int, current_user: User = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Delete a page (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db_page = db.query(Page).filter(Page.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    db.delete(db_page)
    db.commit()
    return {"message": "Page deleted successfully"}
