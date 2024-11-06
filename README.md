# Tokped-API-Scrapper

This repository is an automated web scraping method through the website's API (QueryV5), to scrape or collect data from a famouse e-commerce in Indonesia, Tokopedia.
The scrape method is build using Python language, with the help of Python's library:
 - **Pandas** to transform the data into DataFrame and save it to xlsx format. (version 2.2.3)

(**Note** : The program is build using Python version 3.11.4)

## How to Run
1. As it is build using Python, you can just run it using window's cmd/powershell:
    ```
    python tokped_api_scrapper.py [shop_domain] [how_many_page_to_scrap]
    ```
2. Or run it using the `.bat` file included in the project

`[shop_domain]` is the name of the shop after the `tokopedia.com\` link.
For example `https://www.tokopedia.com/its-iki` shop domain would be `its-iki`

## Result
Here is the list  of column name and definition in the excel file:
|Column Name        |Definition                                         |                          
|-------------------|---------------------------------------------------|
|Nama Produk        |Name of the product                                |
|Harga Produk       |Price of the product (in IDR)                      |
|Rating Produk      |The overall rating of the product                  |
|Gambar Produk      |Image link to the first product image              |
|Link Produk        |The link of the product                            |
|Stock              |Number of stock remaining                          |
|Etalase            |The product's catalogue                            |
|Deskripsi Produk   |The product's description                          |