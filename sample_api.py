import json
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    location: str
    page: int


class UPRN(BaseModel):
    uprn: str

@app.post("/propertysearch")
def fetch_sold(item: Item):
    url = 'https://api-graphql-lambda.prod.zoopla.co.uk/graphql/'
    headers = {
        "accept": "*/*",
        "x-api-key": "3Vzj2wUfaP3euLsV4NV9h3UAVUR3BoWd5clv9Dvu",
        "origin": "zoopla-mobile-app",
        "Content-Type": "application/json",
        "Content-Length": "2595",
        "Host": "api-graphql-lambda.prod.zoopla.co.uk",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.9.2"
    }
    payload = {
        "operationName": "propertiesSearchResults",
        "variables": {
            "geoIdentifier": item.location.lower().replace(' ', '-'),
            "first": 12,
            "after": str(item.page)
        },
        "query": "query propertiesSearchResults($geoIdentifier: GeoIdentifier, $geoString: NonEmptyString, "
                 "$houseType: HouseType, $rangeMonths: MarketActivityWindow, $after: ID, $first: PositiveInt, "
                 "$fromLastSaleDate: String, $propertyTypeCode: String, $sortDirection: String, $sortOrder: "
                 "String, $toLastSaleDate: String) {\n  propertiesSearch(\n    after: $after\n    first: "
                 "$first\n    input: {geoIdentifier: $geoIdentifier, fromLastSaleDate: $fromLastSaleDate, "
                 "propertyTypeCode: $propertyTypeCode, sortDirection: $sortDirection, sortOrder: $sortOrder, "
                 "toLastSaleDate: $toLastSaleDate}\n  ) {\n    ...PropertiesSearchConnection\n    "
                 "...PropertiesSearchResponseError\n    __typename\n  }\n  area(geoIdentifier: $geoIdentifier) "
                 "{\n    geoType\n    id\n    name\n    shortName\n    __typename\n  }\n  marketActivity(\n    "
                 "geoIdentifier: $geoIdentifier\n    geoString: $geoString\n    houseType: $houseType\n    "
                 "rangeMonths: $rangeMonths\n  ) {\n    data {\n      averagePricePaid\n      propertiesSold\n "
                 "     __typename\n    }\n    __typename\n  }\n}\n\nfragment PropertiesSearchConnection on "
                 "PropertiesSearchConnection {\n  pageInfo {\n    hasPreviousPage\n    hasNextPage\n   "
                 " startCursor\n    endCursor\n    __typename\n  }\n  totalResults\n  edges {\n    cursor\n    "
                 "node {\n      propertyId\n      uprn\n      address {\n        fullAddress\n        postcode\n"
                 "        country\n        outcode\n        latitude\n        longitude\n        __typename\n   "
                 "   }\n      attributes {\n        bathrooms\n        bedrooms\n        livingRooms\n        "
                 "propertyType\n        tenure\n        __typename\n      }\n      history {\n        "
                 "historicSales {\n          date\n          price\n          percentageChange\n         "
                 " numericChange\n          __typename\n        }\n        soldPricesDataSource\n        "
                 "__typename\n      }\n      saleEstimate {\n        lowerPrice\n        currentPrice\n       "
                 " upperPrice\n        confidenceLevel\n        __typename\n      }\n      rentEstimate {\n     "
                 "   currentPrice\n        lowerPrice\n        upperPrice\n        __typename\n      }\n      "
                 "trackedProperty {\n        isTracked\n        permissions {\n          hasPermissions\n        "
                 "  ids\n          __typename\n        }\n        relationship\n        __typename\n      }\n    "
                 "  __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment "
                 "PropertiesSearchResponseError on PropertiesSearchResponseError {\n  errors {\n    message\n   "
                 " __typename\n  }\n  __typename\n}"
    }
    response = requests.post(url=url,headers=headers,data=json.dumps(payload))
    resp_data = response.json()

    return resp_data['data']['propertiesSearch']['edges']

