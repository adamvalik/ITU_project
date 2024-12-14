========================================================
                Adresářová struktura:
             klíčové soubory a autorství
========================================================
.
├=======================================================
├── backend
│   ├── Dockerfile - sestavení kontejneru pro BE
│   ├── main.py
│   ├── managers - rozhraní pro komunikaci s databází
│   ├── models - struktura dat v databázi
│   ├── redisClient.py - inicializace klienta databáze
│   └── routers - API endpointy
├=======================================================
├── docker-compose.yml (xvalik05) - sestavení aplikace
├=======================================================
├── frontend
│   ├── Dockerfile - sestavení kontejneru pro FE
│   ├── src
│   │   ├── App.vue (xvalik05)
│   │   ├── components
│   │   │   ├── MapCreatorComponents
│   │   │   │   ├── BackendOperations.js (xeffen00)
│   │   │   │   ├── OperationSelector.vue (xeffen00)
│   │   │   │   ├── RenderingScreen.vue (xeffen00)
│   │   │   │   ├── SaveMap.vue (xeffen00)
│   │   │   │   └── ThemeSelector.vue (xeffen00)
│   │   │   ├── Selectors
│   │   │   │   ├── SkillHint.vue (xvalik05)
│   │   │   │   ├── SkillSelector.vue (xvalik05)
│   │   │   │   └── TankSelector.vue (xvalik05)
│   │   │   ├── Settings
│   │   │   │   ├── BackgroundMusic.vue (xvalik05)
│   │   │   │   └── Settings.vue (xvalik05)
│   │   │   └── Shop
│   │   │       ├── PlayerShopCard.vue (xhorut01)
│   │   │       ├── SkillDetail.vue (xhorut01)
│   │   │       ├── SkillShop.vue (xhorut01)
│   │   │       ├── SkillShopItem.vue (xhorut01)
│   │   │       ├── TankImage.vue (xhorut01)
│   │   │       ├── WeaponDetail.vue (xhorut01)
│   │   │       ├── WeaponShop.vue (xhorut01)
│   │   │       └── WeaponShopItem.vue (xhorut01)
│   │   └── views
│   │       ├── ChooseMapView.vue (xvalik05)
│   │       ├── ChooseTankView.vue (xvalik05)
│   │       ├── GameScreen.vue (xhejni00)
│   │       ├── MainPage.vue (xvalik05)
│   │       ├── MapCreator.vue (xeffen00)
│   │       └── ShopView.vue (xhorut01)
├=======================================================
