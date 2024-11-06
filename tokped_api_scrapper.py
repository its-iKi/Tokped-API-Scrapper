import requests
import json
import pandas as pd

def get_args() -> dict:
    import argparse
    parser = argparse.ArgumentParser(description="Tokopedia Shop Scraper")
    parser.add_argument('shopIdentifier', type=str, help='Target shop identifier', default='aquaings')
    # parser.add_argument('shopId', type=str, help='Target shop number id', default='1207917')
    parser.add_argument('pageToScrape', type=int, help='The number  of page(s) you want to scrape', default=1)
    return vars(parser.parse_args())

args = get_args()
shop_identifier = args['shopIdentifier']
shop_id = 0#args['shopId']
shop_pageCount = args['pageToScrape']

product_list = list()

print(f'[Tokped API Scraper]: Domain name = {shop_identifier}, Page to scrap = {shop_pageCount}')
# Getting shop's core info
print("[Tokped API Scraper]: Getting shop info for shop's ID")
shopInfo_link = 'https://gql.tokopedia.com/graphql/ShopInfoCore'
shopInfo_header = {
   'sec-ch-ua' : '"Chromium";v="128", "Not;A=Brand";v="24", "Opera GX";v="114"',
   'X-Version' : '6e0e4d6',
   'sec-ch-ua-mobile' : '?0',
   'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0',
   'content-type' : 'application/json',
   'accept' : '*/*',
   'Referer' : f'https://www.tokopedia.com/{shop_identifier}?source=universe&st=product',
   'X-Source' : 'tokopedia-lite',
   'X-Tkpd-Lite-Service' : 'zeus',
   'sec-ch-ua-platform' : '"Windows"'}
shopInfo_query = f'[{{"operationName":"ShopInfoCore","variables":{{"id":0,"domain":"{shop_identifier}"}},"query":"query ShopInfoCore($id: Int\u0021, $domain: String) {{\\n  shopInfoByID(input: {{shopIDs: [$id], fields: [\\"active_product\\", \\"allow_manage_all\\", \\"assets\\", \\"core\\", \\"closed_info\\", \\"create_info\\", \\"favorite\\", \\"location\\", \\"status\\", \\"is_open\\", \\"other-goldos\\", \\"shipment\\", \\"shopstats\\", \\"shop-snippet\\", \\"other-shiploc\\", \\"shopHomeType\\", \\"branch-link\\", \\"goapotik\\", \\"fs_type\\"], domain: $domain, source: \\"shoppage\\"}}) {{\\n    result {{\\n      shopCore {{\\n        description\\n        domain\\n        shopID\\n        name\\n        tagLine\\n        defaultSort\\n        __typename\\n      }}\\n      createInfo {{\\n        openSince\\n        __typename\\n      }}\\n      favoriteData {{\\n        totalFavorite\\n        alreadyFavorited\\n        __typename\\n      }}\\n      activeProduct\\n      shopAssets {{\\n        avatar\\n        cover\\n        __typename\\n      }}\\n      location\\n      isAllowManage\\n      branchLinkDomain\\n      isOpen\\n      shipmentInfo {{\\n        isAvailable\\n        image\\n        name\\n        product {{\\n          isAvailable\\n          productName\\n          uiHidden\\n          __typename\\n        }}\\n        __typename\\n      }}\\n      shippingLoc {{\\n        districtName\\n        cityName\\n        __typename\\n      }}\\n      shopStats {{\\n        productSold\\n        totalTxSuccess\\n        totalShowcase\\n        __typename\\n      }}\\n      statusInfo {{\\n        shopStatus\\n        statusMessage\\n        statusTitle\\n        tickerType\\n        __typename\\n      }}\\n      closedInfo {{\\n        closedNote\\n        until\\n        reason\\n        detail {{\\n          status\\n          __typename\\n        }}\\n        __typename\\n      }}\\n      bbInfo {{\\n        bbName\\n        bbDesc\\n        bbNameEN\\n        bbDescEN\\n        __typename\\n      }}\\n      goldOS {{\\n        isGold\\n        isGoldBadge\\n        isOfficial\\n        badge\\n        shopTier\\n        __typename\\n      }}\\n      shopSnippetURL\\n      customSEO {{\\n        title\\n        description\\n        bottomContent\\n        __typename\\n      }}\\n      isQA\\n      isGoApotik\\n      partnerInfo {{\\n        fsType\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    error {{\\n      message\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\n"}}]'

