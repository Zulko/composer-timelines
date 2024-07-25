# Composer timelines

This web app (live [here on Github pages]()) displays timelines of events and works for selected composers. Ever wondered what Haydn was about when Mozart composed his first symphony, what Wagner was brewing when Bizet released Carmen, or what was happening in the world the year Chopin released his Etudes? This app is for you!

The project relies extensively on ChatGPT/GPT4 for data collection - see [this blog post]() for details.

## Adding/requesting more composers

Any classical composer with public-domain work from before 1950 is of interest to this project.

To add a composer, all you need to do is add a `COMPOSER NAME.json` in `data/composer_data`, and add an entry for the composer in `composer_list_with_metadata.json`.

MRs are encouraged. You can also request new composers by opening an Issue in this Github repo, or [emailing me](mailto:valentin.zulkower+@gmail.com?subject=Composer%20timelines%3A%20new%20composers%20request").

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