@app.post("/fetchproperty")
def fetch_sible(uprn: UPRN):
    url = 'https://api-graphql-lambda.prod.zoopla.co.uk/graphql/'
    headers = {
        "accept": "*/*",
        "x-api-key": "3Vzj2wUfaP3euLsV4NV9h3UAVUR3BoWd5clv9Dvu",
        "origin": "zoopla-mobile-app",
        "Content-Type": "application/json",
        "Content-Length": "2595",
        "Host": "api-graphql-lambda.prod.zoopla.co.uk",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.9.2"
    }

    parameter = uprn.uprn

    payload = {"operationName": "property", "variables": {"uprn": str(parameter)},
               "query": "query property($uprn: String) {\n  property(uprn: $uprn) {\n    ...PROPERTY\n    __typename\n  }\n}\n\nfragment PROPERTY on Property {\n  uprn\n  address {\n    fullAddress\n    postcode\n    country\n    outcode\n    latitude\n    longitude\n    uprn\n    __typename\n  }\n  attributes {\n    bathrooms\n    bedrooms\n    livingRooms\n    tenure\n    propertyType\n    __typename\n  }\n  history {\n    historicListings {\n      attributes {\n        bathrooms\n        bedrooms\n        livingRooms\n        __typename\n      }\n      date\n      floorplans {\n        thumbnail\n        medium\n        large\n        __typename\n      }\n      images {\n        thumbnail\n        medium\n        large\n        __typename\n      }\n      price\n      priceType\n      uri\n      __typename\n    }\n    historicSales {\n      date\n      price\n      percentageChange\n      numericChange\n      __typename\n    }\n    soldPricesDataSource\n    __typename\n  }\n  rentEstimate {\n    lowerPrice\n    currentPrice\n    upperPrice\n    __typename\n  }\n  saleEstimate {\n    lowerPrice\n    currentPrice\n    upperPrice\n    confidenceLevel\n    valueChange {\n      numericChange\n      percentageChange\n      saleDate\n      __typename\n    }\n    __typename\n  }\n  saleEstimates {\n    confidenceLevel\n    currentPrice\n    ingestedAt\n    builtAt\n    lowerPrice\n    upperPrice\n    __typename\n  }\n  trackedProperty {\n    equity {\n      calculatedEquity\n      estimatedPrice\n      outstandingMortgage\n      securedLoan\n      __typename\n    }\n    isTracked\n    permissions {\n      hasPermissions\n      ids\n      __typename\n    }\n    relationship\n    __typename\n  }\n  liveListings {\n    branchName\n    transactionType\n    uri\n    listingId\n    displayAddress\n    price\n    rentPerMonth\n    totalBedrooms\n    __typename\n  }\n  pointsOfInterest {\n    title\n    distanceMiles\n    latitude\n    longitude\n    type\n    address\n    __typename\n  }\n  ...SIMILAR_LISTINGS\n  ...SIMILAR_PROPERTIES\n  __typename\n}\n\nfragment SIMILAR_LISTINGS on Property {\n  similarListingsV2(limit: 5) {\n    listingId\n    title\n    imagePreview {\n      src\n      caption\n      __typename\n    }\n    counts {\n      numBedrooms\n      numBathrooms\n      numLivingRooms\n      __typename\n    }\n    pricing {\n      priceQualifierLabel\n      label\n      __typename\n    }\n    displayAddress\n    listingUris {\n      detail\n      __typename\n    }\n    location {\n      coordinates {\n        latitude\n        longitude\n        __typename\n      }\n      uprn\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SIMILAR_PROPERTIES on Property {\n  similarProperties(limit: 5) {\n    uprn\n    address {\n      fullAddress\n      longitude\n      latitude\n      postcode\n      uprn\n      __typename\n    }\n    attributes {\n      bathrooms\n      bedrooms\n      livingRooms\n      __typename\n    }\n    history {\n      historicSales {\n        date\n        price\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"}

    response = requests.post(url=url, headers=headers, data=json.dumps(payload))
    resp_data = response.json()
    return resp_data
