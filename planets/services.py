import requests


def fetch_planets_service():
    url = "https://swapi-graphql.netlify.app/graphql"
    query = """
    query {
      allPlanets {
        planets {
          name
          population
          terrains
          climates
        }
      }
    }
    """
    response = requests.post(
            url,
            json={'query': query},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
    data = response.json()

    # Extract the planet list
    return data['data']['allPlanets']['planets']
