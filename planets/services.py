import requests


def fetch_planets_service():
    url = "https://swapi-graphql.netlify.app/.netlify/functions/index"
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
    response = requests.post(url, json={'query': query})
    data = response.json()

    # Extract the planet list
    return data['data']['allPlanets']['planets']