shopInfo_response = requests.post(shopInfo_link, headers=shopInfo_header, data=shopInfo_query)
shop_id = shopInfo_response.json()[0]['data']['shopInfoByID']['result'][0]['shopCore']['shopID']
print(f'[Tokped API Scraper]: Domain name = {shop_identifier}, ShopID = {shop_id}, Page to scrap = {shop_pageCount}')
shopInfo_response.close()

# Getting shop's product list
for i in range(0, shop_pageCount):
    shop_link = 'https://gql.tokopedia.com/graphql/ShopProducts'
    shop_header = {
        'sec-ch-ua-platform' : '"Windows"',
        'X-Version' : '6e0e4d6',
        'Referer' : 'https://www.tokopedia.com/' + shop_identifier + '/product/page/' + str(i),
        'sec-ch-ua' : '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile' : '?0',
        'X-Source' : 'tokopedia-lite',
        'X-Device' : 'default_v3',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'accept' : '*/*',
        'DNT' : '1',
        'content-type' : 'application/json',
        'X-Tkpd-Lite-Service' : 'zeus'}
    shop_query = f'[{{"operationName":"ShopProducts","variables":{{"source":"shop","sid":"{shop_id}","page":{i},"perPage":80,"etalaseId":"etalase","sort":1,"user_districtId":"2274","user_cityId":"176","user_lat":"0","user_long":"0"}},"query":"query ShopProducts($sid: String\u0021, $source: String, $page: Int, $perPage: Int, $keyword: String, $etalaseId: String, $sort: Int, $user_districtId: String, $user_cityId: String, $user_lat: String, $user_long: String) {{\\n  GetShopProduct(shopID: $sid, source: $source, filter: {{page: $page, perPage: $perPage, fkeyword: $keyword, fmenu: $etalaseId, sort: $sort, user_districtId: $user_districtId, user_cityId: $user_cityId, user_lat: $user_lat, user_long: $user_long}}) {{\\n    status\\n    errors\\n    links {{\\n      prev\\n      next\\n      __typename\\n    }}\\n    data {{\\n      name\\n      product_url\\n      product_id\\n      price {{\\n        text_idr\\n        __typename\\n      }}\\n      primary_image {{\\n        original\\n        thumbnail\\n        resize300\\n        __typename\\n      }}\\n      flags {{\\n        isSold\\n        isPreorder\\n        isWholesale\\n        isWishlist\\n        __typename\\n      }}\\n      campaign {{\\n        discounted_percentage\\n        original_price_fmt\\n        start_date\\n        end_date\\n        __typename\\n      }}\\n      label {{\\n        color_hex\\n        content\\n        __typename\\n      }}\\n      label_groups {{\\n        position\\n        title\\n        type\\n        url\\n        __typename\\n      }}\\n      badge {{\\n        title\\n        image_url\\n        __typename\\n      }}\\n      stats {{\\n        reviewCount\\n        rating\\n        averageRating\\n        __typename\\n      }}\\n      category {{\\n        id\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\n"}}]'
    
    shop_response = requests.post(shop_link, headers=shop_header, data=shop_query)
    shop_products = shop_response.json()[0]['data']['GetShopProduct']['data']
    
    for j in range(0, len(shop_products)):
        product = {
           'Nama Produk' : shop_products[j]['name'],
           'Harga Produk' : shop_products[j]['price']['text_idr'],
           'Rating Produk' : shop_products[j]['stats']['averageRating'],
           'Gambar Produk' : shop_products[j]['primary_image']['original'],
           'Link Produk' : shop_products[j]['product_url']
        }
        
        product_list.append(product)
    
    print(f'[Tokped API Scraper]: Getting page ({i + 1}/{shop_pageCount})')

print(f'[Tokped API Scraper]: Processing {len(product_list)} products')
# print(json.dumps(product_list[0]['nama_produk'], indent=4))

