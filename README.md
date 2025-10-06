# TBR Book Locator

A website that lets you search books, check their availability on [Everand](https://www.everand.com/), and add them to a to be read (TBR) list on [Hardcover](https://hardcover.app/).

## How it works

**Tech used:** React, Flask, Bootstrap, Vite

The search uses the [Hardcover GraphQL API](https://docs.hardcover.app/api/getting-started/) to query books by title and/or author.

After getting the search results back, there will be an option to check if any ebooks or audiobooks are available to read on Everand. This works by searching the ISBNs returned from the Hardcover API on Everand. The TBR Book Locator will display if an ebook or an audiobook is available with links to each one in Everand.

There will be an option to add a book to a Hardcover list. This is super useful if that book is unavailable on Everand but you still want to keep track of it.