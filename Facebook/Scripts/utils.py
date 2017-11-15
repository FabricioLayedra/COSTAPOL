import facebook
import pandas as pd

def initialize(token,versioning=2.10):
	graph = facebook.GraphAPI(access_token=token, version=versioning)
	return graph


def get_username(url):
    url=str(url)
    url = url.strip()
    try:
        domain,username = url.split("https://www.facebook.com/")
        username = username.strip("/")
        return username
    except:
        return "unknown"

#Solo funciona si el perfil es público, caso contrario arroja 0
def getIDbyusername(dataframe):
    username = dataframe.apply(get_username)
    print username[1]
    try:
        id_user = graph.request("%s?fields=id&format=json"%username)
        return id_user['id']
    except:
        return 0


df = pd.read_csv(filename)
df["facebook_id"]=df.apply(getIDbyusername,axis=1)