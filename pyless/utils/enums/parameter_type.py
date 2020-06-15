class ParameterType:
    """Parameter Types are all based off of aws api-gateway lambda proxy integration requests
    (you set this up when creating the route and should be required for all routes in this framework)"""
    # Parameters that come in through defined variable paths
    # in api gateway usually looks like {example+} in the resources tab www.s.com/user/{userid+}
    PATH = "path"
    # Should come in as RAW JSON from a post request
    BODY = "body"
    # any parameter that comes in via a get request usually as a query
    # Example: www.ex.com/test?exampleVar=Helloworld
    QUERY = "query"
