---
marp: true

paginate: true
class: invert
footer: 'Clément Fleury [![Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License")](http://creativecommons.org/licenses/by-nc-sa/4.0/ "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License")'

style: |
    @import url(https://fonts.bunny.net/css?family=asap:400|bungee:400|angkor:400);

    :root {
      font-family: Asap, Arial, sans-serif;
      background-color: snow;
      justify-content: start;
      padding: 50px;
    }

    section.invert {
      background-color: #17202A;
    }

    section.lead {
      justify-content: center;
      padding: 100px;
    }

    h1, h2, h3, h4, h5, h6 {
      font-weight: 400;
    }

    h1, h2 {
      font-family: Bungee;
      text-transform: uppercase;
      text-align: center;
    }

    h3, h4, h5, h6 {
      font-family: Angkor;
      text-transform: capitalize;
    }

    h1 {
      font-size: 4rem;
      color: crimson;
    }

    h2 {
      font-size: 2rem;
      color: navy;
    }

    h3 {
      font-size: 1.5rem;
      color: navy;
    }
    section.invert h3 {
      color: gold;
    }

    h4 {
      font-size: 1.25rem;
    }

    h5 {
      font-size: 1.125rem;
    }

    h6 {
      font-size: 1rem;
    }

    strong {
      color: tomato;
    }
    section.invert strong {
      color: aquamarine;
    }

    em {
      color: salmon;
    }
    section.invert em {
      color: aqua;
    }

    img {
      background-color: transparent;
    }
    section.invert img {
      background-color: snow;
    }

    table, img[alt~="center-img"] {
      justify-content: center;
      display: block;
      margin: 0 auto;
    }
---

### Target performance management policy

In order to achieve the target performance, the following policy must be implemented :

-   **store** each dialogs and inferred _intents_ and _entities_ in a _database_
-   **transform and load** (ETL) the raw data in a _datawarehouse_ in a _format compatible with the LUIS service_
-   daily **re-train** the _language understanding model_ with the new _intents_ and _entities_ of the **successful** bookings

---

### Target production architecture

![center-img h:550px](img/target-architecture.drawio.png "Target production architecture")
