# Airtable Public Table Scraper

Este componente permite monitorear una tabla pública de Airtable sin necesidad de una API key.

## Uso

En tu archivo main.py:

```python
from src.scrapers.airtable import AirtableScraper

# Crear instancia del scraper
airtable_scraper = AirtableScraper(
    base_id="appCHAnr1cEoCNE09",    # ID de la base de Airtable
    table_id="tblgd1rCOBwes8Jxg",   # ID de la tabla
    view_id="shrjIeSkRAVktIaJe"     # ID de la vista (opcional)
)

# Agregar a la lista de scrapers
scrapers.append(airtable_scraper)
```

## Cómo encontrar los IDs

1. En la URL de tu tabla de Airtable:
   ```
   https://airtable.com/appCHAnr1cEoCNE09/shrjIeSkRAVktIaJe/tblgd1rCOBwes8Jxg
   ```
   - `appCHAnr1cEoCNE09` es el base_id
   - `tblgd1rCOBwes8Jxg` es el table_id
   - `shrjIeSkRAVktIaJe` es el view_id

## Países Monitoreados

El scraper monitorea actualizaciones para:
- Chile
- Argentina
- Perú
- Colombia
- México

Para testing, también acepta registros de "Austria".