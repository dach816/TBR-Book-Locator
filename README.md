# TBR Book Locator

A website that lets you search books, check their availability on Everand, a book subscription site, and add them to a to be read (TBR) list on Hardcover, a book tracking site.

<img src="docs/images/TBR Book Locator Screenshot 10-23-25.png" alt="screenshot" style="max-width: 100%;">

## How it works

**Tech used:** React, Flask, Bootstrap, Vite

The search uses the [Hardcover GraphQL API](https://docs.hardcover.app/api/getting-started/) to query books by title and/or author.

After getting the search results back, there is an option to check if any ebooks or audiobooks are available to read on Everand. This works by searching the ISBNs returned from the Hardcover API on Everand. The TBR Book Locator will display links to every ebook and audiobook available in Everand.

There will be an option to add a book to a to be read (TBR) list on Hardcover. This is super useful if that book is unavailable on Everand but you still want to keep track of it.