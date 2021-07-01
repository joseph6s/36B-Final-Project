import twitter

# api oAuth details
c_key = 'YuSXt1CbvOQs5oRLvkht2hegZ'
private_key = 'vKkcnp3ymNv50CxKnXLpHL5FZwcEiO3eSmJeAILPIyLuyFdJuD'
token = '1328852933887225856-i8pyYfFqwCsm1n5a6EdAkJTX0qUmoA'
token_secret = 'G6u77Y8ls07nqHmSouD4kdARMUyx9GMTKTg9HOoTby6i9'

# connecting to api
api = twitter.Api(
                consumer_key=c_key,
                consumer_secret=private_key,
                access_token_key=token,
                access_token_secret=token_secret
                )

#checking if we are connected 
print(api.VerifyCredentials())
