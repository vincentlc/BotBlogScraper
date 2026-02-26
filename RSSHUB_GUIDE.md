# RSSHub Instagram Scraper - Guía de Uso

## ¿Qué es RSSHub?

RSSHub es un generador de feeds RSS/Atom de código abierto que convierte sitios web en feeds estándar. Permite scrappear Instagram, TikTok, Twitter y muchas otras plataformas sin necesidad de APIs oficiales.

## Instalación de RSSHub (Opcional)

Si quieres ejecutar RSSHub localmente:

```bash
# Con Docker (recomendado)
docker run -d -p 1200:1200 diginext/rsshub

# Con Node.js
git clone https://github.com/DIYgod/RSSHub.git
cd RSSHub
npm install
npm start
```

Luego accede en `http://localhost:1200`

O usa la instancia pública: `https://rsshub.app`

## Rutas Disponibles para Instagram

```
/instagram/user/{username}     - Posts del usuario
/instagram/hashtag/{hashtag}   - Posts con hashtag
/instagram/explore/locations   - Locations populares
```

Ejemplo: `https://rsshub.app/instagram/user/municipiopuertovaras`

## Uso en el Proyecto

### 1. **Tests Unitarios** (Sin conexión real)

```bash
pytest tests/test_blog_scraper.py::test_rsshub_instagram_scraper -v
pytest tests/test_blog_scraper.py::test_rsshub_url_construction -v
```

Estos tests verifican que:
- La URL del feed se construye correctamente
- El scraper puede procesar entradas del feed
- La validación de items funciona

### 2. **Prueba Real** (Requiere RSSHub accesible)

```bash
# Usar instancia pública de RSSHub
python test_rsshub_real.py --username municipiopuertovaras

# Usar instancia local
python test_rsshub_real.py --rsshub-base http://localhost:1200 --username municipiopuertovaras

# Probar múltiples cuentas
python test_rsshub_real.py
```

### 3. **Usar en tu Bot**

Edita `src/scrapers/scraper_init.py`:

```python
from src.scrapers.blog import RssHubScraper

def get_scrapers(config):
    return [
        # Instagram Puerto Varas
        RssHubScraper(
            route='/instagram/user/municipiopuertovaras',
            site_name='Puerto Varas',
            rsshub_base='https://rsshub.app'  # o tu instancia local
        ),
        # Más scrapers...
    ]
```

## Rutas de RSSHub Soportadas

### Instagram
- `/instagram/user/{username}` - Timeline del usuario
- `/instagram/hashtag/{hashtag}` - Posts con hashtag
- `/instagram/story/{username}` - Stories (si están disponibles públicamente)

### Otros (Ejemplos)
- `/twitter/user/{user}` - Tweets
- `/tiktok/user/{user}` - Videos de TikTok
- `/youtube/channel/{id}` - Videos de YouTube
- `/reddit/subreddit/{name}` - Posts de Reddit

[Ver documentación completa de RSSHub](https://docs.rsshub.app/)

## Limitaciones

1. **Rate Limiting**: RSSHub tiene límites de requests. La instancia pública es más lenta.
2. **Disponibilidad**: Algunos feeds pueden no estar disponibles según las políticas del sitio.
3. **Retraso**: Los feeds generalmente tienen un retraso de minutos a horas.
4. **Autenticación**: Algunos contenidos privados no son accesibles.

## Solución de Problemas

### "No entries found in feed"
- Verifica que la ruta sea correcta: `{rsshub_base}/{route}`
- Comprueba que el usuario/hashtag existe
- Si usas instancia pública, espera un poco (podría estar en caché)

### "Connection error"
- Verifica que RSSHub esté accesible
- Si usas local: `docker ps` para verificar que el contenedor corre
- Si usas público: intenta acceder a https://rsshub.app directamente

### Feed vacío
- Algunos usuarios/hashtags pueden no tener feeds generados
- Intenta otro usuario/hashtag para verificar que funciona

## Ejemplo Completo

```python
import asyncio
from src.scrapers.blog import RssHubScraper

async def main():
    # Crear scraper para Puerto Varas Instagram
    scraper = RssHubScraper(
        route='/instagram/user/municipiopuertovaras',
        site_name='Puerto Varas Instagram',
        rsshub_base='https://rsshub.app'
    )
    
    # Fetch latest post
    latest = await scraper.fetch_latest()
    
    if latest:
        print(f"Título: {latest.title}")
        print(f"URL: {latest.url}")
        print(f"Autor: {latest.content['author']}")
    else:
        print("No posts found")

if __name__ == '__main__':
    asyncio.run(main())
```

## Referencias

- [RSSHub Documentación](https://docs.rsshub.app/)
- [RSSHub GitHub](https://github.com/DIYgod/RSSHub)
- [Instancia Pública](https://rsshub.app)
