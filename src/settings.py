OutputDir="/var/www/my_status_page/"
Websites=[

    {
        "name": "Autotaglibro development",
        "url": "http://127.0.0.1:8000/TestConnection",
        "test_method": "json",
        "status": "database connection ok"
    },
    {
        "name": "Autotaglibro",
        "url": "https://auto-taglibro.bdempc.pl/TestConnection",
        "test_method": "json",
        "status": "database connection ok"
    },
    {
        "name": "Autotaglibro staging",
        "url": "https://auto-taglibro.bdempc.pl/TestConnection",
        "test_method": "jsodn",
        "status": "database connection ok"
    },
    {
        "name": "DGallery",
        "url": "https://zdjecia.bdempc.pl/TestConnection",
        "test_method": "json",
        "status": "database connection ok"
    },
    {
        "name": "Gogs",
        "url": "https://git.bdempc.pl/",
        "test_method": "http_code",
        "result": "200"
    }
]
