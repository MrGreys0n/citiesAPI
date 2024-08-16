from views import add_city, delete_city, get_all_cities, get_city, get_nearest_cities


def setup_routes(app):
    app.router.add_route('POST', '/cities', add_city)
    app.router.add_route('DELETE', '/cities/{city_name}', delete_city)
    app.router.add_route('GET', '/cities', get_all_cities)
    app.router.add_route('GET', '/cities/{city_name}', get_city)
    app.router.add_route('GET', '/nearest_cities', get_nearest_cities)
