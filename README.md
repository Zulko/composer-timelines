# Composer timelines

This web app (live [here on Github pages](https://zulko.github.io/composer-timelines/)) displays timelines of events and works for selected composers. Ever wondered what Verdi was up to when Puccini composed his first opera? This app is for you! It relies extensively on ChatGPT/GPT4 for building an event database from Wikipedia, which makes it extremely easy to add a new composers, in 3 minutes and 2c of OpenAI credit (see [this write-up](https://github.com/Zulko/composer-timelines/blob/main/docs/write-up.md))

<center><img src='./docs/screenshot.png'/></center>

## Adding/requesting more composers

Any classical composer with public-domain work from before 1950 is of interest to this project.

To add a composer, all you need to do is add a `COMPOSER NAME.json` in `data/composer_data`, and add an entry for the composer in `composer_list_with_metadata.json`.
This can be done by hand through your own research, or automated with ChatGPT via this script:

```bash
# python3 -m pip install data_collection/requirements.txt
python3 data_collection/add_composer.py --composer="Anatoly Lyadov" --target=public/data/
```

PRs are encouraged (one composer per request please). You can also request new composers by opening an Issue in this Github repo, or [emailing me](mailto:valentin.zulkower+@gmail.com?subject=Composer%20timelines%3A%20new%20composers%20request").

## Running the app locally

Run the project with:

```bash
npm install
npm run dev
```

Navigate to [localhost:8080](http://localhost:8080). You should see your app running. Edit a component file in `src`, save it, and the changes should appear live in the app.

If you're using [Visual Studio Code](https://code.visualstudio.com/) we recommend installing the official extension [Svelte for VS Code](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode). If you are using other editors you may need to install a plugin in order to get syntax highlighting and intellisense.

To create an optimised version of the app:

```bash
npm run build
```