# Getting the product
for i in range(0, len(product_list)):
   product_link = 'https://gql.tokopedia.com/graphql/PDPGetLayoutQuery'
   product_header = {
        'sec-ch-ua-platform' : '"Windows"',
        'X-Version' : '6e0e4d6',
        'Referer' : f"{product_list[i]['Link Produk']}",
        'sec-ch-ua' : '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile' : '?0',
        'X-Source' : 'tokopedia-lite',
        'X-TKPD-AKAMAI' : 'pdpGetLayout',
        'x-device' : 'desktop',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'accept' : '*/*',
        'DNT' : '1',
        'content-type' : 'application/json',
        'X-Tkpd-Lite-Service' : 'zeus'}
   replacedLink = product_list[i]['Link Produk'].replace(('https://www.tokopedia.com/' + shop_identifier + '/'), f'')
   markIndex = replacedLink.find('?extParam')
   product_key = replacedLink[0:markIndex]
   extParam = replacedLink[(markIndex + 10):len(replacedLink)]
   product_query = json.dumps([
       {
           "operationName": "PDPGetLayoutQuery",
           "variables": {
               "shopDomain": shop_identifier,
               "productKey": product_key,
               "layoutID": "",
               "apiVersion": 1,
               "tokonow": {
                   "shopID": "0",
                   "whID": "0",
                   "serviceType": ""
                   },
               "deviceID": "NTgyMDI3YzNjNzRhZTBjNGQyMDI2YTI4MjJjMzYwMjNjM2JmZDBmODY1ZGI1MGYwZDhiYTI3MDlhZDk3YmU0M2NmOTEzZmFjOWU1MTY4MTM3YmRjOWU1MTY2ZjU1NTgy47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=",
               "userLocation": {
                   "cityID": "176",
                   "addressID": "",
                   "districtID": "2274",
                   "postalCode": "",
                   "latlon": ""
                   },
                "extParam": extParam
        },
        "query": "fragment ProductVariant on pdpDataProductVariant {\n  errorCode\n  parentID\n  defaultChild\n  sizeChart\n  totalStockFmt\n  variants {\n    productVariantID\n    variantID\n    name\n    identifier\n    option {\n      picture {\n        urlOriginal: url\n        urlThumbnail: url100\n        __typename\n      }\n      productVariantOptionID\n      variantUnitValueID\n      value\n      hex\n      stock\n      __typename\n    }\n    __typename\n  }\n  children {\n    productID\n    price\n    priceFmt\n    slashPriceFmt\n    discPercentage\n    optionID\n    optionName\n    productName\n    productURL\n    picture {\n      urlOriginal: url\n      urlThumbnail: url100\n      __typename\n    }\n    stock {\n      stock\n      isBuyable\n      stockWordingHTML\n      minimumOrder\n      maximumOrder\n      __typename\n    }\n    isCOD\n    isWishlist\n    campaignInfo {\n      campaignID\n      campaignType\n      campaignTypeName\n      campaignIdentifier\n      background\n      discountPercentage\n      originalPrice\n      discountPrice\n      stock\n      stockSoldPercentage\n      startDate\n      endDate\n      endDateUnix\n      appLinks\n      isAppsOnly\n      isActive\n      hideGimmick\n      isCheckImei\n      minOrder\n      showStockBar\n      __typename\n    }\n    thematicCampaign {\n      additionalInfo\n      background\n      campaignName\n      icon\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductMedia on pdpDataProductMedia {\n  media {\n    type\n    urlOriginal: URLOriginal\n    urlThumbnail: URLThumbnail\n    urlMaxRes: URLMaxRes\n    videoUrl: videoURLAndroid\n    prefix\n    suffix\n    description\n    variantOptionID\n    __typename\n  }\n  videos {\n    source\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCategoryCarousel on pdpDataCategoryCarousel {\n  linkText\n  titleCarousel\n  applink\n  list {\n    categoryID\n    icon\n    title\n    isApplink\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductHighlight on pdpDataProductContent {\n  name\n  price {\n    value\n    currency\n    priceFmt\n    slashPriceFmt\n    discPercentage\n    __typename\n  }\n  campaign {\n    campaignID\n    campaignType\n    campaignTypeName\n    campaignIdentifier\n    background\n    percentageAmount\n    originalPrice\n    discountedPrice\n    originalStock\n    stock\n    stockSoldPercentage\n    threshold\n    startDate\n    endDate\n    endDateUnix\n    appLinks\n    isAppsOnly\n    isActive\n    hideGimmick\n    showStockBar\n    __typename\n  }\n  thematicCampaign {\n    additionalInfo\n    background\n    campaignName\n    icon\n    __typename\n  }\n  stock {\n    useStock\n    value\n    stockWording\n    __typename\n  }\n  variant {\n    isVariant\n    parentID\n    __typename\n  }\n  wholesale {\n    minQty\n    price {\n      value\n      currency\n      __typename\n    }\n    __typename\n  }\n  isCashback {\n    percentage\n    __typename\n  }\n  isTradeIn\n  isOS\n  isPowerMerchant\n  isWishlist\n  isCOD\n  preorder {\n    duration\n    timeUnit\n    isActive\n    preorderInDays\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCustomInfo on pdpDataCustomInfo {\n  icon\n  title\n  isApplink\n  applink\n  separator\n  description\n  __typename\n}\n\nfragment ProductInfo on pdpDataProductInfo {\n  row\n  content {\n    title\n    subtitle\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetail on pdpDataProductDetail {\n  content {\n    title\n    subtitle\n    applink\n    showAtFront\n    isAnnotation\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDataInfo on pdpDataInfo {\n  icon\n  title\n  isApplink\n  applink\n  content {\n    icon\n    text\n    __typename\n  }\n  __typename\n}\n\nfragment ProductSocial on pdpDataSocialProof {\n  row\n  content {\n    icon\n    title\n    subtitle\n    applink\n    type\n    rating\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetailMediaComponent on pdpDataProductDetailMediaComponent {\n  title\n  description\n  contentMedia {\n    url\n    ratio\n    type\n    __typename\n  }\n  show\n  ctaText\n  __typename\n}\n\nquery PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $tokonow: pdpTokoNow, $deviceID: String) {\n  pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam, tokonow: $tokonow, deviceID: $deviceID) {\n    requestID\n    name\n    pdpSession\n    basicInfo {\n      alias\n      createdAt\n      isQA\n      id: productID\n      shopID\n      shopName\n      minOrder\n      maxOrder\n      weight\n      weightUnit\n      condition\n      status\n      url\n      needPrescription\n      catalogID\n      isLeasing\n      isBlacklisted\n      isTokoNow\n      menu {\n        id\n        name\n        url\n        __typename\n      }\n      category {\n        id\n        name\n        title\n        breadcrumbURL\n        isAdult\n        isKyc\n        minAge\n        detail {\n          id\n          name\n          breadcrumbURL\n          isAdult\n          __typename\n        }\n        __typename\n      }\n      txStats {\n        transactionSuccess\n        transactionReject\n        countSold\n        paymentVerified\n        itemSoldFmt\n        __typename\n      }\n      stats {\n        countView\n        countReview\n        countTalk\n        rating\n        __typename\n      }\n      __typename\n    }\n    components {\n      name\n      type\n      position\n      data {\n        ...ProductMedia\n        ...ProductHighlight\n        ...ProductInfo\n        ...ProductDetail\n        ...ProductSocial\n        ...ProductDataInfo\n        ...ProductCustomInfo\n        ...ProductVariant\n        ...ProductCategoryCarousel\n        ...ProductDetailMediaComponent\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }])
   
   product_response = requests.post(product_link, headers=product_header, data=product_query)
   products = product_response.json()[0]['data']['pdpGetLayout']
   for j in range(0, len(products.get('components'))):
      if products.get('components')[j].get('name') == 'product_content':
         product_list[i]['Stock'] = products.get('components')[j].get('data')[0]['stock']['value']
      if products.get('components')[j].get('name') == 'product_detail':
         for k in range(0, len(products.get('components')[j].get('data')[0]['content'])):
            if(products.get('components')[j].get('data')[0]['content'][k].get('title') == 'Etalase'):
               product_list[i]['Etalase'] = products.get('components')[j].get('data')[0]['content'][k]['subtitle']
            if(products.get('components')[j].get('data')[0]['content'][k].get('title') == 'Deskripsi'):
               product_list[i]['Deskripsi Produk'] = products.get('components')[j].get('data')[0]['content'][k]['subtitle']
#    print(f'[Tokped API Scraper]: Processing {len(product_list)} products')

print(f'[Tokped API Scraper]: Exporting {len(product_list)} product to excel(xlsx)')

df = pd.DataFrame.from_dict(product_list)
df.to_excel(f'{shop_identifier}_scrap_data.xlsx', index=False, sheet_name='All Products')
print('[Tokped API Scraper]: Excel files created')